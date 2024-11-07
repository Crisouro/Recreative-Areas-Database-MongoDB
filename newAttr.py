import pandas as pd
import random
import numpy as np
from datetime import datetime


def nivelEscalamiento(df):
    """Function that generates nivelEscalamiento value for df."""
    enum = {"desgaste": "muy alto", "rotura": "medio", "vandalismo": "bajo", "mal funcionamiento": "alto"}
    for key, value in enum.items():
        df.loc[df["TIPO_INCIDENCIA"] == key, "NIVEL_ESCALAMIENTO"] = value

def indicadorExposicion(df):
    """Function that generates indicadorExposicion value for df"""
    df["INDICADOR_EXPOSICION"] = np.random.choice(["bajo", "medio", "alto"], size=df.shape[0])

def tiempoResolucion(incidencias, mantenimiento) -> dict:
    """This function generates tiempoResolucion for each incidence"""
    #Manteinance IDs formetting
    man_list = incidencias["MantenimientoID"].str.strip("[]").str.replace("mnt-", "").str.split(", ")
    print(man_list, len(man_list), type(man_list))

    for i in range(len(incidencias)):
        if incidencias.at[i, "ESTADO"] == "cerrada":
            #Obtaining manteinances associated to each incidence, extrating their dates
            int_man_list = [int(item.replace("'", "")) for item in man_list[i]]
            dates = mantenimiento.loc[mantenimiento.index.isin(int_man_list), "FECHA_INTERVENCION"]
            #If manteinances are founded, tiempoResolucion will be the difference between the report time and the latest manteinance operation
            ini_date = datetime.strptime(incidencias.at[i, "FECHA_REPORTE"], "%Y-%m-%dT%H:%M:%S.%fZ")
            if not dates.empty:
                end_date = datetime.strptime(max(dates), "%Y-%m-%dT%H:%M:%S.%fZ")
                incidencias.at[i, "TIEMPO_RESOLUCION"] = (abs(end_date - ini_date))
            else:
                incidencias.at[i, "TIEMPO_RESOLUCION"] = str(incidencias.at[i, "ID"]) + "-TIEMPO_RESOLUCION-desconocido"
        else:
            incidencias.at[i, "TIEMPO_RESOLUCION"] = str(incidencias.at[i, "ID"]) + "-ESTADO-abierta"

def capacidadMax(df):
    "Function that generates capacidadMax value for df"
    pass

def desgasteAcumulado(juegos, mantenimientos):
    """Function that generate the atribute Desgaste Acumulado (int) for Juegos"""
    #Desgaste Acumulado will correspond to the number of performed manteinance of each game
    for i in range(len(juegos)):
        juegos.at[i, "DESGASTE_ACUMULADO"] = len(mantenimientos.loc[mantenimientos["JuegoID"] == juegos.at[i, "ID"]])
