/*AREA RECREATIVA_CLIMA*/
db.AreaRecreativa.aggregate([
    {
        $lookup: {
            from: "Juegos",
            localField: "NDP",
            foreignField: "NDP",
            as: "juegos"
        }
    },
    {
        $lookup: {
            from: "IncidentesSeguridad",
            localField: "ID",
            foreignField: "AreaRecreativaID",
            as: "incidentes"
        }
    },
    {
        $lookup: {
            from: "RegistroClima",
            localField: "COD_POSTAL",
            foreignField: "COD_POSTAL",
            as: "clima"
        }
    },
    {
        $lookup: {
            from: "EncuestasSatisfaccion",
            localField: "ID",
            foreignField: "AreaRecreativaID",
            as: "encuestas"
        }
    },
    {
        $addFields: {
            juegos: {
                $map: {
                    input: "$juegos",
                    as: "juego",
                    in: {
                        id: "$$juego.ID"
                    }
                }
            },
            incidentes: {
                $map: {
                    input: "$incidentes",
                    as: "incidente",
                    in: {
                        id: "$$incidente.ID",
                        tipoIncidente: "$$incidente.TIPO_INCIDENTE",
                        gravedad: "$$incidente.GRAVEDAD",
                        fechaReporte: "$$incidente.FECHA_REPORTE"
                    }
                }
            },
            clima: {
                $map: {
                    input: "$clima",
                    as: "climaItem",
                    in: {
                        id: "$$climaItem.ID" // ID?
                    }
                }
            },
            encuestas: {
                $map: {
                    input: "$encuestas",
                    as: "encuesta",
                    in: {
                        id: "$$encuesta.ID"
                    }
                }
            }
        }
    },
    {
        $project: {
            nombre: "$ID",
            coordenadasGPS: {
                COORD_GIS_X: "$COORD_GIS_X",
                COORD_GIS_Y: "$COORD_GIS_Y",
                SISTEMA_COORD: "$SISTEMA_COORD",
                LATITUD: "$LATITUD",
                LONGITUD: "$LONGITUD"
            },
            barrio: "$BARRIO",
            distrito: "$DISTRITO",
            fechaInstalacion: "$FECHA_INSTALACION",
            estadoOperativo: "$ESTADO",
            capacidadMax: "$CAPACIDAD_MAX",
            cantidadJuegosPorTipo: "$CANTIDAD_JUEGOS_TIPO",
            juegos: 1, 
            incidentes: 1, 
            clima: 1, 
            encuestas: 1 
        }
    }
])


/*INCIDENCIA*/
db.Incidencia.aggregate([
    $lookup: {
        from: "Usuario",
        localField: "UsuarioID",
        foreignField: "NIF",
        as: "usuarios"
    },
    $addFields: {
        usuarios: {
            input: "$usuarios",
            as: "usuario",
            in: {
                NIF: "$$.usuario.NIF",
                nombre: "$$.usuario.NOMBRE",
                email: "$$.usuario.EMAIL",
                telefono: "$$.usuario.TELEFONO"
            }
        }
    },
    $project: {
        id: "$ID",
        tipoIncidencia: "$TIPO_INCIDENCIA", 
        fechaReporte: "$FECHA_REPORTE",
        estado: "$ESTADO",
        tiempoResolucion: "$TIEMPO_RESOLUCION",
        nivelEscalamiento: "$NIVEL_ESCALAMIENTO",
        usuarios: 1
    }
])

/*JUEGO*/
db.Juegos.aggregate([
    {
        $lookup: {
            from: "Mantenimiento",
            localField: "ID",
            foreignField: "JuegoID",
            as: "mantenimiento"
        }
    },
    {
        $unwind: {
            path: "$mantenimiento",
            preserveNullAndEmptyArrays: true 
        }
    },
    {
        $lookup: {
            from: "Incidencias",
            localField: "mantenimiento.ID", 
            foreignField: "MantenimientoID",
            as: "incidencias"
        }
    },
    {
        $addFields: {
            mantenimiento: {
                $map: {
                    input: ["$mantenimiento"], 
                    as: "mnt",
                    in: {
                        id: "$$mnt.ID"
                    }
                }
            },
            incidencias: {
                $map: {
                    input: "$incidencias", 
                    as: "incidencia",
                    in: {
                        id: "$$incidencia.ID",
                        tipoIncidencia: "$$incidencia.TIPO_INCIDENCIA",
                        fechaReporte: "$$incidencia.FECHA_REPORTE",
                        estado: "$$incidencia.ESTADO"
                    }
                }
            }
        }
    },
    {
        $project: {
            nombre: "$DESC_CLASIFICACION",
            modelo: "$MODELO",
            estadoOperativo: "$ESTADO",
            accesibilidad: "$ACCESIBLE",
            fechaInstalacion: "$FECHA_INSTALACION",
            tipo: "$tipo_juego",
            desgasteAcumulado: "$DESGASTE_ACUMULADO",
            indicadorExposicion: "$INDICADOR_EXPOSICION",
            ultimaFechaMantenimiento: "$ULTIMA_FECHA_MANTENIMIENTO",
            tiempoResolucion: "$TIEMPO_RESOLUCION",
            mantenimiento: { $arrayElemAt: ["$mantenimiento", 0] },
            incidencias: 1
        }
    }
])

