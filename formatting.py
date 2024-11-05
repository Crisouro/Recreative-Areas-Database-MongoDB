import unicodedata
import re
from datetime import datetime
import pandas as pd

def general_format(df):
    """Function responsible for normalizing string data."""
    for c in df.select_dtypes(include=['object']).columns:

        def string_formatting(x):
            #Tipography correction.
            if (isinstance(x, str)):
                normalize_text = unicodedata.normalize('NFD', x)
                x = ''.join(c for c in normalize_text if unicodedata.category(c) != 'Mn')
                return x.lower()
            return x

        df[c] = df[c].apply(lambda x: string_formatting(x))

        print(c, ": ", df[c].unique())

def date_unifier(str):
    output_pattern = "%Y-%m-%dT%H:%M:%S.%fZ"
    
    if (str == "fecha_incorrecta"):
        return None

    possible_patterns = [
        "%d/%m/%Y",   # D/M/Y
        "%d-%m-%Y",
        "%m-%d-%Y",   # M-D-Y
        "%Y-%m-%d",   # Y-M-D
        "%d %m %Y",   # D M Y
        "%Y/%m/%d",   # Y/M/D
        "%B %d, %Y",  # M D, Y
        "%b %d, %Y",  # m D, Y
        "%d %B %Y",   # d M Y
        "%d %b %Y",    # d m Y
        "%d/%m/%y",
        "%Y-%m-%d %H:%M:%S"
    ]
    
    for p in possible_patterns:
        try:
            date = datetime.strptime(str, p)
            return date.strftime(output_pattern)
        except ValueError:
            continue  
    
    raise ValueError("El formato de fecha no es reconocido")

def typo_format(df, c_format):
    """Function for solving typographic errors."""

    if (len(c_format.keys()) != 0):
        
        for c, json in c_format.items():
            if ("FECHA" not in c):
                for field, value in json.items():
                    df[c][df[c] == field] = df[c][df[c] == field].apply(lambda x: value)
            else:
                regex = re.compile(json["pattern"])

                def aplicar_regex(x, regex):
                    if pd.isnull(x):  
                        return x
                    else:
                        return date_unifier(x)
                    
                df[c] = df[c].apply(lambda x: aplicar_regex(x, regex))


def format_phone_number(phone):
    # Eliminar todos los espacios del teléfono
    phone = phone.replace(" ", "")

    # Añadir el prefijo '+' si no está presente
    if not phone.startswith("+"):
        phone = "+" + phone

    return phone

def remove_dup_prefix(email):
    # Si el email empieza con 'dup_', quitar esa parte
    if isinstance(email, str) and email.startswith("dup_"):
        return email[4:]  # Quita los primeros 4 caracteres ("dup_")
    return email

