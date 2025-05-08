# ARGencuesta 
Aplicación de visualización de datos de la EPH (Encuesta Permanente de Hogares) desarrollada en Python con Streamlit.  

## Requisitos  
- Python 3.12+  
- Librerías: `streamlit`, `notebook`

## Instalación  
```bash
git clone [https://gitlab.catedras.linti.unlp.edu.ar/python-2025/proyectos/grupo20/code.git]  

# Navegar al directorio del proyecto para instalar y ejecutar streamlit
pip install -r requirements.txt  
streamlit run app.py 

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
│── pages/ # Aplicación Streamlit
    │── 01_inicio.py
    │── 02_carga_de_datos.py
    │── 03_busqueda_por_tema.py
    │── 04_visualizacion.py
│── src/                 # Código fuente y funciones
    │── __pycache__/
│   ├── __init__.py   
    │── constantes.py       # Funciones constantes
    ├── funcionesA.py       # Funciones 
    │── funcionesH.py       # Funciones aplicación hogar
    │── funcionesI.py       # Funciones aplicación individual
    │── funcionesT.py       # Funciones aplicación total
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