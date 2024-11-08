db.createCollection("juegos")
db.mantenimiento.createIndex({"ID": 1}, {unique:1})

VAL = {
    
}

db.runCommand({ "collMod": "juegos", "validator": { $jsonSchema: VAL } })