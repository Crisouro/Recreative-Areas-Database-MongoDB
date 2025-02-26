db.createCollection("incidencias")
db.incidencias.createIndex({ID:1}, {unique: 1})

VAL = {
    bsonType: 'object',
    description: 'Documento que describe a las incidencias',
    required: [
      'ID',
      'TIPO_INCIDENCIA',
      'FECHA_REPORTE',
      'ESTADO',
      'NIVEL_ESCALAMIENTO',
      'TIEMPO_RESOLUCION'
    ],
    properties: {
      ID: {
        bsonType: 'string',
        description: 'El ID debe ser string y es parte de la PK'
      },
      TIPO_INCIDENCIA: {
        bsonType: 'string',
        'enum': [
          'desgaste',
          'rotura',
          'vandalismo',
          'bajo',
          'mal funcionamiento'
        ],
        description: 'El TIPO_INCIDENCIA debe ser una enumeración'
      },
      FECHA_REPORTE: {
        bsonType: 'date',
        description: 'La FECHA_REPORTE debe ser string y debe aparecer siempre'
      },
      ESTADO: {
        bsonType: 'string',
        'enum': [
          'cerrada',
          'abierta'
        ],
        description: 'El TIPO_INCIDENTE es una enumeración'
      },
      NIVEL_ESCALAMIENTO: {
        bsonType: 'string',
        'enum': [
          'muy alto',
          'medio',
          'bajo',
          'alto'
        ],
        description: 'La GRAVEDAD debe ser una enumeración'
      },
      TIEMPO_RESOLUCION: {
        oneOf: [
          {
            bsonType: 'int',
            description: 'El TIEMPO_RESOLUCION debe ser un double'
          },
          {
            bsonType: 'double',
            description: 'El TIEMPO_RESOLUCION debe ser un double'
          },
          {
            bsonType: 'string',
            description: 'CODIGO desconocido',
            pattern: '^\\d+(-(ESTADO-abierta|TIEMPO_RESOLUCION-desconocido))$'
          }
        ]
      },
      UsuarioID: {
        oneOf: [
          {
            bsonType: 'string'
          },
          {
            bsonType: 'array',
            description: 'El UsuarioID debe ser un array de string.',
            items: {
              bsonType: 'string',
              description: 'Cada elemento del array es un string.'
            }
          }
        ]
      },
      MANTENIMIENTO_ID: {
        oneOf: [
          {
            bsonType: 'string'
          },
          {
            bsonType: 'array',
            description: 'El MANTENIMIENTO_ID deber ser un array de strings.',
            items: {
              bsonType: 'string',
              description: 'Cada elemento del array es un string.'
            }
          }
        ]
      }
    }
  }

db.runCommand({ "collMod": "incidencias", "validator": { $jsonSchema: VAL } })