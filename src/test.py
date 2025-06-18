import pandas as pd 
import csv
from src.constantes import DATA_PATH, DATA_OUT_PATH

try:
    df = pd.read_csv(DATA_OUT_PATH / 'usu_individual_final.csv', encoding='latin1', sep=";")
    print("File loaded successfully with latin1 encoding.")
    print(df.info())
except FileNotFoundError:
    print(f"Error: El archivo no se encontró en {DATA_OUT_PATH / 'usu_individual_final.csv'}")
except Exception as e:
    print(f"Ocurrió un error al cargar el archivo: {e}")


