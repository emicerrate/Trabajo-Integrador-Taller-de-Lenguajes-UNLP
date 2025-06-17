import streamlit as st
from st_constantes import DATA_OUT_PATH
import folium
from streamlit_folium import st_folium  # para mostrar el mapa en Streamlit

from package.data_graphics.individuos import (
    agglomeration_id,
    load_individual_data,
    get_available_years,
    filter_by_year_and_quarter,
    get_unemployed_by_education,
    get_unemployment_rate_over_time,
    get_employment_rate_over_time,
    get_employment_distribution_by_agglomerate,
    get_employment_unemployment_by_agglomerate_extremes
)

from package.data_graphics.map_utils import (
    generate_map,
    add_marker
)

st.title("Actividad y empleo")
st.subheader("Personas desocupadas según estudios alcanzados")

# Se Carga el archivo usu_individual_final.csv
try:
    df = load_individual_data()
except (FileNotFoundError, ValueError) as e:
    st.error(str(e))
    st.stop()

available_years = get_available_years(df)
selected_year = st.selectbox("Año", available_years, index=len(available_years) - 1)
selected_quarter = st.selectbox("Trimestre", [1, 2, 3, 4])

filtered_df = filter_by_year_and_quarter(df, selected_year, selected_quarter)

if filtered_df.empty:
    st.warning(f"No hay datos para el {selected_quarter}° trimestre de {selected_year}.")
    st.stop()

education_counts = get_unemployed_by_education(filtered_df)

st.markdown("### Gráfico de desocupados por nivel educativo")
st.bar_chart(education_counts)

# 1.5.2 EVOLUCIÓN DEL DESEMPLEO

# Obtener diccionario de aglomerados
dict_ag_id = agglomeration_id()
dict_name_to_id = {v: k for k, v in dict_ag_id.items()}

# Lista de aglomerados con nombres
agglomerates = ["Todo el país"] + sorted(dict_name_to_id.keys())

st.markdown("### Evolución tasa de desempleo")

"""
Se informa la evolución del desempleo (tasa de empleo) a lo largo del tiempo. 
Elegir aglomerado o para todo el país.
"""

# Selector de aglomerado (por nombre)
selected_agglomerate_name = st.selectbox("Aglomerado", agglomerates)

# Obtener código correspondiente
if selected_agglomerate_name == "Todo el país":
    selected_agglomerate = "Todo el país"
else:
    selected_agglomerate = dict_name_to_id[selected_agglomerate_name]

# Obtener la evolución de la tasa de desempleo
unemployment_df = get_unemployment_rate_over_time(df, selected_agglomerate)

if unemployment_df.empty:
    st.warning("No hay datos disponibles para la selección.")
else:
    st.line_chart(
        unemployment_df.set_index("periodo")["tasa_desempleo"],
        use_container_width=True
    )

# 1.5.3 EVOLUCIÓN DEL EMPLEO

st.markdown("### Evolución de la tasa de empleo")

"""
Se informa la evolución del empleo (tasa de empleo) a lo largo del tiempo. 
Elegir aglomerado o para todo el país.
"""

# Segundo selector (por nombre, con otra clave)
selected_agglomerate_name2 = st.selectbox("Aglomerado", agglomerates, key="emp_agglom")

# Obtener código correspondiente
if selected_agglomerate_name2 == "Todo el país":
    selected_agglomerate2 = "Todo el país"
else:
    selected_agglomerate2 = dict_name_to_id[selected_agglomerate_name2]

# Obtener la evolución de la tasa de empleo
employment_df = get_employment_rate_over_time(df, selected_agglomerate2)

if employment_df.empty:
    st.warning("No hay datos disponibles para la selección.")
else:
    st.line_chart(
        employment_df.set_index("periodo")["tasa_empleo"],
        use_container_width=True
    )

# 1.5.4 DISTRIBUCION DEL EMPLEO

st.markdown("### Distribución del tipo de empleo por aglomerado")

# Selector año y trimestre (por nombre, con otra clave)
selected_year2 = st.selectbox("Año", available_years, index=len(available_years) - 1, key="selected_year_2")
selected_quarter2 = st.selectbox("Trimestre", [1, 2, 3, 4], key="selected_quarter_2")


distribution_df = get_employment_distribution_by_agglomerate(df, selected_year2, selected_quarter2)



st.dataframe(
    distribution_df.style.format({
        "total_ocupados": "{:,.0f}",
        "% estatal": "{:.2f}%",
        "% privado": "{:.2f}%",
        "% otro": "{:.2f}%"
    }),
    height=600  # opcional, para que tenga scroll vertical si es mucha info
)

# 1.5.5 MAPA DE EMPLEO Y DESEMPLEO

st.markdown("### Tasa de empleo y desempleo por aglomerado")

df_rates = get_employment_unemployment_by_agglomerate_extremes(df)  

# Seleccionar columnas a mostrar
cols_a_mostrar = ["nombre"] + [col for col in df_rates.columns if col.startswith("tasa_")]

# Renombrar columnas para que se vean más claras
rename = {
    col: col.replace("tasa_empleo", "Tasa de Empleo").replace("tasa_desempleo", "Tasa de Desempleo")
    for col in cols_a_mostrar if col != "nombre"
}

# Aplicar el renombramiento
df_formateado = df_rates[cols_a_mostrar].rename(columns=rename)

# Mostrar DataFrame con formato de porcentaje
st.dataframe(
    df_formateado.style.format(
        {col: "{:.2f}%" for col in df_formateado.columns if col != "nombre"}
    ),
    height=600
)

st.markdown("### Mapa de tasa de empleo y desempleo por aglomerado")

selected_rate = st.selectbox("Elige la tasa a visualizar:", ["empleo", "desempleo"])

# Se genera el mapa
map = generate_map()

df_rates.apply(lambda row: add_marker(row, map, selected_rate), axis=1)

st_folium(map, width=700, height=500)