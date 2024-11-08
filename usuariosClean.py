import json
import os
import pandas as pd
import formatting as fr
from generalAnalysis import general_analysis
import cleaningFunctions as cf
import newAttr as new


def formatting(usuarios):
    fr.general_format(usuarios)
    usuarios["TELEFONO"] = usuarios["TELEFONO"].apply(fr.format_phone_number).astype(str)
    usuarios["EMAIL"] = usuarios["EMAIL"].apply(fr.remove_dup_prefix)
    usuarios.drop_duplicates(subset=["NIF", "EMAIL", "TELEFONO"])

def cleaning(usuarios, results, parser, all_df):
    cf.clean_null("NIF", usuarios, results['n_columns'], parser[5]['null_values'], all_df)
    return unique_nif(usuarios)

def unique_nif(usuarios):
    new_usuarios = pd.DataFrame()

    for nif in usuarios["NIF"].unique():
        df_nif = usuarios[usuarios["NIF"] == nif]
        row = pd.Series()

        row["NIF"] = nif
        row["NOMBRE"] = ""
        row["EMAIL"] = []
        row["TELEFONO"] = []
        for index, r in df_nif.iterrows():
            row["NOMBRE"] = r["NOMBRE"]
            if r["EMAIL"] not in row["EMAIL"]:
                row["EMAIL"].append(r["EMAIL"])

            if r["TELEFONO"] not in row["TELEFONO"]:
                row["TELEFONO"].append(r["TELEFONO"])

        new_usuarios = pd.concat([new_usuarios, row.to_frame().T], ignore_index=True)
        return new_usuarios

def save(usuarios):
    usuarios.to_csv(os.path.join("cleaned", "UsuariosLimpio.csv"), header=True, sep=',', index=False)


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

    usuarios = pd.read_csv(os.path.join("files", "UsuariosSucio.csv"), sep=',')

    # FORMATTING
    fr.general_format(usuarios)
    usuarios["TELEFONO"] = usuarios["TELEFONO"].apply(fr.format_phone_number).astype(str)

    usuarios["EMAIL"] = usuarios["EMAIL"].apply(fr.remove_dup_prefix)
    usuarios.drop_duplicates(subset=["NIF", "EMAIL", "TELEFONO"])

    # GENERAL ANALYSIS
    results = general_analysis(usuarios, ["NIF"])

    #CLEANING
    print("\n[usuarios][CLEAN_NULLS]")
    cf.clean_null("NIF", usuarios, results['n_columns'], parser[5]['null_values'], all_df)

    #unique nif
    print(len(usuarios["NIF"].unique()))
    new_usuarios = pd.DataFrame()
    
    for nif in usuarios["NIF"].unique():
        df_nif = usuarios[usuarios["NIF"] == nif]
        row = pd.Series()

        row["NIF"] = nif
        row["NOMBRE"] = ""
        row["EMAIL"] = []
        row["TELEFONO"] = []
        for index, r in df_nif.iterrows():
            row["NOMBRE"] = r["NOMBRE"]
            if r["EMAIL"] not in row["EMAIL"]:
                row["EMAIL"].append(r["EMAIL"])

            if r["TELEFONO"] not in row["TELEFONO"]:
                row["TELEFONO"].append(r["TELEFONO"])

        new_usuarios = pd.concat([new_usuarios, row.to_frame().T], ignore_index=True)

    # SAVE
    new_usuarios.to_csv(os.path.join("cleaned", "UsuariosLimpio.csv"), header=True, sep=',', index=False)