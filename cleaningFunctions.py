import os
import json
import pandas as pd
import strategy as str
import re

def clean_null(df, null_columns: list, parser: dict):
    """Algorithm for cleaning the null values of a column"""
    for column in null_columns:

        if column== "COD_DISTRITO":
            str.null_codDistrito_asign(df[column], parser["COD_DISTRITO"])
        elif column== "DISTRITO":
            print("detecting distrito")
            #null_distrito_asign()
    
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