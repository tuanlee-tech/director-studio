#!/usr/bin/env pwsh
# ============================================================
# AI Audio Platform - Smart Launcher (Windows)
# Native-first: runs services directly with Python/uv
# Falls back to Docker if available
# ============================================================

param(
    [ValidateSet("start", "stop", "status", "install", "studio")]
    [string]$Action = "start",
    [switch]$StudioOnly,
    [switch]$TTSOnly,
    [switch]$UseDocker,
    [switch]$Background
)

$ErrorActionPreference = "Continue"
$ROOT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$TTS_DIR = Join-Path $ROOT_DIR "VieNeu-TTS"
$STUDIO_DIR = Join-Path $ROOT_DIR "studio"
$PIDFILE_TTS = Join-Path $ROOT_DIR ".tts.pid"
$PIDFILE_STUDIO = Join-Path $ROOT_DIR ".studio.pid"

# --- Colors ---
function Write-OK($msg)      { Write-Host "[OK] $msg" -ForegroundColor Green }
function Write-Warn($msg)    { Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err($msg)     { Write-Host "[ERROR] $msg" -ForegroundColor Red }
function Write-Info($msg)    { Write-Host "[INFO] $msg" -ForegroundColor Cyan }

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AI Audio Platform - Smart Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# --- Detect Environment ---
function Get-EnvironmentInfo {
    $env_info = @{
        HasPython = $false
        PythonVersion = ""
        HasUV = $false
        HasDocker = $false
        HasNvidiaGPU = $false
        GPUName = ""
        VRAM_MB = 0
        HasCUDA_ORT = $false
        HasTorch = $false
        HasTorchCUDA = $false
        ModelCached = $false
        CanUseGPU = $false
        RecommendedBackend = "onnx-cpu"
    }

    # Python
    try {
        $pyVer = & python --version 2>&1
        if ($pyVer -match "Python (\d+\.\d+)") {
            $env_info.HasPython = $true
            $env_info.PythonVersion = $Matches[1]
        }
    } catch {}

    # uv
    try { $null = & uv --version 2>&1; if ($LASTEXITCODE -eq 0) { $env_info.HasUV = $true } } catch {}

    # Docker
    try { $null = & docker version 2>&1; if ($LASTEXITCODE -eq 0) { $env_info.HasDocker = $true } } catch {}

    # NVIDIA GPU
    try {
        $gpuInfo = & nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>&1
        if ($LASTEXITCODE -eq 0 -and $gpuInfo) {
            $env_info.HasNvidiaGPU = $true
            $parts = $gpuInfo -split ","
            $env_info.GPUName = $parts[0].Trim()
            if ($parts[1] -match "(\d+)") { $env_info.VRAM_MB = [int]$Matches[1] }
        }
    } catch {}

    # Check venv capabilities
    $venvPython = Join-Path $TTS_DIR ".venv\Scripts\python.exe"
    if (Test-Path $venvPython) {
        # ONNX CUDA provider
        try {
            $ort = & $venvPython -c "import onnxruntime as ort; print('CUDAExecutionProvider' in ort.get_available_providers())" 2>&1
            if ($ort -eq "True") { $env_info.HasCUDA_ORT = $true }
        } catch {}

        # Torch + CUDA
        try {
            $torch = & $venvPython -c "import torch; print(torch.cuda.is_available())" 2>&1
            $env_info.HasTorch = ($LASTEXITCODE -eq 0)
            if ($torch -eq "True") { $env_info.HasTorchCUDA = $true }
        } catch {}

        # Model cached
        try {
            $cached = & $venvPython -c "
from huggingface_hub import try_to_load_from_cache
import os
r = try_to_load_from_cache('pnnbao-ump/VieNeu-TTS-v3-Turbo', 'config.json')
print('yes' if r is not None and r != False else 'no')
" 2>&1
            if ($cached -match "yes") { $env_info.ModelCached = $true }
        } catch {}
    }

    # Determine recommended backend
    if ($env_info.HasTorchCUDA -and $env_info.VRAM_MB -ge 3000) {
        $env_info.RecommendedBackend = "pytorch-cuda"
        $env_info.CanUseGPU = $true
    } elseif ($env_info.HasCUDA_ORT) {
        $env_info.RecommendedBackend = "onnx-cuda"
        $env_info.CanUseGPU = $true
    } else {
        $env_info.RecommendedBackend = "onnx-cpu"
    }

    return $env_info
}

# --- Install Dependencies ---
function Install-Platform {
    Write-Info "Setting up AI Audio Platform..."

    # Check Python
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Err "Python not found. Install Python 3.12:"
        Write-Host "  winget install -e --id Python.Python.3.12"
        exit 1
    }

    # Check/Install uv
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Write-Warn "uv not found. Installing..."
        Invoke-Expression "& { $(Invoke-RestMethod 'https://astral.sh/uv/install.ps1') }"
        $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
    }

    # Setup VieNeu-TTS
    Write-Info "Setting up VieNeu-TTS..."
    Push-Location $TTS_DIR
    try {
        & uv sync
        if ($LASTEXITCODE -ne 0) { Write-Err "uv sync failed"; exit 1 }
        Write-OK "VieNeu-TTS dependencies installed"
    } finally { Pop-Location }

    # Setup Studio
    Write-Info "Setting up Studio UI..."
    if (-not (Test-Path (Join-Path $STUDIO_DIR "venv"))) {
        & python -m venv (Join-Path $STUDIO_DIR "venv")
    }
    $studioPip = Join-Path $STUDIO_DIR "venv\Scripts\pip.exe"
    & $studioPip install -q flask requests 2>&1 | Out-Null
    Write-OK "Studio UI dependencies installed"

    # Copy .env
    $envFile = Join-Path $ROOT_DIR ".env"
    $envExample = Join-Path $ROOT_DIR ".env.example"
    if (-not (Test-Path $envFile) -and (Test-Path $envExample)) {
        Copy-Item $envExample $envFile
        Write-Info "Created .env from .env.example"
    }

    Write-OK "Installation complete!"
}

# --- Start Services ---
function Start-Services {
    $envInfo = Get-EnvironmentInfo

    Write-Host "Environment:" -ForegroundColor Cyan
    Write-Host "  Python:    $($envInfo.PythonVersion)" -ForegroundColor White
    Write-Host "  uv:        $(if ($envInfo.HasUV) {'Yes'} else {'No'})" -ForegroundColor White
    Write-Host "  GPU:       $(if ($envInfo.HasNvidiaGPU) {"$($envInfo.GPUName) ($($envInfo.VRAM_MB) MB)"} else {'None'})" -ForegroundColor White
    Write-Host "  Backend:   $($envInfo.RecommendedBackend)" -ForegroundColor White
    Write-Host "  Model:     $(if ($envInfo.ModelCached) {'Cached (ready)'} else {'Will download on first load'})" -ForegroundColor White
    Write-Host ""

    # --- Start TTS ---
    if (-not $StudioOnly) {
        Write-Info "Starting VieNeu TTS on http://localhost:7860 ..."

        # Check if already running
        try {
            $r = Invoke-WebRequest -Uri "http://127.0.0.1:7860/" -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
            if ($r.StatusCode -eq 200) {
                Write-OK "VieNeu TTS already running at http://localhost:7860"
            }
        } catch {
            # Not running, start it
            $venvPython = Join-Path $TTS_DIR ".venv\Scripts\python.exe"
            if (-not (Test-Path $venvPython)) {
                Write-Err "VieNeu-TTS venv not found. Run: .\launcher.ps1 install"
                exit 1
            }

            $logOut = Join-Path $TTS_DIR "vieneu-web.stdout.log"
            $logErr = Join-Path $TTS_DIR "vieneu-web.stderr.log"

            $proc = Start-Process -FilePath $venvPython `
                -ArgumentList "apps/gradio_main.py" `
                -WorkingDirectory $TTS_DIR `
                -RedirectStandardOutput $logOut `
                -RedirectStandardError $logErr `
                -PassThru -WindowStyle Hidden

            $proc.Id | Out-File $PIDFILE_TTS -Force
            Write-Info "TTS started (PID: $($proc.Id)), waiting for ready..."

            # Wait for ready (max 120s for first-time model download)
            $ready = $false
            for ($i = 0; $i -lt 120; $i++) {
                Start-Sleep -Seconds 2
                try {
                    $r = Invoke-WebRequest -Uri "http://127.0.0.1:7860/" -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
                    if ($r.StatusCode -eq 200) { $ready = $true; break }
                } catch {}
                if ($i % 5 -eq 0) {
                    $dots = "." * (($i / 5) % 4 + 1)
                    Write-Host "`r  Waiting$dots    " -NoNewline
                }
            }

            if ($ready) {
                Write-Host ""
                Write-OK "VieNeu TTS ready at http://localhost:7860"
            } else {
                Write-Host ""
                Write-Warn "TTS still starting. Check logs:"
                Write-Host "  $logErr"
                Write-Host "  $logOut"
            }
        }
    }

    # --- Start Studio ---
    if (-not $TTSOnly) {
        Write-Info "Starting Studio UI on http://localhost:3000 ..."

        # Check if already running
        try {
            $r = Invoke-WebRequest -Uri "http://127.0.0.1:3000/api/health" -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
            Write-OK "Studio already running at http://localhost:3000"
        } catch {
            $studioPython = Join-Path $STUDIO_DIR "venv\Scripts\python.exe"
            if (-not (Test-Path $studioPython)) {
                Write-Warn "Studio venv not found. Installing..."
                & python -m venv (Join-Path $STUDIO_DIR "venv")
                & (Join-Path $STUDIO_DIR "venv\Scripts\pip.exe") install -q flask requests 2>&1 | Out-Null
            }

            $studioLog = Join-Path $STUDIO_DIR "studio.log"
            # Set env vars before starting (compatible with all PowerShell versions)
            $env:VIENEU_TTS_URL = "http://localhost:7860"
            $env:VIENEU_API_URL = "http://localhost:8000"
            $env:PORT = "3000"
            $proc = Start-Process -FilePath $studioPython `
                -ArgumentList "app.py" `
                -WorkingDirectory $STUDIO_DIR `
                -RedirectStandardOutput $studioLog `
                -RedirectStandardError (Join-Path $STUDIO_DIR "studio.err.log") `
                -PassThru -WindowStyle Hidden

            $proc.Id | Out-File $PIDFILE_STUDIO -Force
            Start-Sleep -Seconds 3

            try {
                $r = Invoke-WebRequest -Uri "http://127.0.0.1:3000/api/health" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
                Write-OK "Studio ready at http://localhost:3000"
            } catch {
                Write-Warn "Studio starting... check $studioLog"
            }
        }
    }

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  Services:" -ForegroundColor Green
    if (-not $StudioOnly) {
        Write-Host "    TTS UI:     http://localhost:7860" -ForegroundColor White
    }
    if (-not $TTSOnly) {
        Write-Host "    Studio:     http://localhost:3000" -ForegroundColor White
    }
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Stop with: .\launcher.ps1 stop" -ForegroundColor Gray
}

# --- Stop Services ---
function Stop-Services {
    Write-Info "Stopping services..."

    if (Test-Path $PIDFILE_TTS) {
        $procId = (Get-Content $PIDFILE_TTS).Trim()
        try {
            Stop-Process -Id $procId -Force -ErrorAction Stop
            Write-OK "TTS stopped (PID: $procId)"
        } catch {
            Write-Warn "TTS process $procId already stopped"
        }
        Remove-Item $PIDFILE_TTS -Force
    }

    if (Test-Path $PIDFILE_STUDIO) {
        $procId = (Get-Content $PIDFILE_STUDIO).Trim()
        try {
            Stop-Process -Id $procId -Force -ErrorAction Stop
            Write-OK "Studio stopped (PID: $procId)"
        } catch {
            Write-Warn "Studio process $procId already stopped"
        }
        Remove-Item $PIDFILE_STUDIO -Force
    }

    # Also kill any remaining python processes on our ports
    $conns = Get-NetTCPConnection -LocalPort 7860,3000 -ErrorAction SilentlyContinue
    foreach ($c in $conns) {
        if ($c.OwningProcess -and $c.State -eq "Listen") {
            try {
                Stop-Process -Id $c.OwningProcess -Force
                Write-OK "Killed process on port $($c.LocalPort)"
            } catch {}
        }
    }

    Write-OK "All services stopped"
}

# --- Status ---
function Get-ServiceStatus {
    Write-Host "Service Status:" -ForegroundColor Cyan
    Write-Host ""

    # TTS
    $ttsStatus = "Stopped"
    $ttsColor = "Red"
    $ttsConn = Get-NetTCPConnection -LocalPort 7860 -State Listen -ErrorAction SilentlyContinue
    if ($ttsConn) {
        $ttsStatus = "Running"
        $ttsColor = "Green"
    } elseif (Test-Path $PIDFILE_TTS) {
        $ttsPid = (Get-Content $PIDFILE_TTS).Trim()
        if (Get-Process -Id $ttsPid -ErrorAction SilentlyContinue) {
            $ttsStatus = "Starting (PID: $ttsPid)"
            $ttsColor = "Yellow"
        }
    }
    Write-Host "  VieNeu TTS (7860): " -NoNewline
    Write-Host $ttsStatus -ForegroundColor $ttsColor

    # Studio
    $studioStatus = "Stopped"
    $studioColor = "Red"
    $studioConn = Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue
    if ($studioConn) {
        $studioStatus = "Running"
        $studioColor = "Green"
    } elseif (Test-Path $PIDFILE_STUDIO) {
        $studioPid = (Get-Content $PIDFILE_STUDIO).Trim()
        if (Get-Process -Id $studioPid -ErrorAction SilentlyContinue) {
            $studioStatus = "Starting (PID: $studioPid)"
            $studioColor = "Yellow"
        }
    }
    Write-Host "  Studio UI  (3000): " -NoNewline
    Write-Host $studioStatus -ForegroundColor $studioColor

    Write-Host ""
}

# --- Main ---
switch ($Action) {
    "start"   { Start-Services }
    "stop"    { Stop-Services }
    "status"  { Get-ServiceStatus }
    "install" { Install-Platform }
    "studio"  { $script:StudioOnly = $true; Start-Services }
}
