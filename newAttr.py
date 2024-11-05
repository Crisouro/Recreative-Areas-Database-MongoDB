import pandas as pd
import random
import numpy as np

def nivelEscalamiento(df):
    """Function that generates nivelEscalamiento value for df."""
    enum = {"desgaste": "muy alto", "rotura": "medio", "vandalismo": "bajo", "mal funcionamiento": "alto"}
    for key, value in enum.items():
        df.loc[df["TIPO_INCIDENCIA"] == key, "NIVEL_ESCALAMIENTO"] = value

def indicadorExposicion(df):
    """Function that generates indicadorExposicion value for df"""
    df["INDICADOR_EXPOSICION"] = np.random.choice["bajo", "medio", "alto"]

def capacidadMax(df):
    "Function that generates capacidadMax value for df"
    pass