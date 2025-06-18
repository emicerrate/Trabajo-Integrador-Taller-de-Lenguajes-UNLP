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
    return df["PONDERA"].sum()

# Calculo cuantas viviendas hay por tipo
def get_housing_type_distribution(df):
    return df.groupby("IV1")["PONDERA"].sum().sort_values(ascending=False)

# Agrupo por aglomerado y calculo el material predominante en pisos
def get_floor_material_by_agglomerate(df):
    
    FLOOR_MATERIAL = {
        1: "mosaico / baldosa / madera /cerámica / alfombra",
        2: "cemento / ladrillo jo",
        3: "ladrillo suelto / tierra"
    }

    dict_ag_id = agglomeration_id()
    
    resultados = []

    for aglo_id, grupo in df.groupby("AGLOMERADO"):
        nombre_aglo = dict_ag_id.get(str(aglo_id), f"Aglomerado {aglo_id}")

        if grupo.empty or "PONDERA" not in grupo.columns:
            resultados.append({"Aglomerado": nombre_aglo, "Material Predominante": "Sin datos"})
            continue

        # Agrupar por material y sumar ponderación
        ponderado = grupo.groupby("IV3")["PONDERA"].sum()

        if ponderado.empty:
            material_nombre = "Sin datos"
        else:
            cod_material = ponderado.idxmax()
            material_nombre = FLOOR_MATERIAL.get(cod_material, f"Material {cod_material}")

        resultados.append({
            "Aglomerado": nombre_aglo,
            "Material Predominante": material_nombre
        })

    return pd.DataFrame(resultados)

# Calculo el porcentaje de viviendas con baño dentro del hogar por aglomerado
def get_bathroom_access_by_agglomerate(df):
    dict_ag_id = agglomeration_id()

    df = df.copy()
    df["TIENE_BANO"] = df["IV9"] == 1

    grouped = df.groupby("AGLOMERADO").apply(
        lambda g: (g.loc[g["TIENE_BANO"], "PONDERA"].sum() / g["PONDERA"].sum()) * 100
    ).reset_index(name="Porcentaje con baño (%)")

    grouped["Aglomerado"] = grouped["AGLOMERADO"].astype(str).map(dict_ag_id)
    return grouped[["Aglomerado", "Porcentaje con baño (%)"]].round(2)

# Calculo cuantas viviendas estan en villas de emergencia por aglomerado
def get_villas_by_agglomerate(df):
    dict_ag_id = agglomeration_id()
    resultados = []

    for aglo_id, grupo in df.groupby("AGLOMERADO"):
        nombre = dict_ag_id.get(str(aglo_id), f"Aglom {aglo_id}")
        total = grupo["PONDERA"].sum()
        en_villa = grupo.loc[grupo["IV12_3"] == 1, "PONDERA"].sum()
        porcentaje = round((en_villa / total) * 100, 2) if total > 0 else 0.0

        resultados.append({
            "Aglomerado": nombre,
            "Cantidad en Villas": en_villa,
            "Total": total,
            "Porcentaje": porcentaje
        })

    return pd.DataFrame(resultados)

# Calculo las condiciones de habitabilidad por aglomerado
def get_habitability_by_agglomerate(df):
    dict_ag_id = agglomeration_id()
    grouped = df.groupby(["AGLOMERADO", "CONDICION_DE_HABITABILIDAD"])["PONDERA"].sum().reset_index(name="Cantidad")

    total_por_aglo = grouped.groupby("AGLOMERADO")["Cantidad"].sum()
    grouped["Total"] = grouped["AGLOMERADO"].map(total_por_aglo)
    grouped["Porcentaje"] = (grouped["Cantidad"] / grouped["Total"] * 100).round(2)

    grouped["Aglomerado"] = grouped["AGLOMERADO"].astype(str).map(dict_ag_id)

    return grouped[["Aglomerado", "CONDICION_DE_HABITABILIDAD", "Cantidad", "Porcentaje"]]

def get_tenure_evolution_by_agglomerate(df, agglomerate, tenencias):
    from package.data_graphics.individuos import agglomeration_id

def get_tenure_evolution_named(df, agglomerate, selected_labels):

    # Diccionario oficial de códigos a nombres
    TENENCIA_LABELS = {
        1: "Propietario vivienda y terreno",
        2: "Propietario vivienda solo",
        3: "Inquilino / arrendatario",
        4: "Ocupante por impuestos/expensas",
        5: "Ocupante en relación laboral",
        6: "Ocupante con permiso",
        7: "Ocupante sin permiso",
        8: "Está en sucesión"
    }

    # Invertir el diccionario 
    label_to_code = {v: k for k, v in TENENCIA_LABELS.items()}

    # Filtrar por aglomerado y tenencias seleccionadas
    codigos_seleccionados = [label_to_code[label] for label in selected_labels if label in label_to_code]
    df_filtrado = df[(df["AGLOMERADO"] == agglomerate) & (df["II7"].isin(codigos_seleccionados))]

    # Agrupar y sumar ponderaciones
    agrupado = df_filtrado.groupby(["ANO4", "TRIMESTRE", "II7"])["PONDERA"].sum().reset_index()

    # Reemplazo codigo por nombres
    agrupado["II7"] = agrupado["II7"].map(TENENCIA_LABELS)

    pivot = agrupado.pivot_table(
        index=["ANO4", "TRIMESTRE"],
        columns="II7",
        values="PONDERA",
        fill_value=0
    ).reset_index()

    return pivot  