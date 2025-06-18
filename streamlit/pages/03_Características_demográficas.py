import streamlit as st
from st_constantes import DATA_OUT_PATH
import matplotlib.pyplot as plt
from package.data_graphics.individuos import (
    get_available_years,
    load_individual_data_02,
    media_and_median_last_quarter,
    age_media_per_conglomerate
)
from package.data_graphics.funcionesA import data_dates

# Cargamos el archivo usu_individual_final.csv
try:
    df = load_individual_data_02()
except (FileNotFoundError, ValueError) as e:
    st.error(str(e))
    st.stop()

available_years = get_available_years(df)
quarters = [1, 2, 3, 4]

st.title("Características demográficas")

# # 1.3.1 Distribución de la población por edad y sexo
# st.subheader("Distribución de la población por edad y sexo")
# year = st.text_input("Año:")
# quarter = st.slider("Trimestre:", value=1, min_value=1, max_value=4, step=1)
# if year:
#     try:
#         year_int = int(year)
#         if year_int not in available_years:
#             st.warning("No hay datos disponibles para el año ingresado.")
#         else:
#             filtered_df = filter_by_year_and_quarter(df, year_int, quarter)
#             if filtered_df.empty:
#                  st.warning(f"No hay datos para el {quarter}° trimestre de {year}.")
#     except ValueError:
#         st.warning("El año ingresado es inválido. Por favor, vuelva a intentarlo.")


# 1.3.2 Edad promedio último trimestre
st.subheader("Edad promedio de personas por aglomerado para el último trimestre")
df_age_media_per_conglomerate = age_media_per_conglomerate(df)
st.dataframe(df_age_media_per_conglomerate.style.format({"PROMEDIO DE EDAD": "{:.1f}"}), hide_index=True)

# # 1.3.3 Evolución de la dependencia demográfica
# st.subheader("Evolución de la dependencia demográfica")

# 1.3.4 Media y mediana de la edad
st.subheader("Media y mediana de la edad para cada año y trimestre")
df_media_and_median_last_quarter = media_and_median_last_quarter(df)
st.dataframe(df_media_and_median_last_quarter.style.format({"MEDIA": "{:.2f}", "MEDIANA": "{:,.0f}"}), hide_index=True, width=500)