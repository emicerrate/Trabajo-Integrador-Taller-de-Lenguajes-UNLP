import streamlit as st
from st_constantes import DATA_OUT_PATH
import matplotlib.pyplot as plt
import numpy as np
from package.data_graphics.individuos import (
    get_available_years,
    load_individual_data_02,
    media_and_median,
    age_media_per_conglomerate,
    agglomeration_id,
    demography_dependency,
    filter_by_year_and_quarter,
    distribution_per_age_and_gender
)
from package.data_graphics.funcionesA import data_dates

st.title("🧑‍🤝‍🧑 Características demográficas")

st.markdown("""
            En esta sección se pueden explorar **aspectos demográficos** de la población argentina.
            Podés conocer una gran variedad de cosas como:
            - La distribución de la población por edad y sexo ♂️♀️
            - La edad promedio por aglomerado 📅
            - La dependencia demográfica por aglomerado 👶🏻👴🏼
            - Media y mediana de la edad de la población 👩🏼👨🏻
            """)

# Cargamos el archivo usu_individual_final.csv
try:
    df = load_individual_data_02()
except (FileNotFoundError, ValueError) as e:
    st.error(str(e))
    st.stop()

available_years = get_available_years(df)
quarters = [1, 2, 3, 4]
id_to_name_conglomerates = agglomeration_id()
name_to_id_conglomerates = {name: id for id, name in id_to_name_conglomerates.items()}
sorted_conglomerates = sorted(name_to_id_conglomerates)

# 1.3.1 Distribución de la población por edad y sexo
st.subheader("Distribución de la población por edad y sexo")
st.markdown("""
    Muestra la distribución de la población por edad (grupos de 10 años) y sexo para el año y trimestre seleccionados.
""")
year = st.text_input("Año:")
quarter = st.slider("Trimestre:", value=1, min_value=1, max_value=4, step=1)
if year:
    try:
        year_int = int(year)
        if year_int not in available_years:
            st.warning("No hay datos disponibles para el año ingresado.")
        else:
            filtered_df = filter_by_year_and_quarter(df, year_int, quarter)
            if filtered_df.empty:
                st.warning(f"No hay datos para el {quarter}° trimestre de {year}.")
            else:
                df_distribution_per_age_and_gender = distribution_per_age_and_gender(filtered_df)
                
                # Datos para el gráfico
                labels = df_distribution_per_age_and_gender.index # Obtiene las etiquetas de los grupos de edad
                male_count = df_distribution_per_age_and_gender["MASCULINO"]
                female_count = df_distribution_per_age_and_gender["FEMENINO"]

                # Medidas para el gráfico
                x = np.arange(len(labels)) # Genera las posiciones en el eje x para las barras
                width = 0.4
                
                # Hacemos el gráfico de barras dobles para mostrar la distribución
                fig, ax = plt.subplots(figsize=(10,6))

                # Fondo
                fig.patch.set_facecolor('#1D2B44')
                ax.set_facecolor('#1D2B44')

                # Configuración de barras para masculino y femenino
                ax.bar(x - width/2, male_count, width, label="MASCULINO", color="#E44336")
                ax.bar(x + width/2, female_count, width, label="FEMENINO", color="#FF8A65")

                # Título, etiquetas, ejes y bordes
                ax.set_title(f"Distribución de la población por edad y sexo para el {quarter}° trimestre del año {year}", fontsize=14, color="white")
                ax.set_ylabel("Cantidad de personas", fontsize=14, color="white")
                ax.set_xlabel("Grupo etario", fontsize=14, color="white")
                ax.set_xticks(x)
                ax.set_xticklabels(labels, rotation=45, ha="right", color="white") # Rota los nombres de los grupos etarios
                ax.legend() # Agrega la leyenda para distinguir masculino de femenino
                for spine in ax.spines.values():
                    spine.set_edgecolor('white')
                ax.tick_params(axis='y', colors='white')
                fig.tight_layout()

                st.pyplot(fig)
    except ValueError:
        st.warning("El año ingresado es inválido. Por favor, vuelva a intentarlo.")


# 1.3.2 Edad promedio último trimestre
st.subheader("Edad promedio de personas por aglomerado para el último trimestre")
st.markdown("""
    Muestra la edad promedio de las personas para cada aglomerado para el último trimestre cargado.
""")
df_age_media_per_conglomerate = age_media_per_conglomerate(df)
st.dataframe(df_age_media_per_conglomerate.style.format({"PROMEDIO DE EDAD": "{:.1f}"}), hide_index=True)

# 1.3.3 Evolución de la dependencia demográfica
st.subheader("Evolución de la dependencia demográfica")
st.markdown("""
    Muestra la evolución a través del tiempo de la dependencia demográfica para un aglomerado seleccionado.
""")

conglomerate = st.selectbox("Aglomerado:", sorted_conglomerates, index=None, placeholder="Seleccione un aglomerado...")
if conglomerate != None:
    df_demography_dependency = demography_dependency(df, name_to_id_conglomerates[conglomerate])
    
    # Hacemos el gráfico de línea para mostrar en el tiempo la dependencia demográfica
    fig, ax = plt.subplots(figsize=(10, 5))

    # Fondo
    fig.patch.set_facecolor('#1D2B44')
    ax.set_facecolor('#1D2B44')

    # Línea de dependencia demográfica
    ax.plot(df_demography_dependency["PERÍODO"], df_demography_dependency["DEPENDENCIA DEMOGRÁFICA"], color="#E44336", linewidth=2)
    
    # Títulos y etiquetas
    ax.set_title("Evolución de la dependencia demográfica", fontsize=14, color='white')
    ax.set_xlabel("Período", fontsize=12, color='white')
    ax.set_ylabel("Dependencia demográfica (%)", fontsize=12, color='white')

    # Ejes
    ax.tick_params(axis='x', labelrotation=45, colors='white')
    ax.tick_params(axis='y', colors='white')

    # Bordes del gráfico
    for spine in ax.spines.values():
        spine.set_edgecolor('white')
    
    st.pyplot(fig)

# 1.3.4 Media y mediana de la edad
st.subheader("Media y mediana de la edad para cada año y trimestre")
st.markdown("""
    Calcula para cada trimestre almacenado la media y la mediana de edad de la población.
""")
df_media_and_median = media_and_median(df)
st.dataframe(df_media_and_median.style.format({"MEDIA": "{:.2f}", "MEDIANA": "{:,.0f}"}), hide_index=True, width=500)