db.createCollection("area")
db.mantenimiento.createIndex({"ID": 1}, {unique:1})

VAL = {
    
}

db.runCommand({ "collMod": "area", "validator": { $jsonSchema: VAL } })