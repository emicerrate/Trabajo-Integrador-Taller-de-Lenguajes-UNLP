import streamlit as st
from package.data_graphics.funcionesA import range_dataset, init_file_reset, check_dataset

min_quarter, min_year, max_quarter, max_year = range_dataset()

st.title("🔄 Verificación y actualización de archivos EPH")

st.write("""
En esta sección podés verificar la **consistencia de los archivos cargados** para cada período de la Encuesta Permanente de Hogares (EPH).
""")

st.info(f'El Dataset actual contiene información desde el {min_quarter:02}/{min_year} hasta el {max_quarter:02}/{max_year}.')

st.write("""
## 🔍 Check Dataset para controlar:

- Que cada archivo de **individuales** exista su correspondiente archivo de **hogares**.
- Que cada archivo de **hogares** exista su correspondiente archivo de **individuales**.
""")

if st.button("Check dataset"):
    try:
        missing_files = check_dataset()
        if missing_files == []:
            st.success("✅ Todos los archivos de hogares tienen su correspondiente de individuos. ")
            st.info(f"El sistema contiene información desde el {min_quarter:02}/{min_year} hasta el {max_quarter:02}/{max_year}.")
        else:
            st.error("Existe uno o más archivos faltantes en el dataset:")
            for file in missing_files:
                st.error(f'Archivo de {file[2]} correspondiente al trimestre {file[1]} del año {file[0]}')
    except:
        st.error("Existen inconsistencias en los directorios del datasets. Por favor, revise los nombres de los directorios e intente nuevamente")

st.write(""" 
## 🖱️ Actualizar los datasets 
""")

if st.button("Actualizar dataset"):
    init_file_reset()
    missing_files = check_dataset()
    if missing_files == []:
        st.success("Dataset actualizado correctamente. ✅ Todos los archivos de hogares tienen su correspondiente de individuos.")
        st.info(f'El Dataset actual contiene información desde el {min_quarter:02}/{min_year} hasta el {max_quarter:02}/{max_year}.')
    else:
        st.error("Existe uno o más archivos faltantes en el dataset:")
        for file in missing_files:
            st.error(f'Archivo de {file[2]} correspondiente al trimestre {file[1]} del año {file[0]}')

