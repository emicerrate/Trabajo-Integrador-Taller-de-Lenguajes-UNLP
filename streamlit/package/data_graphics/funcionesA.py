import csv
import pandas as pd
from st_constantes import DATA_PATH

def all_togetherH(path_salida):
    """
    Junta todos los datos de los archivos hogar a un único archivo.
    Args:
        path_salida (Path): Ruta al archivo de salida donde se juntara toda la información.
    Returns:
        None
    """
    
    encabezado_escrito = False
    with path_salida.open("w", newline="") as salida:
        writer = csv.writer(salida, delimiter=";")
        for trimestre in DATA_PATH.iterdir():
            for archivo in trimestre.glob("usu_hogar_*"):
                with archivo.open() as file:
                    reader = csv.reader(file, delimiter=";")
                    header = next(reader)
                    if not encabezado_escrito:
                        writer.writerow(header)
                        encabezado_escrito = True
                    for row in reader:
                        writer.writerow(row)

def all_togetherI(path_salida):
    """
    Junta todos los datos de los archivos individuales a un único archivo.
    Args:
        path_salida (Path): Ruta al archivo de salida donde se juntara toda la información.
    Returns:
        None
    """

    encabezado_escrito = False
    with path_salida.open("w", newline="") as salida:
        writer = csv.writer(salida, delimiter=";")
        for trimestre in DATA_PATH.iterdir():
            for archivo in trimestre.glob("usu_individual_*"):
                with archivo.open() as file:
                    reader = csv.reader(file, delimiter=";")
                    header = next(reader)
                    if not encabezado_escrito:
                        writer.writerow(header)
                        encabezado_escrito = True
                    for row in reader:
                        writer.writerow(row)

def get_year_quarter_and_file_type(route_file):
    """Devuelve el año, el trimestre y si se trata de un archivo hogar o de individuos"""
    columns_needed = ["ANO4", "TRIMESTRE"]
    with route_file.open("r", newline=""):
        df = pd.read_csv(route_file, encoding="UTF-8", sep=";", usecols=columns_needed, low_memory=False)
    year = int(df["ANO4"].unique())
    quarter = int(df["TRIMESTRE"].unique())
    if "hogar" in route_file.name.lower():
        file_type = "hogar"
    elif "individual" in route_file.name.lower():
        file_type = "individual"
    else:
        return None
    return year, quarter, file_type
        

def data_dates(route_file):
    """Devuelve un diccionario con los trimestres que contiene el dataset para cada año,
    y los tipos de archivos existentes para el trimestre de ese año"""
    quarters_for_year = {}
    for trimestre in route_file.iterdir():
        # Si no es una carpeta, pasa al siguiente archivo
        if not trimestre.is_dir():
            continue
        # Para cada archivo dentro de la subcarpeta obtiene año, trimestre y tipo de archivo
        # y lo almacena en el diccionario
        for file in trimestre.iterdir():
            try:
                year, quarter, type = get_year_quarter_and_file_type(file)
            except:
                continue
            if year not in quarters_for_year.keys():
                quarters_for_year[year] = {quarter: [type]}
            elif quarter not in quarters_for_year[year].keys():
                quarters_for_year[year][quarter] = [type]
            else:
                quarters_for_year[year][quarter].append(type)
    return quarters_for_year

def check_dataset():
    """Chequea desde la estructura que retorna 'data_dates' que cada archivo encontrado (de hogar o de individuos) 
    tenga su archivo complementario restante"""
    missing_files = []
    
    data_dates_dict = data_dates(DATA_PATH)
    for year in data_dates_dict:
        for quarter in data_dates_dict[year]:
            if "hogar" not in data_dates_dict[year][quarter]:
                missing_files.append((year, quarter, "hogares"))
            if "individual" not in data_dates_dict[year][quarter]:
                missing_files.append((year, quarter, "individuos"))
    
            
    return missing_files
    

def range_dataset():
    """
        Se calcula y devuelve el año maximo y minimo, y a partir del trimestre se agrega como fecha el mes de inicio de ese trimestre
    """
    quarters_for_year = data_dates(DATA_PATH)
    # Se calculan el min y el max
    min_year = min(quarters_for_year.keys())
    max_year = max(quarters_for_year.keys())
    return 3*(min(quarters_for_year[min_year].keys()) - 1) + 1, min_year, 3 * max(quarters_for_year[max_year].keys()), max_year

def init_file_reset():
    """
        Se reinician los datasets invocando las funciones que junta todos los archivos disponibles de la carpeta file en dos datasets,
        uno para individuos y otro para hogares
    """
    home_init_file = DATA_PATH / "usu_hogar_inicial.csv"
    individual_init_file = DATA_PATH / "usu_individual_inicial.csv"
    all_togetherH(home_init_file)
    all_togetherI(individual_init_file)
    
    