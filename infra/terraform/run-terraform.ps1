# Load .env from backend folder
Get-Content "..\..\backend\.env" | ForEach-Object {
    if ($_ -match "^\s*([^#][^=]+)=(.+)$") {
        Set-Item -Path "Env:$($matches[1])" -Value "$($matches[2])"
    }
}

# Run Terraform
terraform apply
