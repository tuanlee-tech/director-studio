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
Write-Host "🔍 Kiểm tra VieNeu-TTS tại $ApiUrl ..." -ForegroundColor Cyan
try {
    $null = Invoke-RestMethod -Uri "$ApiUrl/health" -TimeoutSec 5 -Method GET
    Write-Host "✅ VieNeu-TTS đang online." -ForegroundColor Green
} catch {
    Write-Host "❌ VieNeu-TTS không chạy tại $ApiUrl" -ForegroundColor Red
    Write-Host "   → Hãy chạy '@start-tts' hoặc '.\launcher.ps1 start'" -ForegroundColor Yellow
    exit 1
}

# --- Gọi TTS API ---
Write-Host "🎙️  Đang tạo audio | Voice: $Voice | Chars: $($Text.Length)" -ForegroundColor Cyan
$body = @{
    model           = "vieneu-tts-v3-turbo"
    input           = $Text
    voice           = $Voice
    response_format = "wav"
} | ConvertTo-Json -Compress

try {
    $response = Invoke-WebRequest `
        -Uri "$ApiUrl/v1/audio/speech" `
        -Method POST `
        -Body $body `
        -ContentType "application/json; charset=utf-8" `
        -TimeoutSec 120

    [System.IO.File]::WriteAllBytes($OutputPath, $response.Content)

    $sizeKB = [math]::Round($response.Content.Length / 1024, 1)
    Write-Host "✅ Audio saved: $OutputPath ($sizeKB KB)" -ForegroundColor Green
} catch {
    Write-Host "❌ Lỗi gọi API: $_" -ForegroundColor Red
    exit 1
}
