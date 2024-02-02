 if [ $(curl -LI http://localhost:8000/api/schema -o /dev/null -w '%{http_code}\n' -s) != "200" ]; then echo "Swagger not reachable. Please ensure backend is running on localhost:9000" ;exit; fi
rm -rf projects/swagger-client/src/*;

openapi-generator-cli generate -i  http://localhost:8000/api/schema  -g typescript-angular -o projects/swagger-client/src --additional-properties ngVersion=16.2.11,serviceSuffix=API,serviceFileSuffix=api.service,basePath=''

# Build the lib
ng build swagger-client

sleep .5

# install the freshly built lib
npm install -f ./dist/swagger-client

# run prettier to retablish lib syntax
npx pretty-quick --pattern "projects/swagger-client/src/**/*.ts"