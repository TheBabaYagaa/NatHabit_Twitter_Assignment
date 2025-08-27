# Path to your .env file
$envFilePath = "..\..\backend\.env"

# Check if .env exists
if (-Not (Test-Path $envFilePath)) {
    Write-Error " .env file not found at $envFilePath"
    exit 1
}

# Load all variables from .env into current PowerShell session
Get-Content $envFilePath | ForEach-Object {
    if ($_ -match "^\s*([^#][^=]*)=(.*)$") {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        Set-Item -Path "Env:$key" -Value $value
        Write-Host "Loaded $key"
    }
}

Write-Host " All .env variables are now available in your session."
