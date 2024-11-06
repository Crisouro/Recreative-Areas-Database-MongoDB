
import json
import os
import pandas as pd
import formatting as fr
from generalAnalysis import general_analysis
import cleaningFunctions as cf
import newAttr as new

area = pd.read_csv(os.path.join("cleaned", "AreasLimpio.csv"), sep=',')

copy_area = area.copy()
copy_area["NDP"] = pd.to_numeric(area["NDP"], errors='coerce')

juegos = pd.read_csv(os.path.join("cleaned", "JuegosLimpio.csv"), sep=',')
incidentes = pd.read_csv(os.path.join("cleaned", "IncidentesLimpio.csv"), sep=',')

def estadoGlobalArea(row, filtered_juegos):
    mnt_juegos = filtered_juegos[filtered_juegos["ESTADO"] != "operativo"]

    inc_area = incidentes[incidentes["AreaRecreativaID"] == row["ID"]] 

    #CASO EXCEPCIONAL:
    def check_estado(row):
        if "dano estructural" in str(row["TIPO_INCIDENTE"]) and "critica" in str(row["GRAVEDAD"]):
            return "Sí"
        return "No"  

    inc_area["ESTADO_EXCEPCIONAL"] = inc_area.apply(check_estado, axis=1)
    if (inc_area["ESTADO_EXCEPCIONAL"] == "Sí").any():
        return "cierre temporal"
    
    estadoGlobalArea = ""
    #CASO ESTÁNDAR:
    if (mnt_juegos.shape[0] == 0):
        if (inc_area.shape[0] == 0):
            estadoGlobalArea = "ok"
        else:
            estadoGlobalArea = "pendiente evaluacion"
    else:
        if (inc_area.shape[0] == 0):
            estadoGlobalArea = "mantenimiento"
        else:
            estadoGlobalArea = "riesgo"
    
    return estadoGlobalArea



def new_attr(row):

    #Unknown NDP
    if (pd.isnull(row["NDP"])):
        row["CAPACIDAD_MAX"] = str(row["ID"]) + "-" + "CAPACIDAD_MAX" + "-" + "desconocido"
        row["CANTIDAD_JUEGOS_TIPO"] = str(row["ID"]) + "-" + "CANTIDAD_JUEGOS_TIPO" + "-" + "desconocido"
        row["ESTADO_GLOBAL"] = str(row["ID"]) + "-" + "ESTADO_GLOBAL" + "-" + "desconocido"
        
        return row

    #Known NDP
    filtered_juegos = juegos[juegos["NDP"] == row["NDP"]]
    
    #Unique NDP?
    if (len(copy_area[copy_area["NDP"] == row["NDP"]]) != 1): #NO
        #print(row["DIRECCION_AUX"])
        if ("desconocido" in row["DIRECCION_AUX"]):
            filtered_juegos["NEW_DIR"] = filtered_juegos[['TIPO_VIA', 'NOM_VIA', 'NUM_VIA', 'COD_POSTAL']].astype(str).agg('_'.join, axis=1)
            new_dir = row['TIPO_VIA'] + "_" + row['NOM_VIA'] + "_" + str(row['NUM_VIA']) + "_" + str(row['COD_POSTAL'])
            aux_filter = filtered_juegos[filtered_juegos["NEW_DIR"] == new_dir]
        else:
            aux_filter = filtered_juegos[filtered_juegos["DIRECCION_AUX"] == row["DIRECCION_AUX"]]
        
        #print(aux_filter.shape[0])
        row["CAPACIDAD_MAX"] = aux_filter.shape[0]

        juego_counts = (
        aux_filter.groupby("tipo_juego")
        .size()
        .reset_index(name="count")
        .to_dict(orient="records")
        )

        #print(juego_counts)

        row["CANTIDAD_JUEGOS_TIPO"] = juego_counts

        row["ESTADO_GLOBAL"] = estadoGlobalArea(row, aux_filter)

        return row
    
    #UNIQUE NDP

    row["CAPACIDAD_MAX"] = filtered_juegos.shape[0]

    juego_counts = (
        filtered_juegos.groupby("tipo_juego")
        .size()
        .reset_index(name="count")
        .to_dict(orient="records")
    )

    row["CANTIDAD_JUEGOS_TIPO"] = juego_counts
    
    row["ESTADO_GLOBAL"] = estadoGlobalArea(row, filtered_juegos)
    
    return row

if __name__ == "__main__":
    
    for col in ["CAPACIDAD_MAX", "CANTIDAD_JUEGOS_TIPO", "ESTADO_GLOBAL"]:
        if col not in area.columns:
            copy_area[col] = None

    copy_area = copy_area.apply(new_attr, axis=1)

    print(copy_area.head())

    area["CAPACIDAD_MAX"] = copy_area["CAPACIDAD_MAX"]
    area["CANTIDAD_JUEGOS_TIPO"] = copy_area["CANTIDAD_JUEGOS_TIPO"]
    area["ESTADO_GLOBAL"] = copy_area["ESTADO_GLOBAL"]

    #SAVE
    area.to_csv(os.path.join("cleaned", "Areas.csv"), header=True, sep=',', index=False)