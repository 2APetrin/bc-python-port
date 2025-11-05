#!/bin/bash

# См. https://cyclonedx-bom-tool.readthedocs.io/en/latest/usage.html
echo "Generating Python SBOM..."
cyclonedx-py requirements -o sbom-python.json

# Сгенерировать SBOM для Java с помощью maven
echo "Generating Java SBOM..." 
mvn cyclonedx:makeAggregateBom > /dev/null

# Соединить два SBOM в один общий
if [[ -e "cyclonedx-linux-x64" ]]; then
  CYCLONEDX_CMD='./cyclonedx-linux-x64'
else 
  # Тут короче нужна обработка винды
  echo "Error: appropriate cyclonedx-cli not found! Exiting..."
  exit 1
fi

echo "Merging SBOMs..."
$CYCLONEDX_CMD merge \
  --input-files "./sbom-python.json" \
  --input-files "./target/sbom-java.json" \
  --output-file ./sbom.json

echo "Validating SBOM..."
$CYCLONEDX_CMD validate --input-file sbom.json