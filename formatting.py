import unicodedata
import re
from datetime import datetime
import pandas as pd
import pyproj

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
        
        print("[FORMATTING][NORMALIZING][", c ,"] Checked")
        #print(c, ": ", df[c].unique())

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

def date_typo_format(df, c_date):
    """Function for solving typographic errors."""

    def aplicar_regex(x):
        if pd.isnull(x):  
            return x
        else:
            return date_unifier(x)
                    
    df[c_date] = df[c_date].apply(lambda x: aplicar_regex(x))

    print("[FORMATTING][DATE] Checked")


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
    if email is not None and isinstance(email, str) and email.startswith("dup_"):
        return email[4:]  # Quita los primeros 4 caracteres ("dup_")
    return email


def format_mantenimiento_ID(id_column) -> dict:
    new_id = []
    for i in range(len(id_column)):
        item = id_column[i].strip()
        num, letters = item.split(",00")
        new_id.append(f"{letters}{num.zfill(6)}")
    return new_id

def fix_accent_street_name(data, column= "NOM_VIA"):
    for i in range(len(data)):
        dir = data.iloc[i][column]

        if type(dir) == str and "'" in dir:
            data.at[i, column] = dir.replace("'", "")

def spacial_coordenates_area(df_data: dict):
   """This function transforms the latitude and longitude into a single column"""
   #Unpacking needed data
   x_column= df_data['LONGITUD']
   y_column = df_data['LATITUD']
   new_coord =[]

   for i in range(len(x_column)):
       #data transformation into a longitude-latitude pair.
       x = float(x_column[i])
       y = float(y_column[i])
       new_coord.append([x, y])

   #Seting up the new dataset structure
   df_data.drop(columns=['SISTEMA_COORD'], inplace=True)
   df_data['COORD_GIS'], df_data['SISTEMA_COORD'] = new_coord, ['WGS84']*len(df_data)
   #df_data.rename(columns={"COORD_GIS_X": "COORD_GIS"})
   #df_data.drop(columns=['COORD_GIS_Y', 'LATITUD', 'LONGITUD'], inplace=True)

def spacial_coordenates_juego(df_data: dict):
    """This function transforms the UTM coordinate columns into a single longitude-latitude column"""
    x_column = df_data['COORD_GIS_X']
    y_column = df_data['COORD_GIS_Y']
    new_coord = []
    # UTM configuration to Madrid area
    transformer = pyproj.Transformer.from_crs("EPSG:25830", "EPSG:4326", always_xy=True)

    for i in range(len(x_column)):
        if type(x_column[i]) != str and type(y_column[i]) != str:
        # data transformation into a longitude-latitude pair.
            x = float(x_column[i])
            y = float(y_column[i])
            x,y = transformer.transform(x, y)
            new_coord.append([x,y])
        else:
            new_coord.append(str(df_data.at[i, "ID"]) + "COOR_GIS-desconocidas")

    # Seting up the new dataset structure
    df_data.drop(columns=['SISTEMA_COORD'], inplace=True)
    df_data['COORD_GIS'], df_data['SISTEMA_COORD'] = new_coord, ['WGS84'] * len(df_data)
    #df_data.rename(columns={"COORD_GIS_X": "COORD_GIS"})
    #df_data.drop(columns=['COORD_GIS_Y'], inplace=True)
