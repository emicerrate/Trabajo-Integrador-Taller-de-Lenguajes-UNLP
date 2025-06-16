import streamlit as st
from st_constantes import DATA_OUT_PATH

from package.data_graphics.individuos import (
    get_agglomerate_list,
    agglomeration_id,
    load_individual_data,
    get_available_years,
    filter_by_year_and_quarter,
    get_unemployed_by_education,
    get_unemployment_rate_over_time,
    get_employment_rate_over_time,
    get_employment_distribution_by_agglomerate
)

st.title("Actividad y empleo")
st.subheader("Personas desocupadas según estudios alcanzados")

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

# EVOLUCIÓN DEL DESEMPLEO

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

# EVOLUCIÓN DEL EMPLEO

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

distribution_df = get_employment_distribution_by_agglomerate(df)

st.markdown("### Distribución del tipo de empleo por aglomerado")

st.dataframe(
    distribution_df.style.format({
        "total_ocupados": "{:,.0f}",
        "% estatal": "{:.2f}%",
        "% privado": "{:.2f}%",
        "% otro": "{:.2f}%"
    }),
    height=600  # opcional, para que tenga scroll vertical si es mucha info
)