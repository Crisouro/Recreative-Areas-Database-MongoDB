
import json
import os
import pandas as pd

import incidenciasClean
import incidentesClean
import juegosClean
import mantenimientoClean
import usuariosClean
import meteoClean
import areaNewAttr
from generalAnalysis import general_analysis


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
    # 4.A. Area: clean
    areaClean.cleaning(all_df["area"], results["area"], parser, all_df)
    areaClean.save(all_df["area"])

    # 4.B. Encuestas
    encuestasClean.cleaning(all_df["encuestas"], results["encuestas"], parser, all_df)
    encuestasClean.save(all_df["encuestas"])

    # 4.C. Mantenimiento: clean
    mantenimientoClean.cleaning(all_df["mantenimientos"], results["mantenimientos"], parser, all_df)
    mantenimientoClean.save(all_df["mantenimientos"])

    # 4.D. Incidencias: clean & new attributes
    incidenciasClean.cleaning(all_df["incidencias"], results["incidencias"], parser, all_df)
    incidenciasClean.new_attributes(all_df["incidencias"])
    incidenciasClean.save(all_df["incidencias"])

    # 4.E. Incidentes: clean
    incidentesClean.cleaning(all_df["incidentes"], results["incidentes"], parser, all_df)
    incidentesClean.save(all_df["incidentes"])


    # 4.F. Juegos
    all_df["area"] = pd.read_csv(os.path.join("cleaned", "AreasLimpio.csv"), sep=',')

    juegosClean.cleaning(all_df["juegos"], results["juegos"], parser, all_df)
    juegosClean.new_attributes(all_df["juegos"])
    juegosClean.save(all_df["juegos"])

    # 4.G. Usuarios

    all_df["usuarios"] = usuariosClean.cleaning(all_df["usuarios"], results["usuarios"], parser, all_df)
    usuariosClean.save(all_df["usuarios"])

    # 4.H. Meteo: full format, cleaning and saving
    meteoClean.clean_meteo()



    #5: FINAL ADJUSTMENTS
    areaNewAttr.new_attributes_area()

    areaClean.final_formatting(all_df["area"])
    areaClean.save(all_df["area"])
    juegosClean.final_formatting(all_df["juegos"])
    juegosClean.save(all_df["juegos"])

