import csv
from collections import Counter

def last_quarter(file_path):
    """
    Calcula el trimestre procesado en un archivo.
    Args:
        file_path (Path): Ruta al archivo del cual se leera.
    Returns:
        year (int): Año del trimestre más reciente procesado.
        quarter (int): Número del trimestre más reciente procesado.
    """
    
    with file_path.open("r", newline="") as file:
        file_reader = csv.DictReader(file, delimiter=";")
        year, quarter = max(((int(row["ANO4"]), int(row["TRIMESTRE"])) for row in file_reader), key=lambda x: (x[0], x[1]))
    return year, quarter

def compare_unfinished_high_school(path_individual):
    """
    Compara dos aglomerados según el porcentaje de personas mayores de edad con secundario incompleto.
    Args:
        path_individual (Path): Ruta al archivo usu_individual_final del cual se leera.
    Returns:
        None
    """

    # Guardo los aglomerados para asegurarme que el usuario ingresa aglomerados válidos
    with path_individual.open("r", newline="") as file:
        reader = csv.DictReader(file, delimiter=";")
        conglomerates = {row["AGLOMERADO"] for row in reader}

    # Le pido al usuario los aglomerados a comparar
    while True:
        conglomerateA = input("Aglomerado A: ")
        if conglomerateA not in conglomerates:
            print("ERROR: El aglomerado que introdujo no es válido, por favor, intente de nuevo.")
            continue
        break

    while True:
        conglomerateB = input("Aglomerado B: ")
        if conglomerateB not in conglomerates:
            print("ERROR: El aglomerado que introdujo no es válido, por favor, intente de nuevo.")
            continue
        break

    with path_individual.open("r", newline="") as file:
        reader = csv.DictReader(file, delimiter=";")

        # Creo un contador donde para cada año y trimestre me contara la cantidad de adultos por aglomerado, y
        # hago otro donde calculo la cantidad de adultos que no terminaron el secundario para cada año y trimestre
        # por aglomerado
        adults = Counter()
        unfinished_adults = Counter()

        # Para cada persona verifico a que aglomerado pertenece y si es mayor de edad, y en caso de serlo,
        # verifico si tiene el secundario incompleto
        for person in reader:
            if person["AGLOMERADO"] in (conglomerateA, conglomerateB) and int(person["CH06"]) >= 18:
                adults.update({(person["AGLOMERADO"], person["ANO4"], person["TRIMESTRE"]): 1})
                if person["NIVEL_ED_str"] == "SECUNDARIO INCOMPLETO":
                    unfinished_adults.update({(person["AGLOMERADO"], person["ANO4"], person["TRIMESTRE"]): 1})
        
        # Guardo todos los años y trimestres para luego poder imprimirlos en orden
        all_periods = {(year, quarter) for conglomerate, year, quarter in adults.keys()}
        sorted_periods = sorted(all_periods, key=lambda x: (int(x[0]), int(x[1])))

        # Imprimo para cada año y trimestre la comparación de porcentajes entre ambos aglomerados
        print(f"{'Año':<6} {'Trimestre':<11} {'Aglomerado ' + conglomerateA:<20} {'Aglomerado ' + conglomerateB:<20}")
        for year, quarter in sorted_periods:
            percentageA = 100 * unfinished_adults.get((conglomerateA, year, quarter), 0) / adults[(conglomerateA, year, quarter)]
            percentageB = 100 * unfinished_adults.get((conglomerateB, year, quarter), 0) / adults[(conglomerateB, year, quarter)]
            print(f"{year:<6} {quarter:<11} {f'{percentageA:.2f}%':<20} {f'{percentageB:.2f}%':<20}")

def retired_insufficient(path_individual, path_home):
    """
    Calcula el porcentaje de jubilados que viven en condiciones de habitabilidad insuficientes por aglomerado.
    Args:
        path_individual (Path): Ruta al archivo usu_individual_final del cual se leera.
        path_home (Path): Ruta al archivo usu_hogar_final del cual se leera.
    Returns:
        None
    """

    # Calculo el ultimo trimestre y me guardo su número y el año correspondiente
    max_year, max_quarter = last_quarter(path_home)

    with path_individual.open("r", newline="") as individual, path_home.open("r", newline="") as home:
        # Creo un contador donde para cada conglomerado me contara la cantidad de jubilados, y hago otro
        # donde calculo la cantidad de jubilados que viven en condiciones insuficientes para cada conglomerado
        retired_counter = Counter()
        retired_counter_insufficient = Counter()

        individual_reader = csv.DictReader(individual, delimiter=";")
        home_reader = csv.DictReader(home, delimiter=";")
        
        # Guardo las casas que corresponden al último trimestre
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
        print("\nPORCENTAJE DE JUBILADOS VIVIENDO EN CONDICIÓN DE HABITABILIDAD INSUFICIENTE POR AGLOMERADO:")
        for conglomerate in sorted(retired_counter, key=int):
            percentage = (100 * retired_counter_insufficient.get(conglomerate, 0)) / retired_counter[conglomerate]
            print(f"Aglomerado {conglomerate}: {percentage:.2f}%")

def filter_by_year_and_trimester(data, year='', tri=''):
    """Filtra un dataset por año y trimestre ingresados por parámetro o por teclado"""
    #Verifica que el año ingresado sea válido (se supone datasets entre 2016 y 2024)
    while type(year) != int or (year < 2016 or year > 2024):
        try:
            year = int(input("Ingrese año: "))
        except:
            print("Ingrese un año válido")
        else:
            if (year < 2016 or year > 2024):
                print("Ingrese un año entre 2016 y 2024")
    #Verifica que el trimestre sea válido (1 a 4)
    while type(tri) != int or (tri < 1 or tri > 4):
        try:
            tri = int(input("Ingrese trimestre: "))
        except:
            print("Ingrese un número del 1 al 4")
        else:
            if (tri < 1 or tri > 4):
                print("Ingrese un número del 1 al 4")
    reader = csv.DictReader(data, delimiter=";")
    #Devuelve un iterable tipo 'filter' con los datos del año y trimestre seleccionado
    data_out = filter(lambda line: line["ANO4"] == str(year) and line["TRIMESTRE"] == str(tri), reader)
    return data_out, year, tri
def foreign_university_student_percent(data):
    """Calcula el porcentaje de extranjeros que cursaron un nivel universitario o superior
    en un determinado trimestre, elegido por el usuario"""
    with open(data) as database:
        filtered_data, year, tri = filter_by_year_and_trimester(database)
        foreign_count = 0
        foreign_uni_stu_count = 0
        for line in filtered_data:
            if line["CH15"] in ("4", "5"):
                foreign_count += int(line["PONDERA"])
                if line["NIVEL_ED_str"] == "SUPERIOR O UNIVERSITARIO":
                    foreign_uni_stu_count += int(line["PONDERA"])
    if foreign_count == 0:
        print("No hay información sobre el trimestre seleccionado")
        return None
    perc = foreign_uni_stu_count * 100 / foreign_count
    print(f"""AÑO: {year} TRIMESTRE: {tri}\nPorcentaje de personas no nacidas en Argentina que cursaron un nivel universitario o superior: {perc:.3f}%""")
    return perc

def adults_per_education_level(path_individual):
    #Pido el aglomerado al usuario
    conglomerates = input("Ingrese el numero de aglomerado: ")
    #Creo una lista con los niveles de educacion
    education_levels = [
        "PRIMARIO INCOMPLETO",
        "PRIMARIO COMPLETO",
        "SECUNDARIO INCOMPLETO",
        "SECUNDARIO COMPLETO",
        "SUPERIOR O UNIVERSITARIO"
    ]

    #Agrupo por (año, trimestre) en un diccionario
    year_quarter_dicc = {}

    with open(path_individual, newline='') as file:
        reader = csv.DictReader(file, delimiter=';')

        for row in reader:
            #Verifico si el aglomerado es el que me pidieron 
            if row["AGLOMERADO"] == conglomerates:
                age = int(row["CH06"])
                #Filtro por edad y por nivel de educacion                
                if age >= 18:
                    education_level = row["NIVEL_ED_str"]
                    if education_level in education_levels:
                        year = row["ANO4"]                      
                        quarter = row["TRIMESTRE"]
                        key = (year, quarter) #Formo la clave (año, trimestre)
                        if key not in year_quarter_dicc: 
                            year_quarter_dicc[key] = Counter() #Si es la primera vez que se encuentra creo el contador
                            
                        year_quarter_dicc[key][education_level] += int(row["PONDERA"]) #sumo la ponderacion al contador correspondiente

    #Imprimo encabezado
    print(f"\nNombre de Aglomerado: {conglomerates}")
    print(f"{'Año':<6} {'Trimestre':<10} " + "  ".join(f"{education_level:<25}" for education_level in education_levels))
    print("-" * (6 + 10 + 27 * len(education_levels)))

    #Imprimo datos ordenados por año y trimestre
    for (year, quarter) in sorted(year_quarter_dicc):
        print(f"{year:<6} {quarter:<10} ", end='')
        for education_level in education_levels:
            print(f"{year_quarter_dicc[(year, quarter)].get(education_level, 0):<25}", end='  ')
        print()   

def max_homes_cluster(path_home):
    """
        Informar el aglomerado con mayor cantidad de viviendas con más de dos ocupantes
        y sin baño. Informar también la cantidad de ellas (ponderadas).
        Se utiliza IV8 para saber si tiene baño o no,  
        IX_TOT para cantidad de personas en el hogar,
        PONDERADOR_HOGAR para ponderar cada fila.
    """
    with path_home.open("r", newline="") as file:
        dict_reader = csv.DictReader(file, delimiter=";")
        dict_agglomerate = {}

        # Se Itera cada fila del reader y si no tiene baño y tiene mas de 2 habitantes se guarda en un diccionario el aglomerado y el ponderador com ovalor
        for row in dict_reader:
            if int(row["IV8"]) == 2 and int(row["IX_TOT"]) > 2:
                agglomerate = row["AGLOMERADO"]
                weighter = int(row["PONDERA"])  
                if agglomerate not in dict_agglomerate:
                    dict_agglomerate[agglomerate] = 0
                dict_agglomerate[agglomerate] += weighter

        # Se calcula el maximo si no esta vacio el dicionario
        if dict_agglomerate:
            max_agglomerate = max(dict_agglomerate.items(), key=lambda x: x[1])
            print(f"Aglomerado con más viviendas sin baño y más de dos ocupantes: {max_agglomerate[0]}, cantidad hogares: {max_agglomerate[1]}")
        else:
            print("No se encontraron viviendas que cumplan la condición.")

def percentage_university_level_clusters(path_individual):
    """
        Informar para cada aglomerado el porcentaje de personas que hayan cursado al
        menos en nivel universitario o superior. UNIVERSITARIO
    """
    with path_individual.open("r", newline="") as file:
        dict_reader = csv.DictReader(file, delimiter=";")
        

        university_counts = {}
        total_counts = {}
        
        for row in dict_reader:
            education_level = int(row["UNIVERSITARIO"])
            
            # Filtro los casos que no aplican si UNIVERSITARIO = 2
            if education_level in [0, 1]:
                cluster = row["AGLOMERADO"]
                weight = int(row["PONDERA"])
                
                # Se inicializa contadores si el cluster no existe
                if cluster not in total_counts:
                    total_counts[cluster] = 0
                    university_counts[cluster] = 0
                
                total_counts[cluster] += weight
                
                # Se suman cuando es universitario
                if education_level == 1:
                    university_counts[cluster] += weight
        
        # Se imprimen los aglomerados con su porcentaje de  universitarios
        print("\nPorcentaje universitario por cluster:")
        print("----------------------------------")
        for cluster in sorted(total_counts.keys(), key=int):
            if total_counts[cluster] > 0:
                percentage = (university_counts[cluster] / total_counts[cluster]) * 100
                print(f"Aglomerado {int(cluster):>2}: {round(percentage, 2)}%") 
        
        print("----------------------------------")