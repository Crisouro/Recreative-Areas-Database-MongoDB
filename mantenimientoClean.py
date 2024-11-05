
import json
import os
import pandas as pd
import formatting as fr
from generalAnalysis import general_analysis
import cleaningFunctions as cf
import newAttr as new

if __name__ == "__main__":

    with open(os.path.join("cleaning_param", "parser.json"), 'r', encoding="utf-8") as js:
        parser = json.load(js)

    all_df = {}

    all_df["area"] = pd.read_csv(os.path.join("files", "AreasSucio.csv"), sep=',')
    all_df["encuestas"] = pd.read_csv(os.path.join("files", "EncuestasSatisfaccionSucio.csv"), sep=',')
    all_df["incidencias"] = pd.read_csv(os.path.join("files", "IncidenciasUsuariosSucio.csv"), sep=',')
    all_df["incidentes"] = pd.read_csv(os.path.join("files", "IncidentesSeguridadSucio.csv"), sep=',')
    all_df["mantenimientos"] = pd.read_csv(os.path.join("files", "MantenimientoSucio.csv"), sep=',') 
    all_df["usuarios"] = pd.read_csv(os.path.join("files", "UsuariosSucio.csv"), sep=',')
    all_df["juegos"] = pd.read_csv(os.path.join("files", "JuegosSucio.csv"), sep=',')

    mantenimiento = pd.read_csv(os.path.join("files", "MantenimientoSucio.csv"), sep=',')

    #FORMATTING
    fr.general_format(mantenimiento)
    fr.date_typo_format(mantenimiento, "FECHA_INTERVENCION")
    mantenimiento["ID"] = cf.format_mantenimiento_ID(mantenimiento["ID"]) #CAMBIAR A FORMATTING PLS

    #GENERAL ANALYSIS
    results = general_analysis(mantenimiento, ["ID"])
    
    #CLEANING
    cf.clean_duplicates("incidencias", mantenimiento, results["unique_id"], parser[4]["unique_id"])
    print("\n[incidencias][CLEAN_NULLS]")
    mantenimiento = cf.clean_null("ID", mantenimiento, results['n_columns'], parser[4]['null_values'], all_df)
    

    #SAVE
    mantenimiento.to_csv(os.path.join("cleaned", "MantenimientoLimpio.csv"), header=True, sep=',', index=False)