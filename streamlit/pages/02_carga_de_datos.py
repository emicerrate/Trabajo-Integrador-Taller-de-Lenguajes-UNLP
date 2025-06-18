import streamlit as st
from package.data_graphics.funcionesA import range_dataset, init_file_reset, check_dataset

min_quarter, min_year, max_quarter, max_year = range_dataset()
missing_files = check_dataset()

st.title("🔄 Verificación y actualización de archivos EPH")

st.write("""
En esta sección podés verificar la **consistencia de los archivos cargados** para cada período de la Encuesta Permanente de Hogares (EPH).
El sistema controla que:

- Para cada archivo de **individuales** exista su correspondiente archivo de **hogares**.
- Para cada archivo de **hogares** exista su correspondiente archivo de **individuales**.
""")

st.write("""
🔍 Si se detecta algún archivo faltante, se informará en pantalla el **año, trimestre y tipo de archivo** que no se encontró.

🖱️ **Actualizar datasets** para **resetear y procesar nuevamente** los archivos cargados
""")

st.info(f'El sistema contiene información desde el {min_quarter:02}/{min_year} hasta el {max_quarter:02}/{max_year}.')
if missing_files == []:
    st.success("✅ Todos los archivos de hogares tienen su correspondiente de individuos.")
else:
    st.error("Existe uno o más archivos faltantes en el dataset:")
    for file in missing_files:
        st.write(f'Archivo de {file[2]} correspondiente al trimestre {file[1]} del año {file[0]}')


if st.button("Actualizar dataset"):
    init_file_reset()
    st.write(f'El sistema contiene información desde el {min_quarter:02}/{min_year} hasta el {max_quarter:02}/{max_year}.')
    missing_files = check_dataset()
    if missing_files == []:
        st.success("Dataset actualizado correctamente. ✅ Todos los archivos de hogares tienen su correspondiente de individuos. ")
    else:
        st.error("Existe uno o más archivos faltantes en el dataset:")
        for file in missing_files:
            st.write(f'Archivo de {file[2]} correspondiente al trimestre {file[1]} del año {file[0]}')