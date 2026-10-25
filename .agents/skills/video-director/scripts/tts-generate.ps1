<#
.SYNOPSIS
    Tạo TTS audio cho 1 scene qua VieNeu-TTS OpenAI-compatible API.
    Sử dụng từ cheatcode @gen-audio.

.PARAMETER Text
    Nội dung văn bản cần đọc.

.PARAMETER Voice
    Tên giọng đọc. Mặc định: "Hải Đăng"

.PARAMETER OutputPath
    Đường dẫn file audio đầu ra (.wav).

.PARAMETER ApiUrl
    URL của VieNeu-TTS API. Mặc định: http://localhost:8000

.PARAMETER Scene
    Số scene (dùng để tự động đặt tên OutputPath nếu không chỉ định).

.PARAMETER VideoDir
    Thư mục video (dùng cùng với -Scene để tự động tạo đường dẫn).

.EXAMPLE
    .\tts-generate.ps1 -Text "Xin chào thế giới." -Scene 1 -VideoDir "channels/my-channel/videos/my-video"
    .\tts-generate.ps1 -Text "Hello world" -Voice "Binh" -OutputPath "audio/S001_narration.wav"
#>
param(
    [Parameter(Mandatory=$true)][string]$Text,
    [string]$Voice = "Hải Đăng",
    [string]$OutputPath = "",
    [string]$ApiUrl = "http://localhost:8000",
    [int]$Scene = 0,
    [string]$VideoDir = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# --- Resolve output path ---
if (-not $OutputPath) {
    if ($Scene -gt 0 -and $VideoDir) {
        $sceneStr = $Scene.ToString("D3")
        $audioDir = Join-Path $VideoDir "audio"
        if (-not (Test-Path $audioDir)) { New-Item -ItemType Directory -Path $audioDir -Force | Out-Null }
        $OutputPath = Join-Path $audioDir "S${sceneStr}_narration.wav"
    } else {
        Write-Error "Cần chỉ định -OutputPath hoặc cả -Scene và -VideoDir."
        exit 1
    }
}

# --- Health check ---
Write-Host "[INFO] Kiem tra VieNeu-TTS tai $ApiUrl ..." -ForegroundColor Cyan
try {
    $null = Invoke-RestMethod -Uri "$ApiUrl/health" -TimeoutSec 5 -Method GET
    Write-Host "[OK] VieNeu-TTS online." -ForegroundColor Green
} catch {
    Write-Host "[ERR] VieNeu-TTS khong chay tai $ApiUrl" -ForegroundColor Red
    Write-Host "   -> Hay chay '@start-tts' hoac '.\launcher.ps1 start'" -ForegroundColor Yellow
    exit 1
}

# --- Goi TTS API ---
$charLen = $Text.Length
Write-Host "[INFO] Dang tao audio | Voice: $Voice | Chars: $charLen" -ForegroundColor Cyan
$body = @{
    model           = "vieneu-tts-v3-turbo"
    input           = $Text
    voice           = $Voice
    response_format = "wav"
} | ConvertTo-Json -Compress

try {
    $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($body)
    Invoke-WebRequest `
        -Uri "$ApiUrl/v1/audio/speech" `
        -Method POST `
        -Body $bodyBytes `
        -ContentType "application/json; charset=utf-8" `
        -UseBasicParsing `
        -OutFile $OutputPath `
        -TimeoutSec 120

    $sizeKB = [math]::Round((Get-Item $OutputPath).Length / 1024, 1)
    Write-Host "[OK] Audio saved: $OutputPath ($sizeKB KB)" -ForegroundColor Green
} catch {
    Write-Host "[ERR] Loi goi API: $_" -ForegroundColor Red
    exit 1
}
