import pandas as pd
import os

def fill_missing_tipo(row,column,string_missing):
    if pd.isnull(row[column]):
        return f'{string_missing}_{row["NIF"]}'
    return row[column]

def format_phone_number(phone):
    phone = phone.replace(" ", "")
    if phone.startswith("+34"):
        phone = phone[3:]
    if phone.startswith("34"):
        phone = phone[2:]
    return phone


csv_input = "/Users/luciasotogarcia/PycharmProjects/mongo_processing2/files/UsuariosSucio.csv"

df = pd.read_csv(csv_input)
df["NOMBRE"] = df["NOMBRE"].str.lower()
df["EMAIL"] = df["EMAIL"].str.lower()
df["TELEFONO"] = df["TELEFONO"].apply(format_phone_number)
df["EMAIL"] = df.apply(lambda row: fill_missing_tipo(row, "EMAIL", "EMAIL_DESCONOCIDO"), axis=1)

df.to_csv(os.path.join("cleaned", "UsuariosLimpio.csv"), header=True, sep=',', index=False)