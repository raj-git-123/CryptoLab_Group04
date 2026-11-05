$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DataDir = Join-Path $ScriptDir "data"

New-Item -ItemType Directory -Force -Path $DataDir | Out-Null

$Bytes = New-Object byte[] 1048576

$Rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
$Rng.GetBytes($Bytes)

$OutputPath = Join-Path $DataDir "windows_cng.bin"
[System.IO.File]::WriteAllBytes($OutputPath, $Bytes)

$Rng.Dispose()

Write-Output "Windows CNG dataset generated."
