
db.createCollection('meteo')
db.meteo.createIndex({ID: 1}, {unique: 1})

VAL = {
    bsonType: "object",
    description: "Documento que describe la meteorología",
    required: ["ID", "PROVINCIA", "MUNICIPIO", "ESTACION", "COD_POSTAL", "FECHA", "TEMPERATURA", "PRECIPITACION", "VIENTO_FUERTE"],
    properties: {
        ID: {
            bsonType: "string",
            description: "El ID debe ser string y es PK"
        },
        PROVINCIA: {
            bsonType: "int",
            description: "La PROVINCIA debe ser un entero"
        },
        MUNICIPIO: {
            bsonType: "int",
            description: "El MUNICIPIO debe ser un entero"
        },
        ESTACION: {
            bsonType: "int",
            description: "La ESTACION debe ser un entero"
        },
        COD_POSTAL: {
            bsonType: "array",
            description: "El COD_POSTAL debe ser una lista de enteros",
            items: {
                bsonType: "int",
                description: "Cada valor de la lista debe ser un entero"
            }
        },
        FECHA: {
            bsonType: "date",
            description: "FECHA debe ser un date y aparecer siempre"
        },
        TEMPERATURA: {
            oneOf: [
                {
                    bsonType: "double",
                    description: "TEMPERATURA debe ser un double y aparecer siempre"
                },
                { 
                    bsonType: "string", 
                    description: "CODIGO desconocido",
                    pattern: "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}\\.\\d{6}Z_\\d+_\\d+_\\d+-TEMPERATURA-desconocido$"
                }
            ]
        },
        PRECIPITACION: {
            oneOf: [
                {
                    bsonType: "double",
                    description: "PRECIPITACION debe ser un double y aparecer siempre"
                },
                { 
                    bsonType: "string", 
                    description: "CODIGO desconocido",
                    pattern: "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}\\.\\d{6}Z_\\d+_\\d+_\\d+-PRECIPITACION-desconocido$"
                }
            ]
        },
        VIENTO_FUERTE: {
            oneOf: [
                {
                    bsonType: "bool",
                    description: "VIENTO_FUERTE debe ser un booleano y aparecer siempre"
                },
                { 
                    bsonType: "string", 
                    description: "CODIGO desconocido",
                    pattern: "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}\\.\\d{6}Z_\\d+_\\d+_\\d+-VIENTO_FUERTE-desconocido$"
                }
            ]
        }
    }
}

db.runCommand({ "collMod": "meteo", "validator": { $jsonSchema: VAL } })