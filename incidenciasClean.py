
import json
import os
import pandas as pd
import formatting as fr
from generalAnalysis import general_analysis
import cleaningFunctions as cf
import newAttr as new

def formatting(incidencias):
    fr.general_format(incidencias)
    fr.date_typo_format(incidencias, "FECHA_REPORTE")
    incidencias.rename(columns={'MantenimeintoID': 'MANTENIMIENTO_ID'}, inplace=True)


def cleaning(incidencias, results, parser, all_df):
    cf.clean_duplicates("incidencias", incidencias, results["unique_id"], parser[2]["unique_id"])
    cf.clean_null("ID", incidencias, results['n_columns'], parser[2]['null_values'], all_df)


def new_attributes(incidencias):
    new.nivelEscalamiento(incidencias)
    mantenimientos_aux = pd.read_csv(os.path.join("cleaned", "MantenimientoLimpio.csv"), sep=',')
    new.tiempoResolucion(incidencias, mantenimientos_aux)

def save(incidencias):
    incidencias.to_csv(os.path.join("cleaned", "IncidenciasLimpio.csv"), header=True, sep=',', index=False)



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

    incidencias = pd.read_csv(os.path.join("files", "IncidenciasUsuariosSucio.csv"), sep=',')

    #FORMATTING
    fr.general_format(incidencias)
    fr.date_typo_format(incidencias, "FECHA_REPORTE")
    incidencias.rename(columns= {'MANTENIMIENTO_ID' : 'MANTENIMIENTO_ID'}, inplace= True)

    #GENERAL ANALYSIS
    results = general_analysis(incidencias, ["ID"])
    
    #CLEANING
    cf.clean_duplicates("incidencias", incidencias, results["unique_id"], parser[2]["unique_id"])
    print("\n[incidencias][CLEAN_NULLS]")
    cf.clean_null("ID", incidencias, results['n_columns'], parser[2]['null_values'], all_df)
    
    #NEW ATTRIBUTES
    new.nivelEscalamiento(incidencias)
    mantenimientos = pd.read_csv(os.path.join("cleaned", "MantenimientoLimpio.csv"), sep=',')
    new.tiempoResolucion(incidencias, mantenimientos)


    #SAVE
    incidencias.to_csv(os.path.join("cleaned", "IncidenciasLimpio.csv"), header=True, sep=',', index=False)