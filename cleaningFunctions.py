import os
import json
import pandas as pd
import pyproj
import strategy as str
import re

def clean_null(id_column:str, df_data: dict, null_columns: list, parser: dict, full_df):
    """Algorithm for cleaning the null values of a column"""
    result = {}
    for column in null_columns:
        print(column, "detectado...")
        #if column == "FECHA_INSTALACION":
        print(parser)
        df_data[column] = str.null_assign(column, id_column, df_data, parser["search_values"][column], parser["data_values"][column], full_df)
    return df_data

    
def clean_duplicates(dataset, df, unique: dict, parser: dict):
    """Algorithm for cleansing duplicate ID."""
    
    print(f"['{dataset}'][CLEAN_DUPLICATES]")

    unique_conditions = {}
    unique_ids = list(unique.keys())
    print("UNIQUE KEYS:", unique_ids)
    unique_ids.remove("same")

    for id in unique_ids:
        unique_conditions[id] = parser[id]
    
    for c_id in unique_ids:
        #All duplicates don't share same data.
        if (not unique["same"]["same"]):
            
            for i, dup in unique["same"]["col_diff"][c_id].items():
                print(dup)
                #Each duplicate value has different values in between regarding relevant columns that make an entry unique.
                
                #Trabajar esta condición
                unique_dup = False
                if any(item in dup["all"] for item in unique_conditions[id]):
                    unique_dup = True
                #>>>>

                if (unique_dup):
                    #APPLYING STRATEGY FOR GIVING UNIQUE VALUE.
                    str.renaming_id(df, c_id, i)
                else:
                    if (len(dup["some"]) == 0):
                        #DUPLICATES ARE ALL THE SAME -> DELETE.
                        print(i)
                        str.delete_duplicates(df, c_id, i)
            
        #All duplicates share same data.
        else:
            for i, dup in unique["same"]["col_diff"][c_id].items():
                print(i)
                str.delete_duplicates(df, c_id, i)

            pass #Delete duplicates.

def format_mamntenimiento_ID(id_column) -> dict:
    new_id = []
    for i in range(len(id_column)):
        item = id_column[i].strip()
        num, letters = item.split(",00")
        new_id.append(f"{letters}{num.zfill(6)}")
    return new_id

def format_spacial_coordenates_area(df_data: dict) -> dict:
   """This function transforms the latitude and longitude into a single column"""
   #Unpacking needed data
   x_column= df_data['LONGITUD']
   y_column = df_data['LATITUD']
   new_coord =[]

   for i in range(len(x_column)):
       #data transformation into a longitude-latitude pair.
       x = float(x_column[i])
       y = float(y_column[i])
       new_coord.append([x, y])

   #Seting up the new dataset structure
   df_data['COORD_GIS_X'], df_data['SISTEMA_COORD'] = new_coord, ['WGS84']*len(df_data)
   df_data.rename(columns={"COORD_GIS_X": "COORD_GIS"})
   df_data.drop(columns=['COORD_GIS_Y', 'LATITUD', 'LONGITUD'], inplace=True)
   return df_data

def format_spacial_coordenates_juego(df_data: dict) -> dict:
    """This function transforms the UTM coordinate columns into a single longitude-latitude column"""
    x_column = df_data['COORD_GIS_X']
    y_column = df_data['COORD_GIS_Y']
    new_coord = []
    # UTM configuration to Madrid area
    transformer = pyproj.Transformer.from_crs("EPSG:25830", "EPSG:4326", always_xy=True)

    for i in range(len(x_column)):
        # data transformation into a longitude-latitude pair.
        x = float(x_column[i])
        y = float(y_column[i])
        x,y = transformer.transform(x, y)
        new_coord.append([x,y])

    # Seting up the new dataset structure
    df_data['COORD_GIS_X'], df_data['SISTEMA_COORD'] = new_coord, ['WGS84'] * len(df_data)
    df_data.rename(columns={"COORD_GIS_X": "COORD_GIS"})
    df_data.drop(columns=['COORD_GIS_Y'], inplace=True)
    return df_data
def resolution_time(df_data: dict, df_mantenimiento) -> dict:
    for item in df_data:
        print(item)
        # Step 1: find Manteinance associated to an Incidence
        search_key = item['MantenimeintoID']
        candidates = df_mantenimiento.query(f" 'ID' == {search_key}")
        #Step 2: use the latest manteinance date as close date
        print(candidates['FECHA_INTERVENCION'].max())
        print(candidates['FECHA_INTERVENCION'].min())
        #Stept 3: calculation of solving time
    #return df_data