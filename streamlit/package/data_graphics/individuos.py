import pandas as pd
from st_constantes import DATA_OUT_PATH

def load_individual_data():
    """
    Carga el archivo de datos individuales y verifica columnas necesarias.
    """
    file_path = DATA_OUT_PATH / "usu_individual_final.csv"

    if not file_path.exists():
        raise FileNotFoundError("No se encontró el archivo procesado: usu_individual_final.csv")

    df = pd.read_csv(file_path)
    required_columns = {"ano4", "trimestre", "estado", "nivel_educativo"}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(f"Faltan columnas necesarias: {missing}")
    return df

def get_available_years(df):
    """
    Devuelve una lista ordenada de los años disponibles.
    """
    return sorted(df["ano4"].unique())

def filter_by_year_and_quarter(df, year, quarter):
    """
    Filtra el DataFrame por año y trimestre seleccionados.
    """
    return df[(df["ano4"] == year) & (df["trimestre"] == quarter)]

def get_unemployed_by_education(df):
    """
    Devuelve una serie con el conteo de personas desocupadas por nivel educativo.
    """
    unemployed = df[df["estado"] == "Desocupado"]
    return unemployed["nivel_educativo"].value_counts().sort_index()