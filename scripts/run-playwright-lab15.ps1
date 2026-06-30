$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$backendDir = Join-Path $root "server_smartcity"
$logsDir = Join-Path $root "lab15_deliverables"

New-Item -ItemType Directory -Force -Path $logsDir | Out-Null

function Wait-Url {
    param(
        [string] $Url,
        [int] $TimeoutSeconds = 60
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    do {
        try {
            Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 3 | Out-Null
            return
        } catch {
            Start-Sleep -Seconds 1
        }
    } while ((Get-Date) -lt $deadline)

    throw "Server belum siap: $Url"
}

Write-Host "Menjalankan server backend Django di http://127.0.0.1:8000 ..."
$backend = Start-Process -WindowStyle Hidden -FilePath "python" `
    -ArgumentList @("manage.py", "runserver", "127.0.0.1:8000", "--noreload") `
    -WorkingDirectory $backendDir `
    -RedirectStandardOutput (Join-Path $logsDir "backend_server.log") `
    -RedirectStandardError (Join-Path $logsDir "backend_server.err") `
    -PassThru

Write-Host "Menjalankan server frontend SPA di http://127.0.0.1:5500 ..."
$frontend = Start-Process -WindowStyle Hidden -FilePath "python" `
    -ArgumentList @("-m", "http.server", "5500", "--bind", "127.0.0.1") `
    -WorkingDirectory $root `
    -RedirectStandardOutput (Join-Path $logsDir "frontend_server.log") `
    -RedirectStandardError (Join-Path $logsDir "frontend_server.err") `
    -PassThru

try {
    Wait-Url "http://127.0.0.1:8000/accounts/login/" 90
    Wait-Url "http://127.0.0.1:5500/smartcity_citizen_spa_24782087/index.html" 30

    Write-Host ""
    Write-Host "Running Playwright tests..."
    npx playwright test
    exit $LASTEXITCODE
} finally {
    if ($backend -and -not $backend.HasExited) {
        Stop-Process -Id $backend.Id -Force
    }
    if ($frontend -and -not $frontend.HasExited) {
        Stop-Process -Id $frontend.Id -Force
    }
}
