
import json
import os
import pandas as pd
import formatting as fr
from generalAnalysis import general_analysis
import cleaningFunctions as cf
import newAttr as new

def formatting(incidentes):
    fr.general_format(incidentes)
    fr.date_typo_format(incidentes, "FECHA_REPORTE")

def cleaning(incidentes, results, parser, all_df):
    cf.clean_duplicates("incidentes", incidentes, results["unique_id"], parser[3]["unique_id"])
    cf.clean_null("ID", incidentes, results['n_columns'], parser[3]['null_values'], all_df)
    incidentes["ID"] = incidentes["ID"].astype(str)
    incidentes["AreaRecreativaID"] = incidentes["AreaRecreativaID"].astype(str)

def save(incidentes):
    incidentes.to_csv(os.path.join("cleaned", "IncidentesLimpio.csv"), header=True, sep=',', index=False)


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

    incidentes = pd.read_csv(os.path.join("files", "IncidentesSeguridadSucio.csv"), sep=',')

    #FORMATTING
    fr.general_format(incidentes)
    fr.date_typo_format(incidentes, "FECHA_REPORTE")

    #GENERAL ANALYSIS
    results = general_analysis(incidentes, ["ID"])
    
    #CLEANING
    cf.clean_duplicates("incidentes", incidentes, results["unique_id"], parser[3]["unique_id"])
    print("\n[incidentes][CLEAN_NULLS]")
    cf.clean_null("ID", incidentes, results['n_columns'], parser[3]['null_values'], all_df)
    
    incidentes["ID"] = incidentes["ID"].astype(str)
    incidentes["AreaRecreativaID"] = incidentes["AreaRecreativaID"].astype(str)

    #SAVE
    incidentes.to_csv(os.path.join("cleaned", "IncidentesLimpio.csv"), header=True, sep=',', index=False)