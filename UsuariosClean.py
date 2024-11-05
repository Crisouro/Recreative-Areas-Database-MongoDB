import pandas as pd
import os
from unidecode import unidecode

def rellenar_null(row,column,data_missing):
    """Funcion para gestionar los valores nulos"""
    if pd.isnull(row[column]):
        return f'{row["NIF"]}-{data_missing}'
    return row[column]

def format_phone_number(phone):
    """Funcion para poner todos los numeros de telefono en el mismo formato"""
    phone = phone.replace(" ", "")
    if phone.startswith("+34"):
        phone = phone[3:]
    if phone.startswith("34"):
        phone = phone[2:]
    return phone

def remove_dup_prefix(email):
    # Si el email empieza con 'dup_', quitar esa parte
    if isinstance(email, str) and email.startswith("dup_"):
        return email[4:]  # Quita los primeros 4 caracteres ("dup_")
    return email

#Cambiar por la ruta en la que se encuentre el fichero UsuariosSucio.csv
csv_input = "/Users/luciasotogarcia/PycharmProjects/mongo_processing2/files/UsuariosSucio.csv"

df = pd.read_csv(csv_input)
df["NOMBRE"] = df["NOMBRE"].str.lower() #nombre en minusculas
df["NOMBRE"] =df["NOMBRE"].apply(unidecode) #nombre sin tildes
df["EMAIL"] = df["EMAIL"].str.lower() #mail en minusculas
df["TELEFONO"] = df["TELEFONO"].apply(format_phone_number)
df["EMAIL"] = df.apply(lambda row: rellenar_null(row, "EMAIL", "desconocido"), axis=1)
df["EMAIL"] = df["EMAIL"].apply(remove_dup_prefix)
df.drop_duplicates(subset=["NIF", "TELEFONO", "EMAIL"], keep='first')

#Crear una carpeta cleaned en el directorio del proyecto si no se tiene
df.to_csv(os.path.join("cleaned", "UsuariosLimpio.csv"), header=True, sep=',', index=False)