import csv
from src.constantes import DATA_PATH
from src.funcionesI import all_togetherI
from src.funcionesH import all_togetherH

def range_dataset():
    home_init_file = DATA_PATH / "usu_hogar_inicial.csv"
    quarters_for_year = {}
    with open(home_init_file, newline='', encoding="utf-8") as file:
        reader =csv.DictReader(file, delimiter=";")
        for row in reader:
            quarters_for_year[int(row["ANO4"])] = set()
            quarters_for_year[int(row["ANO4"])].add(int(row["TRIMESTRE"]))
    min_year = min(quarters_for_year)
    max_year = max(quarters_for_year)
    return 3*(min(quarters_for_year[min_year]) - 1) + 1, min_year, 3 * max(quarters_for_year[max_year]), max_year

def init_file_reset():
    home_init_file = DATA_PATH / "usu_hogar_inicial.csv"
    individual_init_file = DATA_PATH / "usu_individual_inicial.csv"
    all_togetherH(home_init_file)
    all_togetherI(individual_init_file)