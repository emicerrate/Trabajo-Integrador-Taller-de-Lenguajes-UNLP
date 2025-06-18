import pandas as pd
from datetime import datetime
from st_constantes import DATA_OUT_PATH, DATA_PATH

def load_hogar_data():
    """
    Carga el archivo de datos individuales y verifica columnas necesarias.
    """
    file_path = DATA_OUT_PATH / "usu_hogar_final.csv"

    if not file_path.exists():
        raise FileNotFoundError("No se encontró el archivo: usu_hogar_final.csv")

    df = pd.read_csv(file_path, encoding="latin-1", sep=";")
    
    return df

def load_basket_data():
    """
    Carga el archivo de datos individuales y verifica columnas necesarias.
    """
    file_path = DATA_PATH / "valores-canasta-basica-alimentos-canasta-basica-total-mensual-2016.csv"

    if not file_path.exists():
        raise FileNotFoundError("No se encontró el archivo de canasta básica de alimentos")

    df = pd.read_csv(file_path, encoding="latin-1", sep=",")
    return df

def basket_cost_per_quarter(df_basket, year, quarter):
    min_date = datetime(year, 3*quarter - 2, 1)
    max_date = datetime(year, 3*quarter, 30)
    df_basket["indice_tiempo"] = pd.to_datetime(df_basket["indice_tiempo"])
    df_basket_filtered = df_basket[(df_basket.indice_tiempo>=min_date) & (df_basket.indice_tiempo<max_date)]
    return df_basket_filtered["canasta_basica_alimentaria"]
    

def homes_under_poverty_indigence(homes, basket):
    homes_filtered = homes[homes["IX_TOT"]=="4"]
    homes_quantity = homes_filtered.count()
    under_poverty_quantity = homes_filtered[homes_filtered]