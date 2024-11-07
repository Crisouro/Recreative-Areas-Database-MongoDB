db.createCollection("mantenimiento")
db.mantenimiento.createIndex({"ID": 1}, {unique:1})

VAL = {
    bsonType: "object",
    description: "Documento que describe al mantenimiento",
    required: ["ID", "FECHA_INTERVENCION", "TIPO_INTERVENCION", "ESTADO_PREVIO", "ESTADO_POSTERIOR", "JuegoID", "Tipo", "Comentarios"],
    properties: {
        ID: {
            bsonType: "string",
            description: "El ID debe ser string y es parte de la PK"
        },
        FECHA_INTERVENCION: {
            bsonType: "date",
            description: "La FECHA_INTERVENCION debe ser tipo date y debe aparecer siempre"
        },
        TIPO_INTERVENCION: {
            bsonType: "string",
            enum: ["correctivo", "emergencia", "preventivo"],
            description: "El TIPO_INTERVENCION debe ser una enumeración"
        },
        ESTADO_PREVIO: {
            bsonType: "string",
            enum: ["malo", "bueno", "regular"],
            description: "El ESTADO_PREVIO debe ser una enumeración"
        },
        ESTADO_POSTERIOR: {
            bsonType: "string",
            enum: ["malo", "bueno", "regular"],
            description: "El ESTADO_POSTERIOR debe ser una enumeración"
        },
        JuegoID: {
            bsonType: "string",
            description: "El JuegoID es un string y debe aparecer siempre."
        },
        Tipo: {
            anyOf: [
                {
                    bsonType: "string",
                    enum: ["preventivo", "correctivo", "queja_usuario"],
                    description: "El Tipo debe ser uno de los valores enumerados"
                },
                {
                    bsonType: "string",
                    description: "CODIGO desconocido",
                    pattern: "^mnt-\\d{5}-Tipo-desconocido$"
                }
            ]
        },
        Comentarios: {
            bsonType: "string",
            description: "Comentarios es un string"
        }
    }
}


db.runCommand({ "collMod": "mantenimiento", "validator": { $jsonSchema: VAL } })