import streamlit as st

st.title("📊 ¿Qué es ARGencuesta?")

st.write("""
ARGencuesta es una plataforma interactiva que transforma los complejos datos de la **Encuesta Permanente de Hogares (EPH)** en gráficos e información accesible y clara.  
Este programa del **INDEC** releva desde hace décadas datos clave sobre empleo, educación, ingresos y condiciones de vida en los hogares argentinos.  

Nuestro objetivo es que cualquier persona, sin conocimientos técnicos, pueda explorar y comprender la realidad socioeconómica del país.
""")

st.subheader("🛠️ ¿Cómo se construye esta aplicación?")

st.write("""
ARGencuesta está desarrollada en **Python**, utilizando notebooks para procesar los datos y la biblioteca **Streamlit** para crear una experiencia visual e interactiva.
""")

st.markdown("### 📁 Preparación de los datos")

st.write("""
Antes de ejecutar la aplicación, es necesario preparar los datos originales de la EPH.
""")

st.markdown("### 🔽 Descarga de archivos")

st.write("""
1. Ingresá al sitio oficial del INDEC:  
   👉 [Bases de datos EPH - INDEC](https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos)

2. Descargá las carpetas correspondientes al período **2016 a 2024** de la **EPH continua**.

3. Descomprimí los archivos y guardalos **dentro de la carpeta `/files`** del proyecto.
""")

st.markdown("### ⚙️ Instalación y ejecución")

st.write("""
Asegurate de tener **Python** instalado en tu sistema. Luego seguí estos pasos:

1. Instalá las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
Procesá los datos ejecutando los notebooks incluidos en el proyecto.
```
Finalmente, iniciá la aplicación desde la terminal con:
         
```bash
    streamlit run streamlit/Inicio.py
```
         
📌 Asegurate de estar ubicado en la carpeta raíz del proyecto al ejecutar este comando.
""")

st.success("Una vez completados estos pasos, ya podés comenzar a explorar los datos socioeconómicos de Argentina con ARGencuesta.")