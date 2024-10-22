import os
import json
import pandas as pd


def clean_null(df, null_columns: list, parser: dict):
    for column in null_columns:
        fill_value = parser[column]
        df.fillna({column: fill_value}, inplace=True)

def clean_duplicates(df, null_columns: list, parser: dict):
    pass