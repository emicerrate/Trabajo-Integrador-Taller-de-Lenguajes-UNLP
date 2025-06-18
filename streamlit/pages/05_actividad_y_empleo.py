import streamlit as st
from st_constantes import DATA_OUT_PATH
import folium
from streamlit_folium import st_folium  # para mostrar el mapa en Streamlit
import matplotlib.pyplot as plt

from package.data_graphics.individuos import (
    agglomeration_id,
    load_individual_data_05,
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

st.title("💼 Actividad y empleo 🛠️")

st.subheader("Explorá **indicadores clave del mercado laboral argentino**.")

st.markdown("""
 
Visualizá la evolución del empleo y el desempleo según 📅 período, 🏙️ aglomerado y 🎓 nivel educativo, con gráficos y mapas interactivos.
""")

# Se Carga el archivo usu_individual_final.csv con las columnas necesarias para las funcionalidades de esta pagina
try:
    df = load_individual_data_05()
except (FileNotFoundError, ValueError) as e:
    st.error(str(e))
    st.stop()

#PARA VER QUE CONTIENE st
#st.dataframe(df[["AGLOMERADO", "ANO4", "TRIMESTRE", "CONDICION_LABORAL"]].drop_duplicates())
#st.write(df.dtypes[[102, 169, 177]])

available_years = get_available_years(df)

st.markdown("""
### Personas desocupadas según estudios alcanzados
Se informa el nivel educativo de los desocupados. 
Elegir año y trimestre, se evalúa para todo el país.
""")

selected_year = st.selectbox("Año", available_years, index=len(available_years) - 1)
selected_quarter = st.selectbox("Trimestre", [1, 2, 3, 4])

filtered_df = filter_by_year_and_quarter(df, selected_year, selected_quarter)

if filtered_df.empty:
    st.warning(f"No hay datos para el {selected_quarter}° trimestre de {selected_year}.")

education_counts = get_unemployed_by_education(filtered_df)

st.markdown(" ### Gráfico de desocupados por nivel educativo")

# Crear figura y ejes
fig, ax = plt.subplots(figsize=(10, 5))

# COlor de fondo
fig.patch.set_facecolor('#1D2B44')
ax.set_facecolor('#1D2B44')

# Color de las barras
ax.bar(education_counts.index, education_counts.values, color='#E44336')

# Títulos y etiquetas (texto blanco brillante)
ax.set_title("Personas desocupadas por nivel educativo", fontsize=14, color='#FFFFFF')
ax.set_xlabel("Nivel educativo", fontsize=12, color='#FFFFFF')
ax.set_ylabel("Cantidad", fontsize=12, color='#FFFFFF')

# Ejes
ax.tick_params(axis='x', labelrotation=45, colors='#FFFFFF')
ax.tick_params(axis='y', colors='#FFFFFF')

# Bordes en blanco 
for spine in ax.spines.values():
    spine.set_edgecolor('#FFFFFF')

# Mostrar en Streamlit
st.pyplot(fig)

# 1.5.2 EVOLUCIÓN DEL DESEMPLEO

# Obtener diccionario de aglomerados
dict_ag_id = agglomeration_id()
dict_name_to_id = {v: k for k, v in dict_ag_id.items()}

# Lista de aglomerados con nombres
agglomerates = ["Todo el país"] + sorted(dict_name_to_id.keys())

st.markdown("""
### Evolución tasa de desempleo
Se informa la evolución del desempleo (tasa de desempleo) a lo largo del tiempo. 
Elegir aglomerado o para todo el país.
""")

# Selector de aglomerado (por nombre)
selected_agglomerate_name = st.selectbox("Aglomerado", agglomerates)

# Obtener código correspondiente
if selected_agglomerate_name == "Todo el país":
    selected_agglomerate = "Todo el país"
else:
    selected_agglomerate = int(dict_name_to_id[selected_agglomerate_name])

# Obtener la evolución de la tasa de desempleo

unemployment_df = get_unemployment_rate_over_time(df, selected_agglomerate)

if unemployment_df.empty:
    st.warning("No hay datos disponibles para la selección.")
else:
    fig, ax = plt.subplots(figsize=(10, 5))

    # Fondo
    fig.patch.set_facecolor('#1D2B44')
    ax.set_facecolor('#1D2B44')

    # Línea de tasa de desempleo
    ax.plot(unemployment_df["periodo"], unemployment_df["tasa_desempleo"],
            color="#E44336", linewidth=2)

    # Títulos y etiquetas
    ax.set_title("Evolución de la tasa de desempleo", fontsize=14, color='white')
    ax.set_xlabel("Periodo", fontsize=12, color='white')
    ax.set_ylabel("Tasa de desempleo (%)", fontsize=12, color='white')

    # Ejes
    ax.tick_params(axis='x', labelrotation=45, colors='white')
    ax.tick_params(axis='y', colors='white')

    # Bordes del gráfico
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    st.pyplot(fig)
    
# 1.5.3 EVOLUCIÓN DEL EMPLEO

st.markdown("""
### Evolución de la tasa de empleo
Se informa la evolución del empleo (tasa de empleo) a lo largo del tiempo. 
Elegir aglomerado o para todo el país.
""")

# Segundo selector (por nombre, con otra clave)
selected_agglomerate_name2 = st.selectbox("Aglomerado", agglomerates, key="emp_agglom")

# Obtener código correspondiente
if selected_agglomerate_name2 == "Todo el país":
    selected_agglomerate2 = "Todo el país"
else:
    selected_agglomerate2 = int(dict_name_to_id[selected_agglomerate_name2])

# Obtener la evolución de la tasa de empleo
employment_df = get_employment_rate_over_time(df, selected_agglomerate2)

if employment_df.empty:
    st.warning("No hay datos disponibles para la selección.")
else:
    fig, ax = plt.subplots(figsize=(10, 5))

    # Fondo
    fig.patch.set_facecolor('#1D2B44')
    ax.set_facecolor('#1D2B44')

    # Línea de tasa de empleo
    ax.plot(employment_df["periodo"], employment_df["tasa_empleo"],
            color="#E44336", linewidth=2)

    # Títulos y etiquetas
    ax.set_title("Evolución de la tasa de empleo", fontsize=14, color='white')
    ax.set_xlabel("Periodo", fontsize=12, color='white')
    ax.set_ylabel("Tasa de empleo (%)", fontsize=12, color='white')

    # Ejes
    ax.tick_params(axis='x', labelrotation=45, colors='white')
    ax.tick_params(axis='y', colors='white')

    # Bordes del gráfico
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    st.pyplot(fig)

# 1.5.4 DISTRIBUCION DEL EMPLEO

st.markdown("""
### Distribución del tipo de empleo por aglomerado
Se informa para cada aglomerado el total de personas ocupadas, el porcentaje con empleo estatal, el porcentaje con empleo privado y el porcentaje de otro tipo. 
Elegir año y trimestre:
""")

# Selector año y trimestre (por nombre, con otra clave)
selected_year2 = st.selectbox("Año", available_years, index=len(available_years) - 1, key="selected_year_2")
selected_quarter2 = st.selectbox("Trimestre", [1, 2, 3, 4], key="selected_quarter_2")


distribution_df = get_employment_distribution_by_agglomerate(df, selected_year2, selected_quarter2)

distribution_df.columns = ["Total Ocupados", "% Estatal", "% Privado", "% Otro"]

st.dataframe(
    distribution_df.style.format({
        "Total Ocupados": "{:,.0f}",
        "% Estatal": "{:.2f}%",
        "% Privado": "{:.2f}%",
        "% Otro": "{:.2f}%"
    }),
    height=600  # opcional, para que tenga scroll vertical si es mucha info
)

# 1.5.5 MAPA DE EMPLEO Y DESEMPLEO

#st.markdown("### Tasa de empleo y desempleo por aglomerado")

df_rates = get_employment_unemployment_by_agglomerate_extremes(df)  

# Seleccionar columnas a mostrar
#cols_a_mostrar = ["nombre"] + [col for col in df_rates.columns if col.startswith("tasa_")]

# Renombrar columnas para que se vean más claras
#ename = {
#    col: col.replace("tasa_empleo", "Tasa de Empleo").replace("tasa_desempleo", "Tasa de Desempleo")
#    for col in cols_a_mostrar if col != "nombre"
#}

# Aplicar el renombramiento
#df_formateado = df_rates[cols_a_mostrar].rename(columns=rename)

# Mostrar DataFrame con formato de porcentaje
#st.dataframe(
#    df_formateado.style.format(
#        {col: "{:.2f}%" for col in df_formateado.columns if col != "nombre"}
#   ),
#    height=600
#)

st.markdown("""
### Mapa de la evolución de  la tasa de empleo y desempleo por aglomerado

Este mapa interactivo permite visualizar cómo evolucionaron las tasas de empleo o desempleo en cada aglomerado urbano del país entre el primer y el último período disponible en la base de datos.  
Al seleccionar el tipo de tasa que desea analizar, el mapa marcará con **puntos verdes** los aglomerados donde la situación **mejoró con el tiempo** y con **puntos rojos** aquellos donde **empeoró**.

- Si elige ver la **tasa de empleo**, el color verde indica un aumento del empleo y el rojo una disminución.  
- Si selecciona la **tasa de desempleo**, el verde representa una reducción del desempleo y el rojo un aumento.
""")

selected_rate = st.selectbox("Elige la tasa a visualizar:", ["empleo", "desempleo"])

# Se genera el mapa
map = generate_map()

df_rates.apply(lambda row: add_marker(row, map, selected_rate), axis=1)

st_folium(map, width=700, height=500)