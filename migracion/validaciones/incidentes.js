db.createCollection("incidentes")
db.incidentes.createIndex({ID:1}, {unique: 1})

VAL = {
    bsonType: "object",
    description: "Documento que describe a los incidentes",
    required: ["ID", "FECHA_REPORTE", "TIPO_INCIDENTE", "GRAVEDAD", "AreaRecreativaID"],
    properties: {
        ID: {
            bsonType: "string",
            description: "El ID debe ser string y es parte de la PK"
        },
        FECHA_REPORTE: {
            bsonType: "date",
            description: "La FECHA_REPORTE debe ser string y debe aparecer siempre"
        },
        TIPO_INCIDENTE: {
            bsonType: "string",
            enum: ["robo", "caida", "accidente", "vandalismo", "dano estructural"],
            description: "El TIPO_INCIDENTE es una enumeración"
        },
        GRAVEDAD: {
            bsonType: "string",
            enum: ["alta", "baja", "critica", "media"],
            description: "La GRAVEDAD debe ser una enumeración",
        },
        AreaRecreativaID: {
            bsonType: "string",
            description: "El AreaReacreativaID debe ser un string"
        }
    }
}

db.runCommand({ "collMod": "incidentes", "validator": { $jsonSchema: VAL } })