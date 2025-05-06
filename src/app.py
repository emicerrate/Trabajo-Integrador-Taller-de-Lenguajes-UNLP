from funcionesA import range_dataset

min_year, max_year, min_quarter, max_quarter = range_dataset()

import streamlit as st

# Sidebar con menú de páginas
st.sidebar.title("Menú de navegación")
pagina = st.sidebar.selectbox("Seleccionar página", ["Inicio", "Carga de datos", "Búsqueda por tema", "Visualización"])

if pagina == "Inicio":
    st.title("ARGencuesta")
    st.write("Transformamos los datos complejos de la Encuesta Permanente de Hogares (EPH) -el programa nacional del INDEC que mide empleo, educación y condiciones de vida- en información clara y visual, para que cualquier persona pueda entender las realidades socioeconómicas de Argentina. Procesamos los datos crudos de la EPH (relevados trimestralmente en todo el país) y los reconvertimos para su fácil acceso, sin requerir conocimientos técnicos.")
    st.info("Instrucciones de uso aquí (etapa 2).")

elif pagina == "Carga de datos":
    st.header("Carga de datos")
    st.write(f'El sistema contiene información desde el {min_quarter:02}/{min_year} hasta el {max_quarter:02}/{max_quarter}.')
    if st.button("Actualizar dataset"):
        # FALTA INVOCAR FUNCIONES
        st.success("Dataset actualizado correctamente.")

elif pagina == "Búsqueda por tema":
    st.header("Búsqueda por tema")

elif pagina == "Visualización":
    st.header("Visualización")