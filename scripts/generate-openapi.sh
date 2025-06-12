#!/bin/sh
GENERATED_PACKAGE_NAME="generated" #subpackage of corbado_python_sdk
SDK_PACKAGE_NAME="corbado_python_sdk"
GENERATED_PROJECT_NAME="corbado-python-generated"
echo "Generating OpenAPI code ..."

cd "$(dirname "$0")"
cp backend_api_public_v2.yml .gen/backend_api_public_v2.yml
#rm -rf .gen
mkdir -p .gen
cd .gen
rm -rf ../../src/$SDK_PACKAGE_NAME/$GENERATED_PACKAGE_NAME
mkdir -p ../../src/$SDK_PACKAGE_NAME/$GENERATED_PACKAGE_NAME


curl -s https://backendapi.cloud.corbado.io/v2/openapi.yaml -o backend_api_public_v2.yml
docker run -v ${PWD}:/local --user $(id -u):$(id -g) openapitools/openapi-generator-cli generate -i /local/backend_api_public_v2.yml -g python -o /local --additional-properties=packageName=$SDK_PACKAGE_NAME.$GENERATED_PACKAGE_NAME,projectName=$GENERATED_PROJECT_NAME

cp -r $SDK_PACKAGE_NAME/$GENERATED_PACKAGE_NAME/* ../../src/$SDK_PACKAGE_NAME/$GENERATED_PACKAGE_NAME
cp -r requirements.txt ../../src/$SDK_PACKAGE_NAME/$GENERATED_PACKAGE_NAME
cd ..
rm -rf .gen

echo " done!"