import streamlit as st
import pandas as pd
import altair as alt

from package.data_graphics.individuos import (
    load_individual_data_06,
    get_education_level_counts,
    P1_B4_to_csv,
    most_common_level,
    calculate_percentage
)

st.title("📖 Educación 🎓")
st.write("""En esta sección explorá el nivel educativo de la población argentina según 🎓 estudios alcanzados,  👥 grupos etarios, 🏙️ aglomerados y 📅 años, con gráficos interactivos y descarga de rankings en CSV.""")

df = load_individual_data_06()

# 1.6.1 cantidad de personas según el máximo nivel educativo
st.subheader("Cantidad de personas según el máximo nivel educativo")
st.markdown("""
Muestra de la cantidad de personas según el máximo nivel educativo alcanzado en el año seleccionado.
""")

year = sorted(df["ANO4"].unique())
selected_year = st.selectbox("Seleccione un año: ", year)

filtered_data = df[df['ANO4'] == selected_year]

st.subheader(f"Año {selected_year}")


# Configuración base
base = alt.Chart(df_education_level).encode(
    x=alt.X('Nivel Educativo:N', sort='-y', title="Nivel Educativo"),
    y=alt.Y('Cantidad:Q', title="Cantidad de personas")
)

# Configuración de barras
bars = base.mark_bar().encode(
    color=alt.Color('Cantidad:Q', scale=alt.Scale(scheme='orangered'), legend=None),
    tooltip=['Nivel Educativo', 'Cantidad']
)

# Configuración del texto en las barras
text = base.mark_text(
    align='center',
    baseline='bottom',
    dy=-5,
    color='white'
).encode(
    text='Cantidad:Q'
)

# Combinación del gráfico
combined = (bars + text).properties(
    width=900,
    height=600,
    title=alt.TitleParams(
        text="Cantidad de personas por nivel educativo alcanzado",
        fontSize=20,
        anchor='start',
        dy=10
    ),
    background='#1D2B44',
    padding={'top': 25, 'left': 15, 'right': 0, 'bottom': 15}
).configure_axis(
    labelColor='white',
    titleColor='white',
    labelAngle=90,
    labelFontSize=10,
    titleFontSize=12
).configure_title(
    color='white'
).configure_view(
    strokeWidth=0
)

# Mostrar el gráfico
st.altair_chart(combined, use_container_width=True)

# 1.6.2 Nivel educacional alcanzado más común por rango etario
st.subheader("Nivel educacional alcanzado más común por rango etario")
st.markdown("""
Muestra de la cantidad de personas según el nivel educativo común según rango etario etiquetado.
""")

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

df_educ = most_common_level(selected_ranges, age_ranges, df)
if not df_educ.empty:
    nivel_mas_comun = df_educ.iloc[0]["Nivel Educativo"]
    st.info(f"El nivel educacional más común alcanzado dentro del rango de edad {selected_ranges} años es *{nivel_mas_comun}*.")
else:
    st.info("No hay datos disponibles para el/los rango/s seleccionado/s.")

st.write(f"El nivel educacional más común alcanzado dentro del rango de edad {selected_ranges} años es {ed_levels[most_common_level]}.")

st.subheader("Ranking de los 5 Aglomerados con Mayor Porcentaje de Hogares con Dos o Más Ocupantes con Estudios Universitarios o Superiores Finalizados")


st.download_button(
    label="⬇️🗂️ Descargar CSV de ranking",
    data=P1_B4_to_csv(),
    file_name="resultados_ranking.csv",
    mime="text/csv"
)

percentage_df = calculate_percentage(df)
percentage_df = percentage_df.rename(columns={"ANO4": "year"})

st.subheader("Porcentaje por año de personas mayores de 6 años capaces de leer y escribir")

# Definimos los límites del zoom para el eje Y
# (Puedes ajustarlos o hacerlos dinámicos si lo necesitas)
y_zoom_min = min(90, int(percentage_df['porcentaje'].min())) # Un valor seguro de inicio
y_zoom_max = 100

# Código del gráfico de Altair, ahora usando 'percentage_df'
chart = alt.Chart(percentage_df).mark_area(
    line={'color':'orangered'},
    color=alt.Gradient(
        gradient='linear',
        stops=[alt.GradientStop(color='orangered', offset=0),
               alt.GradientStop(color='#ff7f50', offset=1)],
        x1=1,
        y1=1,
        x2=1,
        y2=0
    ),
    interpolate='monotone'
).encode(
    x=alt.X('year:O', title='Año'),
    y=alt.Y('porcentaje:Q', scale=alt.Scale(domain=[y_zoom_min, y_zoom_max]), title='Porcentaje (%)'),
    y2=alt.Y2(datum=y_zoom_min),
    tooltip=['year', alt.Tooltip('porcentaje', format='.2f')]
).properties(
    # El título se quitó de aquí porque ahora lo maneja st.subheader
    width=900,
    height=400,
    background='#1E2B44'
).configure_axis(
    labelColor='white',
    titleColor='white',
    titlePadding=15  # Mantiene el espaciado del título del eje
).configure_view(
    strokeWidth=0
)

# Muestra el gráfico en la app
st.altair_chart(chart, use_container_width=True)
file_for_download = P1_B4_to_csv


st.download_button(
    label="Descargar ranking",
    data=file_for_download,
    file_name="resultados_ranking.csv",
    mime="text/csv"
)


# 1.6.4 Nivel educacional alcanzado más común por rango etario
st.subheader("Evolución de la alfabetización en Argentina")
st.markdown("""
Muestra de la evolución del porcentaje de personas mayores a 6 años capaces de leer y escribir.
""")

percentage_df = calculate_percentage(df)
percentage_df = percentage_df.rename(columns={"ANO4": "year"})

# Crear figura y ejes
fig, ax = plt.subplots(figsize=(10, 6))

# Fondo oscuro
fig.patch.set_facecolor('#1E2B44')
ax.set_facecolor('#1E2B44')

# Línea naranja
ax.plot(percentage_df['year'], percentage_df['porcentaje'], color='orangered', linewidth=2)

# Títulos de ejes
ax.set_title("Porcentaje por año de personas mayores de 6 años capaces de leer y escribir", color='white', fontsize=14)
ax.set_xlabel("Año", color='white')
ax.set_ylabel("Porcentaje (%)", color='white')

# Color de ticks
ax.tick_params(axis='x', colors='white', rotation=45)
ax.tick_params(axis='y', colors='white')

# Quitar el marco
for spine in ax.spines.values():
    spine.set_visible(False)

# Mostrar el gráfico en Streamlit
st.pyplot(fig)