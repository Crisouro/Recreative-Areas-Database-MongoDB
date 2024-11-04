unzip old-datasets.zip
mongorestore mongodb://localhost/areas-recreativas areas-recreativas/
mongosh --file migracion.js localhost/areas-recreativas