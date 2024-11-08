db.incidencias.updateMany(
    {
      "UsuarioID": { $type: "string" },
      "MANTENIMIENTO_ID": { $type: "string" }
    },
    [
      {
        $set: {
          UsuarioID: {
            $cond: {
              if: { $eq: [{ $type: "$UsuarioID" }, "string"] },
              then: {
                $map: {
                  input: {
                    $split: [
                      {
                        $replaceAll: {
                          input: { $substrBytes: ["$UsuarioID", 1, { $subtract: [{ $strLenBytes: "$UsuarioID" }, 2] }] },
                          find: "'",
                          replacement: ""
                        }
                      },
                      ","
                    ]
                  },
                  as: "usuario",
                  in: { $trim: { input: "$$usuario" } }
                }
              },
              else: "$UsuarioID"
            }
          },
          MANTENIMIENTO_ID: {
            $cond: {
              if: { $eq: [{ $type: "$MANTENIMIENTO_ID" }, "string"] },
              then: {
                $map: {
                  input: {
                    $split: [
                      {
                        $replaceAll: {
                          input: { $substrBytes: ["$MANTENIMIENTO_ID", 1, { $subtract: [{ $strLenBytes: "$MANTENIMIENTO_ID" }, 2] }] },
                          find: "'",
                          replacement: ""
                        }
                      },
                      ","
                    ]
                  },
                  as: "mantenimiento",
                  in: { $trim: { input: "$$mantenimiento" } }
                }
              },
              else: "$MANTENIMIENTO_ID"
            }
          }
        }
      }
    ]
  );
  
db.usuarios.updateMany(
  {
    "EMAIL": { $type: "string" },
    "TELEFONO": { $type: "string" }
  },
  [
    {
      $set: {
        EMAIL: {
          $cond: {
            if: { $eq: [{ $type: "$EMAIL" }, "string"] },
            then: {
              $map: {
                input: {
                  $split: [
                    {
                      $replaceAll: {
                        input: { $substrBytes: ["$EMAIL", 1, { $subtract: [{ $strLenBytes: "$EMAIL" }, 2] }] },
                        find: "'",
                        replacement: ""
                      }
                    },
                    ","
                  ]
                },
                as: "email",
                in: { $trim: { input: "$$email" } }
              }
            },
            else: "$EMAIL"
          }
        },
        TELEFONO: {
          $cond: {
            if: { $eq: [{ $type: "$TELEFONO" }, "string"] },
            then: {
              $map: {
                input: {
                  $split: [
                    {
                      $replaceAll: {
                        input: { $substrBytes: ["$TELEFONO", 1, { $subtract: [{ $strLenBytes: "$TELEFONO" }, 2] }] },
                        find: "'",
                        replacement: ""
                      }
                    },
                    ","
                  ]
                },
                as: "telefono",
                in: { $trim: { input: "$$telefono" } }
              }
            },
            else: "$TELEFONO"
          }
        }
      }
    }
  ]
);
