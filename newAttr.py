import pandas as pd

def nivelEscalamiento(df):
    """Function that generates nivelEscalamiento value for df."""
    enum = {"Desgaste": "muy alto", "Rotura": "medio", "Vandalismo": "bajo", "Mal funcionamiento": "alto"}
    for key, value in enum.items():
        df.loc[df["TIPO_INCIDENCIA"] == key, "NIVEL_ESCALAMIENTO"] = value

def capacidadMax(df):
    "Function that generates capacidadMax value for df"
    pass