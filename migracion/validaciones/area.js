db.createCollection("area")
db.mantenimiento.createIndex({"ID": 1}, {unique:1})

VAL = {
    bsonType: "object",
    title: "Areas Validator",
    required: ["ID", "DESC_CLASIFICACION", "COD_BARRIO", "BARRIO", "COD_DISTRITO", "DISTRITO", "ESTADO", "DIRECCION_AUX", "SISTEMA_COORD", "CODIGO_INTERNO", "CONTRATO_COD", "TOTAL_ELEM", "tipo", "TIPO_VIA", "NOM_VIA", "NUM_VIA", "COD_POSTAL", "FECHA_INSTALACION"],
    properties: {
            ID: {
                bsonType: "string",
                description: "id del área"
            },
            DESC_CLASIFICACION: {
                bsonType: "string",
                enum: ["area de juegos/especial", "area de mayores", "area infantil", "circuito deportivo elemental"],
                description: "descripción del tipo de área recreativa"
            },
            COD_BARRIO: {
                bsonType: "int",
                description: "código del barrio al que pertenece el área"
            },
            BARRIO: {
                bsonType: "string",
                description: "barrio al que pertenece el área"
            },
            DIRECCION_AUX: {
                bsonType: "string",
                description: "direccion_aux es un string"
            },
            SISTEMA_COORD: {
                bsonType: "string",
                description: "sistema_coord es un string"
            },
            CODIGO_INTERNO: {
                bsonType: "string",
                description: "codigo_interno es un string"
            },
            CONTRATO_COD: {
                bsonType: "string",
                description: "contrato_cod es un string"
            },
            TOTAL_ELEM: {
                bsonType: "int",
                description: "el total de elementos de un area es un int"
            },
            tipo: {
                bsonType: "string",
                enum: ["infantil", "mayores", "deportivas"],
                description: "el tipo de juego tiene que ser uno de esos strings"
            },
            COD_DISTRITO: {
                bsonType: "int",
                description: "código del distrito al que pertenece el área"
            },
            DISTRITO: {
                bsonType: "string",
                description: "distrito al que pertenece el área"
            },
            ESTADO: {
                bsonType: "string",
                enum: ["operativo"],
                description: "estado del área"
            },
            TIPO_VIA: {
                bsonType: "string",
                description: "tipo del vía donde se encuentra el área"
            },
            NOM_VIA: {
                bsonType: "string",
                description: "nombre de la vía donde se encuentra el área"
            },
            NUM_VIA: {
                bsonType: "string",
                description: "número de la vía donde se encuentra el área"
            },
            COD_POSTAL: {
                bsonType: ["string", "double"],
                description: "código postal de la zona postal en la que se encuentra el área"
            },
            FECHA_INSTALACION: {
                bsonType: ["date", "string"],
                description: "fecha en la que se instaló el área"
            }

        }
}




    


db.runCommand({ "collMod": "area", "validator": { $jsonSchema: VAL } })