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





        
def clean_format(c: str, df, pattern: str, add = ""):
    """Algorithm for cleansing the format of a column."""

    regex = re.compile(pattern)
    
    def format_id(x):
        if pd.notnull(x):
            if regex.match(x):
                return x 
            else:
                numbers = ''.join(re.findall(r"\d+", x))

                if numbers:
                    return f"AR_{numbers}"
                
        return x

    if (c in ["NIF", "ID"]):
        df[c] = df[c].apply(lambda x: format_id(x))
    

def clean_duplicates(dataset, df, unique: dict, exp_format: dict, parser: dict):
    """Algorithm for cleansing duplicate ID."""
    
    print(f"['{dataset}'][CLEAN_DUPLICATES]")

    unique_conditions = {}
    unique_ids = list(unique.keys())
    unique_ids.remove("same")

    for id in unique_ids:
        unique_conditions[id] = parser[id]
    
    for c_id in unique_ids:
        #All duplicates don't share same data.
        if (not unique["same"]["same"]):
            
            unique_dup = 0
            for i, dup in unique["same"]["col_diff"][c_id].items():
                #Each duplicate value has different values in between regarding relevant columns that make an entry unique.
                if all(item in dup["all"] for item in unique_conditions[id]):
                    unique_dup += 1
            
            if (unique_dup == len(unique["same"]["col_diff"][id].keys())):
                #APPLYING STRATEGY FOR GIVING UNIQUE VALUE.
                str.renaming_id()
            
        #All duplicates share same data.
        else:
            pass #Delete duplicates.