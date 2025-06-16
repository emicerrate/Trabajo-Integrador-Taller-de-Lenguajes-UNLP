import pandas as pd
from st_constantes import DATA_OUT_PATH

# FUNCIONES PARA PAGINA 5

def load_individual_data():
    """
    Carga el archivo de datos individuales y verifica columnas necesarias.
    """
    file_path = DATA_OUT_PATH / "usu_individual_final.csv"

    if not file_path.exists():
        raise FileNotFoundError("No se encontró el archivo procesado: usu_individual_final.csv")

    df = pd.read_csv(file_path, encoding="latin-1", sep=";")
    required_columns = {"ANO4", "TRIMESTRE", "CONDICION_LABORAL", "NIVEL_ED_str"}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(f"Faltan columnas necesarias: {missing}")
    return df

def get_available_years(df):
    """
    Devuelve una lista ordenada de los años disponibles.
    """
    return sorted(df["ANO4"].unique())

def filter_by_year_and_quarter(df, year, quarter):
    """
    Filtra el DataFrame por año y trimestre seleccionados.
    """
    return df[(df["ANO4"] == year) & (df["TRIMESTRE"] == quarter)]

def get_unemployed_by_education(df):
    """
    Devuelve una serie con el conteo de personas desocupadas por nivel educativo.
    """
    unemployed = df[df["CONDICION_LABORAL"] == "Desocupado"]
    return unemployed["NIVEL_ED_str"].value_counts().sort_index()

def get_agglomerate_list(df):
    """
    Devuelve una lista ordenada de los aglomerados disponibles.
    """
    return sorted(df["AGLOMERADO"].unique())

def get_unemployment_rate_over_time(df, selected_agglomerate):
    """
    Devuelve un DataFrame con la evolución de la tasa de desempleo por período (AÑO + TRIMESTRE).
    Si se selecciona un aglomerado, se filtra por él.
    """

    # Se filtra por aglomerado si se selecciona uno (evitar "Todo el país")
    if selected_agglomerate != "Todo el país":
        df = df[df["AGLOMERADO"] == selected_agglomerate]

    # Se agrupa por año y trimestre
    grouped = df.groupby(["ANO4", "TRIMESTRE", "CONDICION_LABORAL"]).size().unstack(fill_value=0)

    # Asegurar que estén las columnas esperadas
    for col in ["Ocupado dependiente", "Ocupado autónomo", "Desocupado"]:
        if col not in grouped.columns:
            grouped[col] = 0

    # Calcular ocupados y tasa de desempleo
    grouped["ocupados"] = grouped["Ocupado dependiente"] + grouped["Ocupado autónomo"]
    grouped["desocupados"] = grouped["Desocupado"]
    grouped["tasa_desempleo"] = (grouped["desocupados"] / (grouped["ocupados"] + grouped["desocupados"])) * 100

    # Resetear índice y crear columna de período
    grouped = grouped.reset_index()
    grouped["periodo"] = grouped["ANO4"].astype(str) + "-T" + grouped["TRIMESTRE"].astype(str)

    return grouped[["periodo", "tasa_desempleo"]].sort_values("periodo")

def get_employment_rate_over_time(df, selected_agglomerate):
    """
    Devuelve un DataFrame con la evolución de la tasa de empleo por período (AÑO + TRIMESTRE).
    Si se selecciona un aglomerado, se filtra por él.
    """

    # Se filtra por aglomerado si se selecciona uno (evitar "Todo el país")
    if selected_agglomerate != "Todo el país":
        df = df[df["AGLOMERADO"] == selected_agglomerate]

    # Se agrupa por año, trimestre y condición laboral
    grouped = df.groupby(["ANO4", "TRIMESTRE", "CONDICION_LABORAL"]).size().unstack(fill_value=0)

    # Asegurar que estén las columnas esperadas
    for col in ["Ocupado dependiente", "Ocupado autónomo", "Desocupado"]:
        if col not in grouped.columns:
            grouped[col] = 0

    # Calcular ocupados y tasa de empleo
    grouped["ocupados"] = grouped["Ocupado dependiente"] + grouped["Ocupado autónomo"]
    grouped["desocupados"] = grouped["Desocupado"]
    grouped["tasa_empleo"] = (grouped["ocupados"] / (grouped["ocupados"] + grouped["desocupados"])) * 100

    # Resetear índice y crear columna de período
    grouped = grouped.reset_index()
    grouped["periodo"] = grouped["ANO4"].astype(str) + "-T" + grouped["TRIMESTRE"].astype(str)

    return grouped[["periodo", "tasa_empleo"]].sort_values("periodo")