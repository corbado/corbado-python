#!/bin/sh
GENERATED_PACKAGE_NAME="generated"

echo "Generating OpenAPI code ..."

cd "$(dirname "$0")"
rm -rf .gen
mkdir -p .gen
cd .gen
rm -rf ../../src/corbado_python_sdk/$GENERATED_PACKAGE_NAME
mkdir -p ../../src/corbado_python_sdk/$GENERATED_PACKAGE_NAME

curl -s -O https://api.corbado.com/docs/api/openapi/backend_api_public.yml
docker pull openapitools/openapi-generator-cli
docker run -v ${PWD}:/local --user $(id -u):$(id -g) openapitools/openapi-generator-cli generate -i /local/backend_api_public.yml -g python -o /local --additional-properties=packageName=$GENERATED_PACKAGE_NAME,projectName=corbado-python
#pip install .

cp -r $GENERATED_PACKAGE_NAME/* ../../src/corbado_python_sdk/$GENERATED_PACKAGE_NAME
cp -r requirements.txt ../../src/corbado_python_sdk/$GENERATED_PACKAGE_NAME

cd ..
rm -rf .gen

echo " done!"