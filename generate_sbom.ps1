# См. https://cyclonedx-bom-tool.readthedocs.io/en/latest/usage.html
Write-Output "Generating Python SBOM..."
cyclonedx-py requirements -o sbom-python.json

# Сгенерировать SBOM для Java с помощью maven
Write-Output "Generating Java SBOM..." 
mvn cyclonedx:makeAggregateBom *> $nul

# Соединить два SBOM в один общий
Write-Output "Merging SBOMs..."
$CYCLONEDX_CMD = $null
if (Test-Path "cyclonedx-win-x64.exe") {
    $CYCLONEDX_CMD = ".\cyclonedx-win-x64.exe"
} elseif (Test-Path "cyclonedx-win-x86.exe ") {
    $CYCLONEDX_CMD = ".\cyclonedx-win-x86.exe"
} elseif (Test-Path "cyclonedx-win-arm64.exe") {
    $CYCLONEDX_CMD = ".\cyclonedx-win-arm64.exe"
} else {
    Write-Error "Error: failed merging SBOMs, appropriate cyclonedx-cli not found! Please consult the user manual (README)."
    Write-Error "Exiting..."
    exit 1
}

& $CYCLONEDX_CMD merge --input-files ".\sbom-python.json" --input-files ".\target\sbom-java.json" --output-file "./sbom.json"

Write-Output "Validating SBOM..."
& $CYCLONEDX_CMD validate --input-file sbom.json