# ARGencuesta 
Aplicación de visualización de datos de la EPH (Encuesta Permanente de Hogares) desarrollada en Python con Streamlit.  

## Requisitos  
- Python 3.12+  
- Librerías: `streamlit`, `notebook`, `pandas`, `matplotlib`, `folium`, `streamli-folium`

## Instalación  
```bash
git clone [https://gitlab.catedras.linti.unlp.edu.ar/python-2025/proyectos/grupo20/code.git]  

# Navegar al directorio del proyecto para instalar y ejecutar streamlit
pip install -r requirements.txt  
streamlit run streamlit/Inicio.py 

```

# Estructura del Proyecto
```
code/
│── .git/ (oculto)
|── data_out/
    │── .gitkeep
    │── usu_hogar_final.csv         # Archivo hogar que compila todos los data sets "hogar" en un solo archivo
    │── usu_individual_final.csv    # Archivo individual que compila todos los data sets "individual" en un solo archivo
|── files/      #Carpeta donde almacenar los data sets a ser usados
    │── .gitkeep
│── notebooks/
    │── hogar.ipynb         # Aplicación hogar
    │── individual.ipynb    # Aplicación individual
    │── total.ipynb         # Aplicación total
│── src/                 # Código fuente y funciones
    │── __pycache__/
    ├── __init__.py   
    │── constantes.py
    ├── funcionesA.py       # Funciones aplicación Streamlit
    │── funcionesH.py       # Funciones aplicación hogar
    │── funcionesI.py       # Funciones aplicación individual
    │── funcionesT.py       # Funciones aplicación total
│── streamlit           # Aplicación Streamlit
    │── package             
        │── data_graphics   # Funcionalidades
            │── __init__.py
            │── funcionesA.py   # Funciones de carga de datos
            │── hogares.py      # Funciones que procesan sobre archivo de hogares
            │── individuos.py   # Funciones que procesan sobre archivo de individuos
            │── maps_utils.py   # Funciones que procesan la visualización de mapas
    │── pages
        │── 02_Carga_de_datos.py
        │── 03_Características_demográficas.py
        │── 04_Carcterísca_hogares.py
        │── 05_Actividad_y_empleo.py
        │── 06_Educación.py
        │── 07_Ingresos.py
    │── Inicio.py           # Archivo que inicializa la aplicación
    │── st.constantes.py    # Contiene paths absolutos como variables
│── .gitattributes
│── .gitignore
│── app.py              # Script principal aplicación Streamlit
│── LICENSE
│── README.md            # Instrucciones y documentación
│── requirements.txt     # Dependencias del proyecto
```

## Grupo 20

- ALEJANDRO MANUEL AMOR
- EMILIO PABLO CERRATE
- FRANCO PAOLO URRICELQUI
- JOAQUIN ARIEL CEQUEIRA
- JOAQUIN PEREA