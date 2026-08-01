param(
    [string]$Target = "dev"
)

$ErrorActionPreference = "Stop"

Write-Host "Deploying Databricks bundle for target: $Target"

databricks bundle deploy --target $Target

if ($LASTEXITCODE -ne 0) {
    throw "Databricks bundle deployment failed for target: $Target"
}

Write-Host "Databricks bundle deployment succeeded for target: $Target"
