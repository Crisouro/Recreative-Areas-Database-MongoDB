db.createCollection('usuarios')
db.usuarios.createIndex({NIF: 1}, {unique: 1})

VAL = { 
    "bsonType": "object",
    "description": "Documento que describe a los usuarios",
    "required": [
      "NIF",
      "NOMBRE",
      "EMAIL"
    ],
    "properties": {
      "NIF": {
        "bsonType": "string",
        "description": "El ID debe ser string y es parte de la PK"
      },
      "NOMBRE": {
        "bsonType": "string",
        "description": "El NOMBRE debe ser string y debe aparecer siempre"
      },
      "EMAIL": {
        "oneOf": [
          { "bsonType": "string" },
          {
            "bsonType": "array",
            "items": { "bsonType": "string" }
          }
        ]
      },
      "TELEFONO": {
        "oneOf": [
          { "bsonType": "string", "description": "El TELEFONO debe ser un array de string o un string único" },
          {
            "bsonType": "array",
            "items": { "bsonType": "string" }
          }
        ]
      }
    }
}

db.runCommand({ "collMod": "usuarios", "validator": { $jsonSchema: VAL } })

