import streamlit as st
from package.data_graphics.funcionesA import range_dataset, init_file_reset, check_dataset

min_quarter, min_year, max_quarter, max_year = range_dataset()

st.header("Carga de datos")

if st.button("Actualizar dataset"):
    init_file_reset()
    st.write(f'El sistema contiene información desde el {min_quarter:02}/{min_year} hasta el {max_quarter:02}/{max_year}.')
    missing_files = check_dataset()
    if missing_files == []:
        st.success("Dataset actualizado correctamente.")
    else:
        st.error("Existe uno o más archivos faltantes en el dataset:")
        for file in missing_files:
            st.write(f'Archivo de {file[2]} correspondiente al trimestre {file[1]} del año {file[0]}')