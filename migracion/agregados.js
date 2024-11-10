/*AREA RECREATIVA_CLIMA*/
db.area.aggregate([
    {
        $lookup: {
            from: "juegos",
            localField: "NDP",
            foreignField: "NDP",
            as: "ref_juegos"
        }
    },
    {
        $lookup: {
            from: "incidentes",
            localField: "ID",
            foreignField: "AreaRecreativaID",
            as: "ref_incidentes"
        }
    },
    {
        $lookup: {
            from: "meteo",
            localField: "COD_POSTAL",
            foreignField: "COD_POSTAL",
            as: "ref_meteo"
        }
    },
    {
        $lookup: {
            from: "encuestas",
            localField: "ID",
            foreignField: "AreaRecreativaID",
            as: "ref_encuestas"
        }
    },
    {
        $addFields: {
            JUEGOS: {
                $map: {
                    input: "$ref_juegos",
                    as: "juego",
                    in: {
                        _id: "$$juego._id"
                    }
                }
            },
            INCIDENTES_SEGURIDAD: {
                $map: {
                    input: "$ref_incidentes",
                    as: "incidente",
                    in: {
                        _id: "$$incidente._id",
                        TIPO_INCIDENTE: "$$incidente.TIPO_INCIDENTE",
                        GRAVEDAD: "$$incidente.GRAVEDAD",
                        FECHA_REPORTE: "$$incidente.FECHA_REPORTE"
                    }
                }
            },
            CLIMA: {
                $map: {
                    input: "$ref_meteo",
                    as: "meteo",
                    in: {
                        _id: "$$meteo._id"
                    }
                }
            },
            ENCUESTAS: {
                $map: {
                    input: "$ref_encuestas",
                    as: "encuesta",
                    in: {
                        _id: "$$encuesta._id"
                    }
                }
            }
        }
    },
    {
        $project: {
            NOMBRE: "$ID",
            UBICACION: {
                COD_BARRIO: 1,
                BARRIO: 1,
                COD_DISTRITO: 1, 
                DISTRITO: 1,
                TIPO_VIA: 1,
                NOM_VIA: 1, 
                NUM_VIA: 1,
                COD_POSTAL: 1,
                DIRECCION_AUX: 1,
                COORD_GIS: 1,
                SISTEMA_COORD: 1,
                NDP: 1
            },
            FECHA_INSTALACION: 1,
            ESTADO_GLOBAL_AREA: "$ESTADO_GLOBAL",
            ESTADO_OPERATIVO: "$ESTADO",
            CAPACIDAD_MAX: 1,
            CANTIDAD_JUEGOS_TIPO: 1,
            JUEGOS: 1, 
            INCIDENTES_SEGURIDAD: 1, 
            CLIMA: 1, 
            ENCUESTAS: 1 
        }
    },
    {
        $out: {db:"entregable", coll: "area-agregado"} 
    }
])


/*INCIDENCIA*/

db.incidencias.aggregate([
    {
        $lookup: {
            from: "usuarios",
            localField: "UsuarioID",
            foreignField: "NIF",
            as: "ref_usuarios"
        }
    },
    {
        $addFields: {
            usuarios: {
                $map: {
                    input: "$ref_usuarios",
                    as: "usuario",
                    in: {
                        _id: "$$usuario._id",
                        nombre: "$$usuario.NOMBRE",
                        email: "$$usuario.EMAIL",
                        telefono: "$$usuario.TELEFONO"
                    }
                }
            }
        }
    },
    {
        $project: {
            TIPO_INCIDENCIA: 1, 
            FECHA_REPORTE: 1,
            estado: 1,
            TIEMPO_RESOLUCION: 1,
            NIVEL_ESCALAMIENTO: 1,
            usuarios: 1
        }
    },
    {
        $out: {db:"entregable", coll: "incidencias-agregado"} 
    }
])

/*JUEGO*/
db.juegos.aggregate([
    {
        $lookup: {
            from: "mantenimiento",
            localField: "ID",
            foreignField: "JuegoID",
            as: "ref_mantenimiento"
        }
    },
    {
        $lookup: {
            from: "incidencias",
            localField: "ref_mantenimiento.ID", 
            foreignField: "MANTENIMIENTO_ID",
            as: "ref_incidencias"
        }
    },
    {
        $addFields: {
            MANTENIMIENTO: {
                $map: {
                    input: "$ref_mantenimiento", 
                    as: "mnt",
                    in: {
                        _id: "$$mnt._id",
                        TIPO_MANTENIMIENTO: "$$mnt.TIPO_MANTENIMIENTO", 
                        FECHA_MANTENIMIENTO: "$$mnt.FECHA_MANTENIMIENTO"  
                    }
                }
            },
            INCIDENCIAS: {
                $map: {
                    input: "$ref_incidencias", 
                    as: "incidencia",
                    in: {
                        _id: "$$incidencia._id",
                        TIPO_INCIDDENCIA: "$$incidencia.TIPO_INCIDENCIA",
                        FECHA_REPORTE: "$$incidencia.FECHA_REPORTE",
                        ESTADO: "$$incidencia.ESTADO"
                    }
                }
            },
            TIEMPO_RESOLUCION: {
                $map: {
                    input: "$ref_incidencias",
                    as: "incidencia",
                    in: "$$incidencia.TIEMPO_RESOLUCION"
                }
            }
        }
    },
    {
        $project: {
            NOMBRE: "$DESC_CLASIFICACION",
            MODELO: 1,
            ESTADO_OPERATIVO: "$ESTADO",
            ACCESIBILIDAD: "$ACCESIBLE",
            FECHA_INSTALACION: 1,
            TIPO: "$tipo_juego",
            DESGASTE_ACUMULADO: 1,
            INDICADOR_EXPOSICION: 1,
            ULTIMA_FECHA_MANTENIMIENTO: "$ULTIMA_FECHA_MANTENIMIENTO",
            TIEMPO_RESOLUCION: 1,
            MANTENIMIENTO: 1, 
            INCIDENCIAS: 1
        }
    },
    {
        $out: { db: "entregable", coll: "juegos-agregado" }
    }
]);



