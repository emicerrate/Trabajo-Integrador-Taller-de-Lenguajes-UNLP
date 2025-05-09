import streamlit as st
from src.funcionesA import range_dataset, init_file_reset

init_file_reset()
min_quarter, min_year, max_quarter, max_year = range_dataset()

st.header("Carga de datos")
st.write(f'El sistema contiene información desde el {min_quarter:02}/{min_year} hasta el {max_quarter:02}/{max_year}.')
if st.button("Actualizar dataset"):
    init_file_reset()
    st.success("Dataset actualizado correctamente.")