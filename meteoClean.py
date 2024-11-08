import pandas as pd
from datetime import datetime
import os




def codPostal(meteo, cp):
    """Function that associates COD_POSTAL with each PUNTO_MUESTREO in meteo24.csv"""
    
    meteo['PM_PREFIX'] = meteo['PUNTO_MUESTREO'].str.split('_').str[0].astype(int)

    cod_postal_map = dict(zip(cp["CÓDIGO"], cp["Codigo Postal"]))

    def lambda_function(x):
        literal = cod_postal_map[x].split(',')

        return [int(l) for l in literal]

    meteo["COD_POSTAL"] = meteo["PM_PREFIX"].map(lambda x: lambda_function(x))

    meteo.drop(columns=["PM_PREFIX"], inplace=True)

def temperature(meteo):
    """Function that calculates monthly temperature."""

    #MEDIAN FOR EACH MONTH.
    for index, f in meteo[meteo["MAGNITUD"] == 83].iterrows():
        
        numbers = []

        for i in range(31):
            c = ""
            if (i < 9):
                c = "0"    
            c += str(i + 1)
        
            if f["V" + c] == "V":
                numbers.append(f["D" + c])
        
        ordered_numbers = sorted(numbers)

        if (len(ordered_numbers) == 0):
            median_temp = 0
        elif (len(ordered_numbers) % 2 == 0):
            median_temp = (ordered_numbers[len(ordered_numbers)// 2 - 1] + ordered_numbers[len(ordered_numbers)// 2]) / 2
        else:
            median_temp = ordered_numbers[len(ordered_numbers) // 2]
        
        meteo.at[index, "MONTHLY_TEMP"] = median_temp

def precipitacion(meteo):
    """Function that calculates monthly precipitations."""

    for index, f in meteo[meteo["MAGNITUD"] == 89].iterrows():
        sum = 0
        n = 0

        for i in range(31):
            c = ""
            if (i < 9):
                c = "0"    
            c += str(i + 1)
        
            if f["V" + c] == "V":
                sum += f["D" + c]
                n += 1
        
        meteo.at[index, "MONTHLY_PREC"] =  round(sum/n, 2)

def wind(meteo):
    """Function that determines whether there is strong wind or not."""

    for index, f in meteo[meteo["MAGNITUD"] == 81].iterrows():
        sum = 0
        n = 0

        for i in range(31):
            c = ""
            if (i < 9):
                c = "0"    
            c += str(i + 1)
        
            if f["V" + c] == "V":
                sum += f["D" + c]
                n += 1
        
        avg = round(sum/n, 2)

        strong = False
        if (avg > 10.8):
            strong = True
        
        meteo.at[index, "MONTHLY_STRONG_WIND"] =  strong

def mongodb_date(row):
    
    date = datetime(row["ANO"], row["MES"], 1)
    return date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def null_values(row):
    to_review = ["TEMPERATURA", "VIENTO_FUERTE", "PRECIPITACION"]
    
    for c in to_review:
        if pd.isnull(row[c]):
            row[c] = row["ID"] + "-" + c + "-desconocido"

    return row

def clean_meteo():
    # CLEANING ORIGINAL METEO
    meteo = pd.read_csv(os.path.join("files", "meteo24.csv"), sep=';')

    meteo["MONTHLY_DATE"] = meteo.apply(mongodb_date, axis=1)
    cp = pd.read_csv(os.path.join("files", "estaciones_meteo_CodigoPostal.csv"), sep=';')
    codPostal(meteo, cp)
    temperature(meteo)
    precipitacion(meteo)
    wind(meteo)

    meteo.to_csv(os.path.join("cleaned", "MeteoLimpio.csv"), header=True, sep=';', index=False)

    # GENERATING NEW METEO
    df = pd.DataFrame()

    # BASIC FIELDS + TEMPERATURE
    df["FECHA"] = meteo["MONTHLY_DATE"].unique()

    meteo_filtered = meteo.loc[
        meteo["MAGNITUD"] == 83, ["MONTHLY_DATE", "PROVINCIA", "MUNICIPIO", "ESTACION", "MONTHLY_TEMP"]]
    print(meteo_filtered.shape[0])
    meteo_filtered.rename(columns={'MONTHLY_DATE': 'FECHA'}, inplace=True)
    meteo_filtered.rename(columns={'MONTHLY_TEMP': 'TEMPERATURA'}, inplace=True)

    df = pd.merge(df, meteo_filtered, on=["FECHA"], how="left")

    # WIND

    meteo_filtered = meteo.loc[
        meteo["MAGNITUD"] == 81, ["MONTHLY_DATE", "PROVINCIA", "MUNICIPIO", "ESTACION", "MONTHLY_STRONG_WIND"]]
    print(meteo_filtered.shape[0])
    meteo_filtered.rename(columns={'MONTHLY_DATE': 'FECHA', 'MONTHLY_STRONG_WIND': 'VIENTO_FUERTE'}, inplace=True)

    # --- ADDING NO-MATCHING RESULTS WITH PREVIOUSLY ADDED METEOSTATIONS ---.
    df = pd.merge(df, meteo_filtered, on=["FECHA", "PROVINCIA", "MUNICIPIO", "ESTACION"], how="left")

    df['KEY'] = df[['FECHA', 'PROVINCIA', 'MUNICIPIO', 'ESTACION']].astype(str).agg('-'.join, axis=1)
    meteo_filtered['KEY'] = meteo_filtered[['FECHA', 'PROVINCIA', 'MUNICIPIO', 'ESTACION']].astype(str).agg('-'.join,
                                                                                                            axis=1)

    df_no_match = meteo_filtered[~meteo_filtered['KEY'].isin(df['KEY'])]

    df_no_match = df_no_match.drop(columns=['KEY'])
    df = df.drop(columns=['KEY'])

    meteo_filtered = meteo.loc[
        meteo.index.isin(df_no_match.index), ["MONTHLY_DATE", "PROVINCIA", "MUNICIPIO", "ESTACION", "MONTHLY_TEMP",
                                              "MONTHLY_STRONG_WIND"]]
    meteo_filtered.rename(
        columns={'MONTHLY_DATE': 'FECHA', 'MONTHLY_TEMP': 'TEMPERATURA', 'MONTHLY_STRONG_WIND': 'VIENTO_FUERTE'},
        inplace=True)
    df = pd.concat([df, meteo_filtered])

    # PRECIPITATIONS
    meteo_filtered = meteo.loc[
        meteo["MAGNITUD"] == 89, ["MONTHLY_DATE", "PROVINCIA", "MUNICIPIO", "ESTACION", "MONTHLY_PREC"]]
    meteo_filtered.rename(columns={'MONTHLY_DATE': 'FECHA'}, inplace=True)
    meteo_filtered.rename(columns={'MONTHLY_PREC': 'PRECIPITACION'}, inplace=True)

    df = pd.merge(df, meteo_filtered, on=["FECHA", "PROVINCIA", "MUNICIPIO", "ESTACION"], how="left")

    # COD_POSTAL
    meteo_filtered = meteo.loc[
        (meteo["MAGNITUD"] == 83) | meteo.index.isin(df_no_match.index), ["MONTHLY_DATE", "PROVINCIA", "MUNICIPIO",
                                                                          "ESTACION", "COD_POSTAL"]]
    meteo_filtered.rename(columns={'MONTHLY_DATE': 'FECHA'}, inplace=True)

    df = pd.merge(df, meteo_filtered, on=["FECHA", "PROVINCIA", "MUNICIPIO", "ESTACION"], how="left")

    # FILLING NULL VALUES:
    df['ID'] = df[['FECHA', 'PROVINCIA', 'MUNICIPIO', 'ESTACION']].astype(str).agg('_'.join, axis=1)
    df = df.apply(null_values, axis=1)

    df.to_csv(os.path.join("cleaned", "Meteo.csv"), header=True, sep=';', index=False)  # SAVE NEW FILE

if __name__ == "__main__":
    clean_meteo()