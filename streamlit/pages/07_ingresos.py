import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from st_constantes import DATA_OUT_PATH, DATA_PATH
from package.data_graphics.hogares import (
    load_basket_data,
    load_hogar_data_07,
    poverty_indigence_lines_per_quarter,
    homes_under_poverty_indigence
)
from package.data_graphics.individuos import (
    get_available_years,
    get_available_quarters,
    filter_by_year_and_quarter
)

st.title("👨‍👩‍👧‍👦 Ingresos 💸")

st.markdown("""
Esta sección permite al usuario seleccionar un año y trimestre para analizar los ingresos de hogares de 4 integrantes. 
A partir de los datos de ingresos totales (ITF) y los valores mensuales de la canasta básica familiar, 
se calcula y muestra cuántos hogares están por debajo de la línea de pobreza e indigencia, tanto en cantidad como en porcentaje.
""")

st.subheader("Hogares por debajo de la linea de pobreza e indigencia")
st.markdown("""
Seleccionar año y trimestre:
""")

# Se carga los archivos de valores de canasta básica y de hogares
try:
    df_basket = load_basket_data()
except (FileNotFoundError, ValueError) as e:
    st.error(str(e))
    st.stop()
finally:
    try:
        df_homes = load_hogar_data_07()
    except (FileNotFoundError, ValueError) as e:
        st.error(str(e))
        st.stop()

# Se carga el dataframe necesario para la pagina
available_years = get_available_years(df_homes)

# El usuario selecciona año y trimestre
col1, col2 = st.columns(2)

with col1:
    selected_year = st.radio("Año", options=available_years)

with col2:
    available_quarters = get_available_quarters(df_homes, selected_year)
    selected_quarter = st.radio("Trimestre", options=available_quarters)

# Se filtra el dataframe por año y trimestre
df_homes_filtered = filter_by_year_and_quarter(df_homes, selected_year, selected_quarter)

# Se obtienen las lineas de pobreza e indigencia
p_line, i_line = poverty_indigence_lines_per_quarter(df_basket, selected_year, selected_quarter)

if st.button("Calcular"):
    # Se calculan la cantidad de hogares bajo la linea de pobreza e indigencia y se sacan los porcentajes con el total
    under_poverty_q, under_indigence_q, total = homes_under_poverty_indigence(df_homes_filtered, p_line, i_line)
    perc_poverty = round(under_poverty_q * 100 / total, 2)
    perc_indigence = round(under_indigence_q * 100 / total, 2)
    rest = 100 - perc_poverty
    percentages = [perc_indigence, perc_poverty, rest]

    # Se emprolija el DataFrame
    data = pd.DataFrame(
        {
        "condicion": ["Bajo la linea de indigencia", "Bajo la linea de pobreza", "Sobre la linea de pobreza"],
        "porcentajes": percentages
        }
    )

    # Grafico de Barras
    fig, ax = plt.subplots(figsize=(8,6))
    plt.title("Canasta básica", color="#FFFFFF")
    plt.ylabel("Porcentaje", labelpad=10, color="#FFFFFF")
    ax.bar(data['condicion'], data['porcentajes'], width=0.4, color=["#B71C1C"], edgecolor=["#FFFFFF"])  # Ajusta `width` para cambiar el ancho de las barras
    ax.tick_params(axis='x', colors='#FFFFFF')
    ax.tick_params(axis='y', colors='#FFFFFF')
    ax.spines['top'].set_visible(False)      # Quitar marco superior
    ax.spines['right'].set_visible(True)
    ax.spines['left'].set_color("#FFFFFF")      # Quitar marco superior
    ax.spines['bottom'].set_color("#FFFFFF")
    ax.set_ylim(0, 100)
    fig.patch.set_facecolor('#1D2B44')
    ax.set_facecolor('#1D2B44')
    
    ax2 = ax.twinx()
    ax2.spines['right'].set_color('#FFFFFF')
    ax2.spines['top'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.set_ylabel("Cantidad", color='#FFFFFF', labelpad=30)  # Título
    ax2.tick_params(axis='y', colors='#FFFFFF')  # Color de las graduaciones
    ax2.set_ylim(0, total)
    ax2.ticklabel_format(axis='y', style='plain')
    
    texts = ["Cantidad de hogares " + data["condicion"][0].lower() +" : " + str(under_indigence_q) + " (" + str(percentages[0])+ "%).",
             "Cantidad de hogares " + data["condicion"][1].lower() +" : " + str(under_poverty_q) + " (" + str(percentages[1])+ "%).",
             "Cantidad de hogares " + data["condicion"][2].lower() +" : " + str(total - under_poverty_q) + " (" + str(percentages[2])+ "%)."]

    for text in texts:
        st.info(text)

    st.pyplot(fig)
    
