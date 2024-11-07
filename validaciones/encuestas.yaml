db.createCollection('encuestas')
db.meteo.createIndex({ID: 1}, {unique: 1})

VAL = {
    bsonType: "object",
    description: "Documento que describe la meteorología",
    required: ["ID", "PUNTUACION_ACCESIBILIDAD", "PUNTUACION_CALIDAD", "COMENTARIOS", "AreaRecreativaID", "FECHA"],
    properties: {
        ID: {
            bsonType: "string",
            description: "El ID debe ser string y es PK"
        },
        PUNTUACION_ACCESIBILIDAD: {
            bsonType: "int",
            description: "PUNTUACION_ACCESIBILIDAD debe ser un entero"
        },
        PUNTUACION_CALIDAD: {
            bsonType: "int",
            description: "PUNTUACION_CALIDAD debe ser un entero"
        },
        COMENTARIOS: {
            bsonType: "string",
            description: "COMENTARIOS debe ser un string"
        },
        AreaRecreativaID: {
            bsonType: "string",
            description: "El AreaRecreativaID debe ser una lista de enteros",
        },
        FECHA: {
            bsonType: "date",
            description: "FECHA debe ser un date y aparecer siempre"
        }
    }
}

db.runCommand({ "collMod": "encuestas", "validator": { $jsonSchema: VAL } })