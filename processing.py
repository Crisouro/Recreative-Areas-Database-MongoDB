import os
import json
import datetime 
import pandas as pd
import cleaningFunctions as cf
from generalAnalysis import general_analysis


def cleanse_area(df, to_process: dict, parser: dict, format)-> None:
    """Functions responsible for the cleaning of Area dataset."""
    cf.clean_duplicates("area", df, to_process["unique_id"], parser["unique_id"])
    #cf.clean_null(df, to_process['n_columns'], parser['null_values'])

    df.to_csv(os.path.join("datasets", "Areas_cleaned.csv"), header=True, sep=',', index=False)



def cleanse_encuestas(df):
    pass

def cleanse_incidencias(df, to_process: dict, parser: dict, format):
    cf.clean_duplicates("incidentes", df, to_process["unique_id"], parser["unique_id"])
    df.to_csv(os.path.join("cleaned", "IncidenciasLimpio.csv"), header=True, sep=',', index=False)

def cleanse_incidentes(df, to_process: dict, parser: dict, format):
    cf.clean_duplicates("incidentes", df, to_process["unique_id"], parser["unique_id"])
    df.to_csv(os.path.join("cleaned", "IncidentesLimpio.csv"), header=True, sep=',', index=False)



def cleanse_mantenimiento(df):
    pass

def cleanse_usuarios(df):
    pass

def cleanse_juegos(df, to_process: dict, parser: dict, format):
    cf.clean_duplicates("juegos", df, to_process["unique_id"], parser["unique_id"])
    df.to_csv(os.path.join("cleaned", "JuegosLimpio.csv"), header=True, sep=',', index=False)

def cleanse_meteo(df):
    pass

if __name__ == "__main__":

    
    with open (os.path.join("cleaning_param", "param.json")) as js:
        gcl_data = json.load(js)

    # PARSER FOR CLEANING
    with open(os.path.join("cleaning_param", "parser.json")) as js:
        parser = json.load(js)

    all_df = {}

    all_df["area"] = pd.read_csv(os.path.join("files", "AreasSucio.csv"), sep=',')
    #all_df["encuestas"] = pd.read_csv(os.path.join("files", "EncuestasSatisfaccionSucio.csv"), sep=',')
    #all_df["incidencias"] = pd.read_csv(os.path.join("files", "IncidenciasUsuariosSucio.csv"), sep=',')
    #all_df["incidentes"] = pd.read_csv(os.path.join("files", "IncidentesSeguridadSucio.csv"), sep=',')
    #all_df["mantenimientos"] = pd.read_csv(os.path.join("files", "MantenimientoSucio.csv"), sep=',')
    #all_df["usuarios"] = pd.read_csv(os.path.join("files", "UsuariosSucio.csv"), sep=',')
    #all_df["juegos"] = pd.read_csv(os.path.join("files", "JuegosSucio.csv"), sep=',')
    #all_df["meteo"] = pd.read_csv(os.path.join("files", "meteo24.csv"), sep=',') #Revisar JSON.
    
    #print("Columns: ", all_df["area"].columns)
    #print(all_df["area"].head())

    #GENERAL ANALYSIS:
    #Ahora que lo estamos probando de uno en uno hay que actualizar i cada vez (area=0, encuestas=1 ...)
    i = 7
    results = {}
    for key in all_df.keys():
        print(gcl_data[i])
        results[key] = general_analysis(all_df[key], gcl_data[i]["c_id"], gcl_data[i]["c_format"], gcl_data[i]["c_enum"])

        i += 1

    cleanse_area(all_df['area'], results["area"], parser[0], gcl_data[0]["c_format"])
    #cleanse_encuestas(df_encuestas)
    #cleanse_incidencias(all_df['incidencias'], results["incidencias"], parser[2], gcl_data[2]["c_format"])
    #cleanse_incidentes(all_df['incidentes'], results["incidentes"], parser[3], gcl_data[3]["c_format"])
    #cleanse_mantenimiento(all_df["mantenimientos"], results["mantenimientos"], parser[4], gcl_data[4]["c_format"])
    #cleanse_usuarios(df_usuarios)
    #cleanse_juegos(all_df['juegos'], results["juegos"], parser[6], gcl_data[6]["c_format"])
    #cleanse_meteo(df_meteo)
