import csv
from collections import Counter

def retired_insufficient(path_individual, path_home):
    """
    Calcula el porcentaje de jubilados que viven en condiciones de habitabilidad insuficientes por aglomerado.
    Args:
        path_individual (Path): Ruta al archivo usu_individual_final del cual se leera.
        path_home (Path): Ruta al archivo usu_hogar_final del cual se leera.
    Returns:
        None
    """

    # Calculo el ultimo trimestre y me guardo su numero y el año correspondiente
    with path_home.open("r", newline="") as home:
        home_reader = csv.DictReader(home, delimiter=";")
        max_year, max_quarter = max(((int(house["ANO4"]), int(house["TRIMESTRE"])) for house in home_reader), key=lambda x: (x[0], x[1]))

    with path_individual.open("r", newline="") as individual, path_home.open("r", newline="") as home:
        # Creo un contador donde para cada conglomerado me contara la cantidad de jubilados, y hago otro
        # donde calculo la cantidad de jubilados que viven en condiciones insuficientes para cada conglomerado
        retired_counter = Counter()
        retired_counter_insufficient = Counter()

        individual_reader = csv.DictReader(individual, delimiter=";")
        home_reader = csv.DictReader(home, delimiter=";")
        
        # Guardo las casas que corresponden al ultimo trimestre
        houses = {house["CODUSU"]: house for house in home_reader if int(house["ANO4"]) == max_year and int(house["TRIMESTRE"]) == max_quarter}
        
        # Para cada persona verifico si es o no jubilado, en caso de serlo, sus condiciones de habitabilidad
        # y finalmente los voy contando
        for person in individual_reader:
            if person["ANO4"] == str(max_year) and person["TRIMESTRE"] == str(max_quarter):
                if person["CONDICION_LABORAL"] == "Inactivo" and person["CAT_INAC"] == "1":
                    retired_counter.update({person["AGLOMERADO"]: 1})
                    if houses[person["CODUSU"]]["CONDICION_DE_HABITABILIDAD"] == "INSUFICIENTE":
                        retired_counter_insufficient.update({person["AGLOMERADO"]: 1})
        
        # Imprimo para cada aglomerado en orden ascendente su porcentaje
        print("PORCENTAJE DE JUBILADOS VIVIENDO EN CONDICIÓN DE HABITABILIDAD INSUFICIENTE POR CONGLOMERADO:\n")
        for conglomerate in sorted(retired_counter, key=int):
            percentage = (100 * retired_counter_insufficient.get(conglomerate, 0)) / retired_counter[conglomerate]
            print(f"Aglomerado {conglomerate}: {percentage:.2f}%")