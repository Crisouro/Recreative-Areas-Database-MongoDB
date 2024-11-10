db.createCollection("juegos")
db.mantenimiento.createIndex({"ID": 1}, {unique:1})

VAL = {
        bsonType: "object",
        title: "juegos Validator",
        required: ["ID", "DESC_CLASIFICACION", "COD_BARRIO", "BARRIO", "COD_DISTRITO", "DISTRITO", "ESTADO",  "TIPO_VIA", "NOM_VIA", "NUM_VIA", "COD_POSTAL", "DIRECCION_AUX", "FECHA_INSTALACION", "CODIGO_INTERNO", "CONTRATO_COD", "MODELO", "tipo_juego", "ACCESIBLE", "INDICADOR_EXPOSICION", "DESGASTE_ACUMULADO", "SISTEMA_COORD"],
        properties: {
            ID: {
                bsonType: "string",
                description: "id del juego"
            },
            DESC_CLASIFICACION: {
                bsonType: "string",
                enum: ["AREAS DE JUEGO/ESPECIAL", "AREAS DE MAYORES", "AREAS INFANTIL", "CIRCUITO DEPORTIVO ELEMENTAL"],
                description: "descripción del tipo de juego recreativa"
            },
            COD_BARRIO: {
                bsonType: "int",
                description: "código del barrio al que pertenece el juego"
            },
            BARRIO: {
                bsonType: "string",
                description: "barrio al que pertenece el juego"
            },
            COD_DISTRITO: {
                bsonType: "int",
                description: "código del distrito al que pertenece el juego"
            },
            DISTRITO: {
                bsonType: "string",
                description: "distrito al que pertenece el juego"
            },
            ESTADO: {
                bsonType: "string",
                enum: ["OPERATIVO"],
                description: "estado del juego"
            },
            TIPO_VIA: {
                bsonType: "string",
                description: "tipo del vía donde se encuentra el juego"
            },
            NOM_VIA: {
                bsonType: "string",
                description: "nombre de la vía donde se encuentra el juego"
            },
            NUM_VIA: {
                bsonType: "string",
                description: "número de la vía donde se encuentra el juego"
            },
            COD_POSTAL: {
                bsonType: "string",
                description: "código postal de la zona postal en la que se encuentra el juego"
            },
            DIRECCION_AUX: {
                bsonType: "string",
                description: "direccion_aux es un stirng"
            },
            FECHA_INSTALACION: {
                bsonType: ["string", "date"],
                description: "fecha en la que se instaló el juego"
            },
            CODIGO_INTERNO: {
                bsonType: "string",
                description: "codigo_interno es un string"
            },
            CONTRATO_COD: {
                bsonType: "string",
                description: "cond_contrato es un string"
            },
            MODELO: {
                bsonType: "string",
                description: "modelo de juego"
            },
            tipo_juego: {
                bsonType: "string",
                enum: ["deportivas", "infantiles", "mayores"],
                description: "tipo de juego"
            },
            ACCESIBLE: {
                bsonType: "bool",
                description: "indica si el juego es accesible"
            },
            INDICADOR_EXPOSICION: {
                bsonType: "string",
                enum: ["alto", "medio", "bajo"],
                description: "indicador_exposicion solo puede ser uno de esos strings"
            },
            SISTEMA_COORD: {
                bsonType: "string",
                description: "sistema_coord es un string"
            },
            DESGASTE_ACUMULADO: {
                bsonType: "int",
                description: "desgaste acumulado es un int"
            }
        }
}

db.runCommand({ "collMod": "juegos", "validator": { $jsonSchema: VAL } })