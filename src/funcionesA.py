import csv
from constantes import DATA_OUT_PATH

def range_dataset():
    home_final_file = DATA_OUT_PATH / "usu_hogar_final.csv"
    years = set()
    quarters = set()
    with open(home_final_file, newline='', encoding="utf-8") as file:
        reader =csv.DictReader(file, delimiter=";")
        for row in reader:
            years.add(int(row["ANO4"]))
            quarters.add(int(row["TRIMESTRE"]))
    return min(quarters), min(years), max(quarters), max(years)