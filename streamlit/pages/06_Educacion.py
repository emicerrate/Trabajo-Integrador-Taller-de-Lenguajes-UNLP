import streamlit as st
import pandas as pd
import altair as alt
import csv
from io import StringIO
from package.data_graphics.individuos import (
    load_individual_data_06,
    select_age_range,
    P1_B4_to_csv,
    calculate_percentage
)

st.title("Educación")
st.write("En esta sección se visualizará información relacionada al nivel de educación alcanzado por la población argentina según la EPH.")


df = load_individual_data_06

year = sorted(df["ANO4"].unique())
selected_year = st.selectbox("Seleccione un año: ", year)

filtered_data = df[df['ANO4'] == selected_year]

st.subheader(f"{selected_year}")
chart = alt.Chart(filtered_data).mark_bar().encode(
    x='category',
    y='value',
    tooltip=['category', 'value']
).properties(width=600)

st.altair_chart(chart, use_container_width=True)

age_ranges = {
        "20-30": (20, 30),
        "30-40": (30, 40),
        "40-50": (40, 50),
        "50-60": (50, 60),
        "+60": (60, 200)
    }

ed_levels = {
    1 : "Jardín/preescolar",
    2 : "Primario",
    3 : "EGB",
    4 : "Secundario",
    5 : "Polimodal",
    6 : "Terciario",
    7 : "Universitario",
    8 : "Posgrado universitario",
    9 : "Educación especial (discapacitado)"
}
selected_ranges = st.multiselect("Seleccione el/los rango/s de edad: ", list(age_ranges))

most_common_level = select_age_range(selected_ranges, df)

st.write(f"El nivel educacional más común alcanzado dentro del rango de edad {selected_ranges} años es {ed_levels[most_common_level]}.")

st.subheader("Ranking de los 5 Aglomerados con Mayor Porcentaje de Hogares con Dos o Más Ocupantes con Estudios Universitarios o Superiores Finalizados")

file_for_download = P1_B4_to_csv

st.download_button(
    label="Descargar ranking",
    data=file_for_download,
    file_name="resultados_ranking.csv",
    mime="text/csv"
)

percentage = calculate_percentage(df)

st.subheader("Porcentaje por año de personas mayores de 6 años capaces de leer y escribir")
st.line_chart(percentage.set_index("year"))