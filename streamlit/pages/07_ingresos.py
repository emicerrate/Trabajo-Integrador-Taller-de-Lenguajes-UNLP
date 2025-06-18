import streamlit as st
from st_constantes import DATA_OUT_PATH, DATA_PATH
from package.data_graphics.hogares import (
    load_basket_data,
    load_hogar_data,
    basket_cost_per_quarter
)
from package.data_graphics.individuos import (
    get_available_years,
    get_available_quarters,
    filter_by_year_and_quarter
)

st.title("Ingresos")
st.subheader("Hogares por debajo de la linea de pobreza e indigencia")

# Se carga los archivos de valores de canasta básica y de hogares
try:
    df_basket = load_basket_data()
except (FileNotFoundError, ValueError) as e:
    st.error(str(e))
    st.stop()
finally:
    try:
        df_homes = load_hogar_data()
    except (FileNotFoundError, ValueError) as e:
        st.error(str(e))
        st.stop()

# El usuario selecciona año y trimestre
available_years = get_available_years(df_homes)
selected_year = st.radio("Año", options=available_years)
available_quarters = get_available_quarters(df_homes, selected_year)
selected_quarter = st.radio("Trimestre", options=available_quarters)
df_homes_filtered = filter_by_year_and_quarter(df_homes, selected_year, selected_quarter)
if st.button("Calcular"):
    st.write(basket_cost_per_quarter(df_basket, selected_year, selected_quarter))