import csv
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

def data_dates(route_file):
    """Devuelve un diccionario con los trimestre que contiene el dataset para cada año"""
    quarters_for_year = {}
    # Se lee el archivo inicial
    with open(route_file, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            # Se genera un set para filtrar los trimestres y que se registren de manera única, el año es la key del diccionario
            if int(row["ANO4"]) not in quarters_for_year.keys():
                quarters_for_year[int(row["ANO4"])] = set()
            quarters_for_year[int(row["ANO4"])].add(int(row["TRIMESTRE"]))
    return quarters_for_year

def check_dataset():
    """Chequea que ambos 'usu_***_inicial.csv' tengan los mismos archivos según año y trimestre"""
    home_init_file = DATA_PATH / "usu_hogar_inicial.csv"
    indiv_init_file = DATA_PATH / "usu_individual_inicial.csv"
    quarters_for_year_home = data_dates(home_init_file)
    quarters_for_year_indiv = data_dates(indiv_init_file)
    missing_files = []
    # se guardan los trimestres que faltan en el archivo de individuos
    for year in quarters_for_year_home:
        if year not in quarters_for_year_indiv.keys():
            for quarter in quarters_for_year_home[year]:
                missing_files.append((year, quarter, "individuos"))
        elif quarters_for_year_home[year] != quarters_for_year_indiv[year]:
            for quarter in quarters_for_year_home[year]:
                if quarter not in quarters_for_year_indiv[year]:
                    missing_files.append((year, quarter, "individuos"))
    # se guardan los trimestres que faltan en el archivo de hogares
    for year in quarters_for_year_indiv:
        if year not in quarters_for_year_home.keys():
            for quarter in quarters_for_year_indiv[year]:
                missing_files.append((year, quarter, "hogares"))
        elif quarters_for_year_indiv[year] != quarters_for_year_home[year]:
            for quarter in quarters_for_year_indiv[year]:
                if quarter not in quarters_for_year_home[year]:
                    missing_files.append((year, quarter, "hogares"))
    return missing_files
    

def range_dataset():
    """
        Se calcula y devuelve el año maximo y minimo, y a partir del trimestre se agrega como fecha el mes de inicio de ese trimestre
    """
    home_init_file = DATA_PATH / "usu_hogar_inicial.csv"
    quarters_for_year = data_dates(home_init_file)
    # Se calculan el min y el max
    min_year = min(quarters_for_year)
    max_year = max(quarters_for_year)
    return 3*(min(quarters_for_year[min_year]) - 1) + 1, min_year, 3 * max(quarters_for_year[max_year]), max_year

def init_file_reset():
    """
        Se reinician los datasets invocando las funciones que junta todos los archivos disponibles de la carpeta file en dos datasets,
        uno para individuos y otro para hogares
    """
    home_init_file = DATA_PATH / "usu_hogar_inicial.csv"
    individual_init_file = DATA_PATH / "usu_individual_inicial.csv"
    all_togetherH(home_init_file)
    all_togetherI(individual_init_file)
    