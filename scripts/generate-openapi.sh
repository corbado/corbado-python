#!/bin/sh
PACKAGE_NAME="python_generate"

echo "Generating OpenAPI code ..."

cd "$(dirname "$0")"
rm -rf .gen
mkdir -p .gen
cd .gen

curl -s -O https://api.corbado.com/docs/api/openapi/backend_api_public.yml
docker pull openapitools/openapi-generator-cli
docker run -v ${PWD}:/local --user $(id -u):$(id -g) openapitools/openapi-generator-cli generate -i /local/backend_api_public.yml -g python -o /local --additional-properties=packageName=$PACKAGE_NAME,invokerPackage=Corbado\\Generated
cp -r $PACKAGE_NAME/* ../../src/Generated
cp -r requirements.txt ../../src/Generated

cd ..
rm -rf .gen

echo " done!"