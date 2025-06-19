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
def load_individual_data_05():
    """
    Carga solo las columnas necesarias del archivo de datos individuales.
    """
    file_path = DATA_OUT_PATH / "usu_individual_final.csv"

    if not file_path.exists():
        raise FileNotFoundError("No se encontró el archivo procesado: usu_individual_final.csv")

    columnas_utilizadas = [
        "ANO4",
        "TRIMESTRE",
        "CONDICION_LABORAL",
        "NIVEL_ED_str",
        "PONDERA",
        "AGLOMERADO",
        "PP04A"
    ]

    df = pd.read_csv(
        file_path,
        encoding="latin-1",
        sep=";",
        usecols=columnas_utilizadas,
        low_memory=False
    )
    return df

def get_available_years(df):
    """
    Devuelve una lista ordenada de los años disponibles.
    """
    return sorted(df["ANO4"].unique())

def get_available_quarters(df, year):
    """Devuelve los trimestres disponibles para determinado año"""
    dff = df[df.ANO4==year]
    return sorted(dff["TRIMESTRE"].unique())

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

# FUNCIONES PARA PÁGINA 2
def load_individual_data_02():
    """
    Carga solo las columnas necesarias del archivo de datos individuales para la página 2.
    Args:
        None.
    Returns:
        df (dataframe): Dataframe con las columnas necesarias para la página 2. 
    """
    file_path = DATA_OUT_PATH / "usu_individual_final.csv"

    if not file_path.exists():
        raise FileNotFoundError("No se encontró el archivo procesado: usu_individual_final.csv")

    columnas_utilizadas = [
        "ANO4",
        "TRIMESTRE",
        "CONDICION_LABORAL",
        "NIVEL_ED_str",
        "PONDERA",
        "AGLOMERADO",
        "PP04A"
    ]

    df = pd.read_csv(file_path, encoding="latin-1", sep=";", low_memory=False)
    return df

def media_and_median_last_quarter(df):
    """
    Calcula para cada trimestre cargado la media y la mediana de su edad.
    Args:
        df (dataframe): Dataframe con la información de las personas.
    Returns:
        grouped_df (dataframe): Dataframe agrupado por año y trimestre con la media y mediana de edad para cada trimestre.
    """
    grouped_df = df.groupby(["ANO4", "TRIMESTRE"])["CH06"].agg(MEDIA="mean", MEDIANA="median").reset_index()
    grouped_df.rename(columns={"ANO4": "AÑO"}, inplace=True)
    return grouped_df

def age_media_per_conglomerate(df):
    """
    Calcula el promedio de edad por aglomerado para el último trimestre cargado.
    Args:
        df (dataframe): Dataframe con la información de las personas.
    Returns:
        grouped_df (dataframe): Dataframe agrupado por aglomerado y con el promedio de edad para cada uno.
    """
    dict_ag_id = agglomeration_id()
    max_year = max(get_available_years(df))
    max_quarter = max(get_available_quarters(df, max_year))

    # Filtro el dataframe para el último año y trimestre
    df_last_quarter = df[(df["ANO4"]==max_year) & (df["TRIMESTRE"]==max_quarter)]

    # Agrupo el dataframe por aglomerado y le calculo el promedio de edad para cada uno
    grouped_df = df_last_quarter.groupby("AGLOMERADO")["CH06"].agg(PROMEDIO="mean").reset_index()
    
    # Renombro la columna del promedio y para cada aglomerado pongo su nombre
    grouped_df.rename(columns={"PROMEDIO": "PROMEDIO DE EDAD"}, inplace=True)
    grouped_df["AGLOMERADO"] = grouped_df["AGLOMERADO"].astype(str).map(dict_ag_id)

    return grouped_df

def calculate_dp(group):
    """
    Calcula la dependencia demográfica para un trimestre.
    Args:
        group (dataframe): Dataframe con toda la información de personas para un trimestre y año específicos.
    Returns:
        float: Valor de la dependencia demográfica para el trimestre.
    """
    inactive = group[(group["CH06"]<=14) | (group["CH06"]>=65)].shape[0]
    active = group[group["CH06"].between(15, 64)].shape[0]
    return 100 * (inactive/active)

def demography_dependency(df, conglomerate):
    """
    Calcula para un aglomerado dado la dependencia demográfica para cada trimestre cargado.
    Args:
        df (dataframe): Dataframe con la información de las personas.
        conglomerate (str): Id del conglomerado al cual le calcularemos.
    Returns:
        grouped_df (dataframe): Dataframe con información de un aglomerado agrupado por año y trimestre y con 
        la dependencia demográfica para cada trimestre.
    """
    df_conglomerate = df[df["AGLOMERADO"]==int(conglomerate)]
    grouped_df = df_conglomerate.groupby(["ANO4","TRIMESTRE"]).apply(calculate_dp).reset_index(name="DEPENDENCIA DEMOGRÁFICA")
    grouped_df["PERÍODO"] = grouped_df["ANO4"].astype(str) + "-T" + grouped_df["TRIMESTRE"].astype(str)
    grouped_df.rename(columns={"ANO4": "AÑO"}, inplace=True)
    return grouped_df