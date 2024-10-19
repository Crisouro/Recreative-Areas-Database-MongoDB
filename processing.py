import os
import json
import datetime 
import pandas as pd


def null_values(df)-> list:
    """Function that detects columns with null values in the dataset."""
    n_columns = []
    
    print("\n[GENERAL ANALYSIS][NULL VALUES]")
    for c in df.columns:
        if (df[c].isnull().any()):
            n_columns.append(c)
    print("The following columns have missing values: ", n_columns)

    return n_columns


def unique_id(df, c_id: list)-> dict:
    """Function that checks whether all the id elements in the datasets are unique."""

    unique = {}
    print("\n[GENERAL ANALYSIS][UNIQUE ID]")
    for c in c_id:
        duplicates = df[c][df[c].duplicated()].unique().tolist()

        if(len(duplicates) != 0):
            print("Duplicated data ", c, ": ", duplicates)
        else:
            print("No duplicated data")

        unique[c] = duplicates
    
    return unique

def exp_format(df, cd_format):
    """Function that checks whether the column format coincides with the expected one"""

    expected = {}
    
    print("\n[GENERAL ANALYSIS][EXPECTED_FORMAT]")
    for c in cd_format.keys():
        regex = cd_format[c]

        expected[c] = df[c].str.match(regex).all()
        if (not expected[c]):
            print(c, " values doesn't match expected format ", cd_format[c])
        else:
            print(c, " values match expected format ", cd_format[c])
    
    return expected
        

def enum_display(df, c_enum: list)-> dict:
    """Function that displays the values used in an enumerated type field."""
    enum_values = {}

    print("\n[GENERAL ANALYSIS][ENUMERATION DISPLAY]")
    for c in c_enum:
        enum_values[c] = df[c].unique()
        print(c, ": ", enum_values[c])

    return enum_values

def general_analysis(df, c_id: list, cd_format: dict, c_enum: list)-> dict:
    """Function that executes a general analysis with common anomalies to all dataframes."""
    to_process = {}

    to_process["n_columns"] = null_values(df)               #1) Columns with null values?
    to_process["unique_id"] = unique_id(df, c_id)           #2) A Unique data column has duplicates?
    to_process["exp_format"] = exp_format(df, cd_format)    #3) The column data follows the expected format.
    to_process["enum_values"] = enum_display(df, c_enum)    #4) Values in enumerated type columns.

    #type_analysis(df, c_type)                              #2) All columns' data are the expected type?

    return to_process


def limpieza_area(df):

    pass

def limpieza_encuestas(df):
    pass

def limpieza_incidencias(df):
    pass

def limpieza_incidentes(df):
    pass

def limpieza_mantenimiento(df):
    pass

def limpieza_usuarios(df):
    pass

def limpieza_juegos(df):
    pass

def limpieza_meteo(df):
    pass

if __name__ == "__main__":

    
    with open (os.path.join("cleaning_param", "param.json")) as js:
        gcl_data = json.load(js)

    all_df = {}

    all_df["area"] = pd.read_csv(os.path.join("datasets", "Areas.csv"), sep=',')
    #all_df["encuestas"] = pd.read_csv(os.path.join("datasets", "Dirty_EncuestaSatisfaccion.csv"), sep=',', index_col=0)
    #all_df["incidencias"] = pd.read_csv(os.path.join("datasets", "Dirty_Incidencias.csv"), sep=',', index_col=0)
    #all_df["incidentes"] = pd.read_csv(os.path.join("datasets", "Dirty_IncidenteSeguridad.csv"), sep=',', index_col=0)
    #all_df["mantenimientos"] = pd.read_csv(os.path.join("datasets", "Dirty_Mantenimientos.csv"), sep=',', index_col=0)
    #all_df["usuarios"] = pd.read_csv(os.path.join("datasets", "Dirty_Usuarios.csv"), sep=',', index_col=0)
    #all_df["juegos"] = pd.read_csv(os.path.join("datasets", "Juegos.csv"), sep=',', index_col=0)
    #all_df["meteo"] = pd.read_csv(os.path.join("datasets", "Meteo.csv"), sep=',', index_col=0)
    
    print("Columns: ", all_df["area"].columns)
    print(all_df["area"].head())

    #ANÁLISIS GENERAL:
    i = 0
    for key in all_df.keys():
        print(gcl_data[i])
        general_analysis(all_df[key], gcl_data[i]["c_id"], gcl_data[i]["c_format"], gcl_data[i]["c_enum"])
        i += 1


    #limpieza_area(df_area)
    #limpieza_encuestas(df_encuestas)
    #limpieza_incidencias(df_incidencias)
    #limpieza_incidentes(df_incidentes)
    #limpieza_mantenimiento(df_mantenimientos)
    #limpieza_usuarios(df_usuarios)
    #limpieza_juegos(df_juegos)
    #limpieza_meteo(df_meteo)