param(
    [string]$Target = "dev"
)

$ErrorActionPreference = "Stop"

Write-Host "Validating Databricks bundle for target: $Target"

databricks bundle validate --target $Target

if ($LASTEXITCODE -ne 0) {
    throw "Databricks bundle validation failed for target: $Target"
}

Write-Host "Databricks bundle validation succeeded for target: $Target"
