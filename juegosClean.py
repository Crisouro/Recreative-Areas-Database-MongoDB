
import json
import os
import pandas as pd
import formatting as fr
from generalAnalysis import general_analysis
import cleaningFunctions as cf
import newAttr as new

def formatting(juegos):
    fr.general_format(juegos)
    fr.date_typo_format(juegos, "FECHA_INSTALACION")
    fr.accesible_bool(juegos)
    fr.fix_accent_street_name(juegos)


def cleaning(juegos, results, parser, all_df):
    cf.clean_duplicates("juegos", juegos, results["unique_id"], parser[6]["unique_id"])
    cf.clean_null("ID", juegos, results['n_columns'], parser[6]['null_values'], all_df)

def new_attributes(juegos):
    new.indicadorExposicion(juegos)
    mantenimientos_aux = pd.read_csv(os.path.join("cleaned", "MantenimientoLimpio.csv"), sep=',')
    new.desgasteAcumulado(juegos, mantenimientos_aux)
    new.ultimaFechaMantenimiento(juegos, mantenimientos_aux)


def final_formatting(juegos):
    fr.spacial_coordenates_juego(juegos)
    fr.accesible_bool(juegos)

def save(juegos):
    juegos.to_csv(os.path.join("cleaned", "JuegosLimpio.csv"), header=True, sep=',', index=False)


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

    juegos = pd.read_csv(os.path.join("files", "JuegosSucio.csv"), sep=',')

    #AUX DATASET WITH CURRENTLY CLEANED DATASETS
    clean_df = all_df.copy()
    clean_df["area"] = pd.read_csv(os.path.join("cleaned", "AreasLimpio.csv"), sep=',')


    #FORMATTING
    fr.general_format(juegos)
    fr.date_typo_format(juegos, "FECHA_INSTALACION")
    fr.fix_accent_street_name(juegos)

    #GENERAL ANALYSIS
    results = general_analysis(juegos, ["ID"])
    
    #CLEANING
    cf.clean_duplicates("juegos", juegos, results["unique_id"], parser[6]["unique_id"])
    
    print("\n[juegos][CLEAN_NULLS]")
    cf.clean_null("ID", juegos, results['n_columns'], parser[6]['null_values'], clean_df)
    
    #NEW ATTR
    new.indicadorExposicion(juegos)
    mantenimientos = pd.read_csv(os.path.join("cleaned", "MantenimientoLimpio.csv"), sep=',')
    new.desgasteAcumulado(juegos, mantenimientos)
    new.ultimaFechaMantenimiento(juegos, mantenimientos)

    #FINAL FORMATTING
    fr.spacial_coordenates_juego(juegos)
    fr.accesible_bool(juegos)

    #SAVE
    juegos.to_csv(os.path.join("cleaned", "JuegosLimpio.csv"), header=True, sep=',', index=False)