import os
import json

import datetime 
import pandas as pd
import cleaningFunctions as cf
from generalAnalysis import general_analysis
import formatting as fr
import newAttr as new



def cleanse_area(df_data, to_process: dict, parser: dict, df)-> None:
    """Functions responsible for the cleaning of Area dataset."""
    print("Cleaning Area dataset...")
    #cf.clean_duplicates("area", df_data, to_process["unique_id"], parser["unique_id"])
    #df_data = cf.clean_null("ID", df_data, to_process['n_columns'], parser['null_values'], df)
    df_data = cf.format_spacial_coordenates_area(df_data)
    df_data.to_csv(os.path.join("cleaned", "AreasLimpio.csv"), header=True, sep=',', index=False)

def cleanse_encuestas(df_data, to_process: dict, parser: dict, df)->None:
    #cf.clean_duplicates("encuestas", df_data, to_process["unique_id"], parser["unique_id"])
    df_data = cf.clean_null("ID", df_data, to_process['n_columns'], parser['null_values'], df)
    #df_data.to_csv(os.path.join("cleaned", "EncuestasSatisfaccionLimpio.csv"), header=True, sep=',', index=False)

def cleanse_incidencias(df_data, to_process: dict, parser: dict, df):
    #cf.clean_duplicates("incidentes", df_data, to_process["unique_id"], parser["unique_id"])
    new.nivelEscalamiento(df_data)
    df_data = cf.clean_null("ID", df_data, to_process['n_columns'], parser['null_values'], df)
    #df_data.to_csv(os.path.join("cleaned", "IncidenciasLimpio.csv"), header=True, sep=',', index=False)

def cleanse_incidentes(df_data, to_process: dict, parser: dict, df):
    #cf.clean_duplicates("incidentes", df_data, to_process["unique_id"], parser["unique_id"])
    df_data = cf.clean_null("ID", df_data, to_process['n_columns'], parser['null_values'], df)
    #df_data.to_csv(os.path.join("cleaned", "IncidentesLimpio.csv"), header=True, sep=',', index=False)



def cleanse_mantenimiento(df_data, to_process: dict, parser: dict, df):
    #cf.clean_duplicates("mantenimiento", df_data, to_process["unique_id"], parser["unique_id"])
    df_data = cf.clean_null("ID", df_data, to_process['n_columns'], parser['null_values'], df)
    df_data["ID"] = cf.format_mamntenimiento_ID(df_data["ID"])
    df_data.to_csv(os.path.join("cleaned", "MantenimientoLimpio.csv"), header=True, sep=',', index=False)

def cleanse_usuarios(df_data, to_process: dict, parser: dict, df):
    #cf.clean_duplicates("usuarios", df, to_process["unique_id"], parser["unique_id"])
    df_data = cf.clean_null("NIF", df_data, to_process['n_columns'], parser['null_values'], df)
    #df_data.to_csv(os.path.join("cleaned", "UsuariosLimpio.csv"), header=True, sep=',', index=False)

def cleanse_juegos(df_data, to_process: dict, parser: dict, df):
    print("Cleaning Juegos dataset...")
    #cf.clean_duplicates("juegos", df_data, to_process["unique_id"], parser["unique_id"])
    #df_data = cf.clean_null("ID", df_data, to_process['n_columns'], parser['null_values'], df)
    df_data = cf.format_spacial_coordenates_juego(df_data)
    df_data.to_csv(os.path.join("cleaned", "JuegosLimpio.csv"), header=True, sep=',', index=False)

def cleanse_meteo(df):
    pass

if __name__ == "__main__":

    
    with open (os.path.join("cleaning_param", "param.json"), 'r', encoding="utf-8") as js:
        gcl_data = json.load(js)

    # PARSER FOR CLEANING
    with open(os.path.join("cleaning_param", "parser.json"), 'r', encoding="utf-8") as js:
        parser = json.load(js)

    all_df = {}

    all_df["area"] = pd.read_csv(os.path.join("files", "AreasSucio.csv"), sep=',')
    all_df["encuestas"] = pd.read_csv(os.path.join("files", "EncuestasSatisfaccionSucio.csv"), sep=',')
    all_df["incidencias"] = pd.read_csv(os.path.join("files", "IncidenciasUsuariosSucio.csv"), sep=',')
    all_df["incidentes"] = pd.read_csv(os.path.join("files", "IncidentesSeguridadSucio.csv"), sep=',')
    all_df["mantenimientos"] = pd.read_csv(os.path.join("files", "MantenimientoSucio.csv"), sep=',') #TODO: Revisar ID
    all_df["usuarios"] = pd.read_csv(os.path.join("files", "UsuariosSucio.csv"), sep=',') #TODO: NIF especial porque email y teléfono diferentes.
    all_df["juegos"] = pd.read_csv(os.path.join("files", "JuegosSucio.csv"), sep=',')
    all_df["meteo"] = pd.read_csv(os.path.join("files", "meteo24.csv"), sep=',') #Revisar JSON.
    
    #print("Columns: ", all_df["area"].columns)
    #print(all_df["area"].head())

    #FORMATTING:

    #Formatting Normalization + Typographic corrections
    """i = 5
    for key in all_df.keys():
        fr.general_format(all_df[key])
        fr.typo_format(all_df[key], gcl_data[i]["c_format"])

        i += 1"""

    #GENERAL ANALYSIS:
    #Ahora que lo estamos probando de uno en uno hay que actualizar i cada vez (area=0, encuestas=1 ...)
    i = 0
    results = {}
    for key in all_df.keys():
        results[key] = general_analysis(all_df[key], gcl_data[i]["c_id"])

        i += 1

    cleanse_area(all_df['area'], results["area"], parser[0], all_df)
    #cleanse_encuestas(all_df['encuestas'], results["encuestas"], parser[1], all_df)
    #cleanse_incidencias(all_df['incidencias'], results["incidencias"], parser[2], all_df)
    #cleanse_incidentes(all_df['incidentes'], results["incidentes"], parser[3], all_df)
    #cleanse_mantenimiento(all_df["mantenimientos"], results["mantenimientos"], parser[4], all_df)
    #cleanse_usuarios(all_df["usuarios"], results["usuarios"], parser[5], all_df)
    cleanse_juegos(all_df['juegos'], results["juegos"], parser[6], all_df)
    #cleanse_meteo(df_meteo)
