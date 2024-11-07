
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

    area = pd.read_csv(os.path.join("files", "AreasSucio.csv"), sep=',')

    #FORMATTING
    fr.general_format(area)
    fr.date_typo_format(area, "FECHA_INSTALACION")
    fr.fix_accent_street_name(area)
    fr.fix_accent_street_name(area, "DIRECCION_AUX")

    #GENERAL ANALYSIS
    results = general_analysis(area, ["ID"])
    
    #CLEANING
    cf.clean_duplicates("area", area, results["unique_id"], parser[0]["unique_id"])
    
    print("\n[area][CLEAN_NULLS]")
    area = cf.clean_null("ID", area, results['n_columns'], parser[0]['null_values'], all_df)

    #FINAL FORMATTING
    fr.spacial_coordenates_area(area)
    
    #SAVE
    area.to_csv(os.path.join("cleaned", "AreasLimpio.csv"), header=True, sep=',', index=False)





