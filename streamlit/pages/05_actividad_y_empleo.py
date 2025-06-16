import streamlit as st
from st_constantes import DATA_OUT_PATH

from package.data_graphics.individuos import (
    load_individual_data,
    get_available_years,
    filter_by_year_and_quarter,
    get_unemployed_by_education
)

st.title("(P5) Actividad y empleo")
st.subheader("1.5.1 Personas desocupadas según estudios alcanzados")

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

st.markdown("### Tabla de datos")
st.dataframe(
    education_counts.reset_index().rename(
        columns={"index": "Estudios", "nivel_educativo": "Cantidad"}
    )
)