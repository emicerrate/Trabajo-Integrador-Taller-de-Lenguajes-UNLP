import csv
from src.constantes import DATA_PATH
from src.funcionesI import all_togetherI
from src.funcionesH import all_togetherH

def range_dataset():
    home_init_file = DATA_PATH / "usu_hogar_inicial.csv"
    years = set()
    quarters = set()
    with open(home_init_file, newline='', encoding="utf-8") as file:
        reader =csv.DictReader(file, delimiter=";")
        for row in reader:
            years.add(int(row["ANO4"]))
            quarters.add(int(row["TRIMESTRE"]))
    return min(quarters), min(years), max(quarters), max(years)

def init_file_reset():
    home_init_file = DATA_PATH / "usu_hogar_inicial.csv"
    individual_init_file = DATA_PATH / "usu_individual_inicial.csv"
    all_togetherH(home_init_file)
    all_togetherI(individual_init_file)