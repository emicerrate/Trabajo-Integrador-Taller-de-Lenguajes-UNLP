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

def agglomeration_id():
    dict_ag_id = {
    "2" : "Gran La Plata",
    "3" : "Bahía Blanca - Cerri",
    "4" : "Gran Rosario",
    "5" : "Gran Santa Fé",
    "6" : "Gran Paraná",
    "7" : "Posadas",
    "8" : "Gran Resistencia",
    "9" : "Comodoro Rivadavia - Rada Tilly",
    "10" : "Gran Mendoza",
    "12" : "Corrientes",
    "13" : "Gran Córdoba",
    "14" : "Concordia",
    "15" : "Formosa",
    "17" : "Neuquén – Plottier",
    "18" : "Santiago del Estero - La Banda",
    "19" : "Jujuy - Palpalá",
    "20" : "Río Gallegos",
    "22" : "Gran Catamarca",
    "23" : "Gran Salta",
    "25" : "La Rioja",
    "26" : "Gran San Luis",
    "27" : "Gran San Juan",
    "29" : "Gran Tucumán - Tafí Viejo",
    "30" : "Santa Rosa – Toay",
    "31" : "Ushuaia - Río Grande",
    "32" : "Ciudad Autónoma de Buenos Aires",
    "33" : "Partidos del GBA",
    "34" : "Mar del Plata",
    "36" : "Río Cuarto",
    "38" : "San Nicolás – Villa Constitución",
    "91" : "Rawson – Trelew",
    "93" : "Viedma – Carmen de Patagones"
    }
    return dict_ag_id

# Carga los datos de hogares con las columnas necesarias
def load_hogar_data_04():
    file_path = DATA_OUT_PATH / "usu_hogar_final.csv"

    if not file_path.exists():
        raise FileNotFoundError("No se encontró el archivo procesado: usu_hogar_final.csv")

    df = pd.read_csv(file_path, encoding="latin-1", sep=";") # Uso latin-1 para acentos

    required_columns = {
        "ANO4", "TRIMESTRE", "AGLOMERADO", "CODUSU",
        "IV1", "IV3", "IV9",
        "IV12_3", "CONDICION_DE_HABITABILIDAD"
    }
    
    # Verifico si las columnas necesarias estan en el dataframe, si no informo el error
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(f"Faltan columnas necesarias: {missing}")

    return df

# Devuelvo una lista de años disponibles(unicos) en el dataframe
def get_available_years(df):
    return sorted(df["ANO4"].unique())

# Calculo el total de viviendas 
def get_total_houses(df):
    return df["CODUSU"].nunique()

# Calculo cuantas viviendas hay por tipo
def get_housing_type_distribution(df):
    return df["IV1"].value_counts()

# Agrupo por aglomerado y calculo el material predominante en pisos
def get_floor_material_by_agglomerate(df):
    
    dict_ag_id = agglomeration_id()

    aglomerados = []

    for aglo_id, grupo in df.groupby("AGLOMERADO"):
        nombre_aglo = dict_ag_id.get(str(aglo_id), f"Aglom {aglo_id}")
        if grupo["IV3"].mode().empty:
            material = "Sin datos"
        else:
            material = grupo["IV3"].mode().iloc[0]

        aglomerados.append({
            "Aglomerado": nombre_aglo,
            "Material Predominante": material
        })

    return pd.DataFrame(aglomerados)

# Calculo el porcentaje de viviendas con baño dentro del hogar por aglomerado
def get_bathroom_access_by_agglomerate(df):
    dict_ag_id = agglomeration_id()

    df = df.copy()
    df["TIENE_BANO"] = df["IV9"] == 1

    porcentajes = df.groupby("AGLOMERADO")["TIENE_BANO"].mean() * 100

    porcentajes.index = porcentajes.index.astype(str).map(dict_ag_id)

    result = porcentajes.reset_index()
    result.columns = ["AGLOMERADO", "Porcentaje con baño (%)"]

    return result.round(2)

# Calculo cuantas viviendas estan en villas de emergencia por aglomerado
def get_villas_by_agglomerate(df):
    dict_ag_id = agglomeration_id()
    resultados = []

    for aglo_id, grupo in df.groupby("AGLOMERADO"):
        nombre = dict_ag_id.get(str(aglo_id), f"Aglom {aglo_id}")
        total = len(grupo)
        en_villa = (grupo["IV12_3"] == 1).sum()  
        porcentaje = round((en_villa / total) * 100, 2) if total > 0 else 0.0

        resultados.append({
            "Aglomerado": nombre,
            "Total": total,
            "Cantidad en Villas": en_villa,
            "Porcentaje": porcentaje
        })

    return pd.DataFrame(resultados)

# Calculo las condiciones de habitabilidad por aglomerado
def get_habitability_by_agglomerate(df):
    dict_ag_id = agglomeration_id()
    grouped = df.groupby(["AGLOMERADO", "CONDICION_DE_HABITABILIDAD"]).size().reset_index(name="Cantidad") 
    totales = grouped.groupby("AGLOMERADO")["Cantidad"].sum()
    grouped["Total"] = grouped["AGLOMERADO"].map(totales)
    grouped["Porcentaje"] = ((grouped["Cantidad"] / grouped["Total"]) * 100).round(2)
    grouped["Aglomerado"] = grouped["AGLOMERADO"].astype(str).map(dict_ag_id)
    return grouped[["Aglomerado", "CONDICION_DE_HABITABILIDAD", "Cantidad", "Porcentaje"]]     