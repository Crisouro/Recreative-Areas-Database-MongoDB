import json
import os
import pandas as pd
import formatting as fr
from generalAnalysis import general_analysis
import cleaningFunctions as cf
import newAttr as new

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
    usuarios["TELEFONO"] = usuarios["TELEFONO"].apply(fr.format_phone_number)
    usuarios["EMAIL"] = usuarios["EMAIL"].apply(fr.remove_dup_prefix)
    usuarios.drop_duplicates(subset=["NIF", "EMAIL", "TELEFONO"])

    # GENERAL ANALYSIS
    results = general_analysis(usuarios, ["NIF"])



    print("\n[usuarios][CLEAN_NULLS]")
    usuarios = cf.clean_null("NIF", usuarios, results['n_columns'], parser[5]['null_values'], all_df) #HACER QUE FUNCIONE




    # SAVE
    usuarios.to_csv(os.path.join("cleaned", "UsuariosLimpio.csv"), header=True, sep=',', index=False)