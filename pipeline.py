
import json
import os
import pandas as pd

import incidenciasClean
import incidentesClean
import mantenimientoClean
import usuariosClean
import meteoClean
from generalAnalysis import general_analysis
import cleaningFunctions as cf
import formatting as fr

import areaClean
import encuestasClean

if __name__ == "__main__":

    # 1: Loading dirty datasets
    with open(os.path.join("cleaning_param", "parser.json"), 'r', encoding="utf-8") as js:
        parser = json.load(js)

    all_df = {"area": pd.read_csv(os.path.join("files", "AreasSucio.csv"), sep=','),
              "encuestas": pd.read_csv(os.path.join("files", "EncuestasSatisfaccionSucio.csv"), sep=','),
              "incidencias": pd.read_csv(os.path.join("files", "IncidenciasUsuariosSucio.csv"), sep=','),
              "incidentes": pd.read_csv(os.path.join("files", "IncidentesSeguridadSucio.csv"), sep=','),
              "mantenimientos": pd.read_csv(os.path.join("files", "MantenimientoSucio.csv"), sep=','),
              "usuarios": pd.read_csv(os.path.join("files", "UsuariosSucio.csv"), sep=','),
              "juegos": pd.read_csv(os.path.join("files", "JuegosSucio.csv"), sep=',')}

    # 2: FORMATTING
    areaClean.formatting(all_df["area"])
    encuestasClean.formatting(all_df["encuestas"])
    incidenciasClean.formatting(all_df["incidencias"])
    incidentesClean.formatting(all_df["incidentes"])
    mantenimientoClean.formatting(all_df["mantenimientos"])
    usuariosClean.formatting(all_df["usuarios"])

    # 3: GENERAL ANALYSIS
    results = {"area": general_analysis(all_df["area"], ["ID"]),
               "encuestas": general_analysis(all_df["encuestas"], ["ID"]),
               "incidencias": general_analysis(all_df["incidencias"], ["ID"]),
               "incidentes": general_analysis(all_df["incidentes"], ["ID"]),
               "mantenimientos": general_analysis(all_df["mantenimientos"], ["ID"]),
               "usuarios": general_analysis(all_df["usuarios"], ["NIF"]),
               "juegos": general_analysis(all_df["juegos"], ["ID"])}

    # 4: CLEANING
    # 4.A. Area
    areaClean.cleaning(all_df["area"], results["area"], parser, all_df)
    areaClean.save(all_df["area"])

    # 4.B. In

    meteoClean.clean_meteo()


    #OJO: CLEANING USUARIS RETORNA DATASET DE LIMPIEZA.
    #AÑADIR AREA_NEWATT

    #5: FINAL ADJUSTMENTS
    areaClean.final_formatting(all_df["area"])
    areaClean.save(all_df["area"])

