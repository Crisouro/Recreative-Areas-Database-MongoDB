import pandas as pd
import os 

def limpieza_area(df):
    pass

def limpieza_encuestas(df):
    pass

def limpieza_incidencias(df):
    pass

def limpieza_incidentes(df):
    pass

def limpieza_mantenimiento(df):
    pass

def limpieza_usuarios(df):
    pass

def limpieza_juegos(df):
    pass

def limpieza_meteo(df):
    pass

if __name__ == "__main__":

    df_area = pd.read_csv(os.path.join("datasets", "Areas.csv"), sep=',', index_col=0)
    df_encuestas = pd.read_csv(os.path.join("datasets", "Dirty_EncuestaSatisfaccion.csv"), sep=',', index_col=0)
    df_incidencias = pd.read_csv(os.path.join("datasets", "Dirty_Incidencias.csv"), sep=',', index_col=0)
    df_incidentes = pd.read_csv(os.path.join("datasets", "Dirty_IncidenteSeguridad.csv"), sep=',', index_col=0)
    df_mantenimientos = pd.read_csv(os.path.join("datasets", "Dirty_Mantenimientos.csv"), sep=',', index_col=0)
    df_usuarios = pd.read_csv(os.path.join("datasets", "Dirty_Usuarios.csv"), sep=',', index_col=0)
    df_juegos = pd.read_csv(os.path.join("datasets", "Juegos.csv"), sep=',', index_col=0)
    df_meteo = pd.read_csv(os.path.join("datasets", "Meteo.csv"), sep=',', index_col=0)

    limpieza_area(df_area)
    limpieza_encuestas(df_encuestas)
    limpieza_incidencias(df_incidencias)
    limpieza_incidentes(df_incidentes)
    limpieza_mantenimiento(df_mantenimientos)
    limpieza_usuarios(df_usuarios)
    limpieza_juegos(df_juegos)
    limpieza_meteo(df_meteo)