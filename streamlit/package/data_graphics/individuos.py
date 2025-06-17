import pandas as pd
import json
from st_constantes import DATA_OUT_PATH, DATA_PATH

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

def load_agglomerate_geodata():
    """
    Carga el archivo JSON llamado 'aglomerados_coordenadas.json' desde DATA_PATH
    y devuelve un DataFrame con columnas: AGLOMERADO, nombre, lat, lon.
    """
    filepath = DATA_PATH / "aglomerados_coordenadas.json"

    if not filepath.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {filepath}")

    with open(filepath, encoding="utf-8") as f:
        raw_data = json.load(f)

    records = []
    for aglo_id, info in raw_data.items():
        lat, lon = info["coordenadas"]
        records.append({
            "AGLOMERADO": int(aglo_id),
            "nombre": info["nombre"],
            "lat": lat,
            "lon": lon
        })

    return pd.DataFrame(records)

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
    Devuelve una serie con el total ponderado de personas desocupadas por nivel educativo.
    """
    unemployed = df[df["CONDICION_LABORAL"] == "Desocupado"]
    return (
        unemployed.groupby("NIVEL_ED_str")["PONDERA"].sum().sort_index()
    )

def get_agglomerate_list(df):
    """
    Devuelve una lista ordenada de los aglomerados disponibles.
    """
    return sorted(df["AGLOMERADO"].unique())

def get_unemployment_rate_over_time(df, selected_agglomerate):
    """
    Devuelve un DataFrame con la evolución de la tasa de desempleo ponderada por período (AÑO + TRIMESTRE).
    Si se selecciona un aglomerado, se filtra por él.
    """

    # Filtrar por aglomerado si corresponde
    if selected_agglomerate != "Todo el país":
        df = df[df["AGLOMERADO"] == selected_agglomerate]

    # Agrupar por año, trimestre y condición laboral y sumar PONDERA
    grouped = df.groupby(["ANO4", "TRIMESTRE", "CONDICION_LABORAL"])["PONDERA"].sum().unstack(fill_value=0)

    # Asegurar que estén las columnas necesarias
    for col in ["Ocupado dependiente", "Ocupado autónomo", "Desocupado"]:
        if col not in grouped.columns:
            grouped[col] = 0

    # Calcular ocupados y tasa de desempleo ponderada
    grouped["ocupados"] = grouped["Ocupado dependiente"] + grouped["Ocupado autónomo"]
    grouped["desocupados"] = grouped["Desocupado"]
    grouped["tasa_desempleo"] = (grouped["desocupados"] / (grouped["ocupados"] + grouped["desocupados"])) * 100

    # Crear columna de período
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

    # Se agrupa por año, trimestre y condición laboral y se suma la columna PONDERA
    grouped = df.groupby(["ANO4", "TRIMESTRE", "CONDICION_LABORAL"])["PONDERA"].sum().unstack(fill_value=0)

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

def get_employment_distribution_by_agglomerate(df, selected_year2, selected_quarter2):
    dict_ag_id = agglomeration_id()

    # Filtrar por año y trimestre seleccionados
    df = df[(df["ANO4"] == selected_year2) & (df["TRIMESTRE"] == selected_quarter2)]

    # Filtrar solo ocupados
    ocupy = df[df["CONDICION_LABORAL"].isin(["Ocupado dependiente", "Ocupado autónomo"])]

    # Agrupar por aglomerado y tipo de empleo (PP04A), sumando las ponderaciones
    distribution = ocupy.groupby(["AGLOMERADO", "PP04A"])["PONDERA"].sum().unstack(fill_value=0)

    for col in [1, 2, 3]:
        if col not in distribution.columns:
            distribution[col] = 0

    distribution["total_ocupados"] = distribution[1] + distribution[2] + distribution[3]

    distribution["% estatal"] = (distribution[1] / distribution["total_ocupados"]) * 100
    distribution["% privado"] = (distribution[2] / distribution["total_ocupados"]) * 100
    distribution["% otro"] = (distribution[3] / distribution["total_ocupados"]) * 100

    distribution = distribution.reset_index()
    distribution["AGLOMERADO"] = distribution["AGLOMERADO"].astype(str).map(dict_ag_id)
    distribution = distribution.sort_values("AGLOMERADO")
    distribution = distribution.set_index("AGLOMERADO")

    return distribution[["total_ocupados", "% estatal", "% privado", "% otro"]]

def get_employment_unemployment_by_agglomerate_extremes(df):
    """
    Devuelve un DataFrame con la tasa de empleo y desempleo por aglomerado
    para el período más antiguo y el más reciente del dataset.
    """
    # Se carga la geolocalización desde el JSON con DATA_PATH
    geo_df = load_agglomerate_geodata()

    # Se obtiene los años y trimestres únicos ordenados
    periodos = df[["ANO4", "TRIMESTRE"]].drop_duplicates().sort_values(["ANO4", "TRIMESTRE"])
    if periodos.empty:
        return pd.DataFrame()

    # Obtenemos el período más antiguo y más reciente
    periodo_min = periodos.iloc[0]
    periodo_max = periodos.iloc[-1]

     # Filtrar dataset para solo esos dos períodos
    df_filtrado = df[
        ((df["ANO4"] == periodo_min["ANO4"]) & (df["TRIMESTRE"] == periodo_min["TRIMESTRE"])) |
        ((df["ANO4"] == periodo_max["ANO4"]) & (df["TRIMESTRE"] == periodo_max["TRIMESTRE"]))
    ]

    # Agrupar por aglomerado, año, trimestre y condición laboral
    grouped = df_filtrado.groupby(["AGLOMERADO", "ANO4", "TRIMESTRE", "CONDICION_LABORAL"])["PONDERA"].sum().unstack(fill_value=0)

    for col in ["Ocupado dependiente", "Ocupado autónomo", "Desocupado"]:
        if col not in grouped.columns:
            grouped[col] = 0

    grouped["ocupados"] = grouped["Ocupado dependiente"] + grouped["Ocupado autónomo"]
    grouped["desocupados"] = grouped["Desocupado"]
    grouped["total"] = grouped["ocupados"] + grouped["desocupados"]

    grouped["tasa_empleo"] = (grouped["ocupados"] / grouped["total"]) * 100
    grouped["tasa_desempleo"] = (grouped["desocupados"] / grouped["total"]) * 100

    grouped = grouped.reset_index()
    grouped["periodo"] = grouped["ANO4"].astype(str) + "-T" + grouped["TRIMESTRE"].astype(str)

    # Resetear índice y crear columna período
    # Pivotear para tener aglomerados como índice y columnas separadas por período
    # Aplanar columnas
    table = grouped.pivot(index="AGLOMERADO", columns="periodo", values=["tasa_empleo", "tasa_desempleo"])
    table.columns = [f"{metrico}_{periodo}" for metrico, periodo in table.columns]
    table = table.reset_index()

    # Reemplazar ID de aglomerado por nombre
    nombre_map = geo_df.set_index("AGLOMERADO")["nombre"].to_dict()
    lat_map = geo_df.set_index("AGLOMERADO")["lat"].to_dict()
    lon_map = geo_df.set_index("AGLOMERADO")["lon"].to_dict()

    #Se agrega la geolocalizacion

    table["nombre"] = table["AGLOMERADO"].map(nombre_map)
    table["lat"] = table["AGLOMERADO"].map(lat_map)
    table["lon"] = table["AGLOMERADO"].map(lon_map)

    return table