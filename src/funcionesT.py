import csv
from collections import Counter

def agglomeration_id():
    dict_ag_id = {
    "2" : "Gran La Plata",
    "3" : "Bahía Blanca - Cerri",
    "4" : "Gran Rosario",
    "5" : "Gran Santa Fé",
    "6" : "Gran Paraná",
    "7" : "Posadas",
    "8" : "Gran Resistencia",
    "9" : "Comodoro Rivadavia - Rada Tilly",
    "10" : "Gran Mendoza",
    "12" : "Corrientes",
    "13" : "Gran Córdoba",
    "14" : "Concordia",
    "15" : "Formosa",
    "17" : "Neuquén – Plottier",
    "18" : "Santiago del Estero - La Banda",
    "19" : "Jujuy - Palpalá",
    "20" : "Río Gallegos",
    "22" : "Gran Catamarca",
    "23" : "Gran Salta",
    "25" : "La Rioja",
    "26" : "Gran San Luis",
    "27" : "Gran San Juan",
    "29" : "Gran Tucumán - Tafí Viejo",
    "30" : "Santa Rosa – Toay",
    "31" : "Ushuaia - Río Grande",
    "32" : "Ciudad Autónoma de Buenos Aires",
    "33" : "Partidos del GBA",
    "34" : "Mar del Plata",
    "36" : "Río Cuarto",
    "38" : "San Nicolás – Villa Constitución",
    "91" : "Rawson – Trelew",
    "93" : "Viedma – Carmen de Patagones"
    }
    return dict_ag_id

def region_id():
    dict_re_id = {
        "1" : "Gran Buenos Aires",
        "40" : "Noroeste",
        "41" : "Noreste",
        "42" : "Cuyo",
        "43" : "Pampeana",
        "44" : "Patagonia"
    }
    return dict_re_id

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
    ag_id = agglomeration_id()
    # Le pido al usuario los aglomerados a comparar
    print("LISTA DE AGLOMERADOS:")
    for item in ag_id:
            print(f"{item}: {ag_id[item]}")
    
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
        print(f"\nCOMPARACIÓN DE PORCENTAJE DE PERSONAS MAYORES DE EDAD CON SECUNDARIO INCOMPLETO ENTRE {ag_id[conglomerateA]} y {ag_id[conglomerateB]}")
        print(f"{'Año':<6} {'Trimestre':<11} {ag_id[conglomerateA]:<20} {ag_id[conglomerateB]:<20}")
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
    ag_id = agglomeration_id()

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
            print("{:<36} {:<8}".format(f"{ag_id[conglomerate]}:", f"{percentage:.2f}%"))

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

def adults_per_education_level(path_individual):
    
    with path_individual.open("r", newline="") as file:
        reader = list(csv.DictReader(file, delimiter=";"))  # Convierto en lista de diccionarios porque necesito correrlo mas de 1 vez
        conglomerates = {row["AGLOMERADO"] for row in reader}
    ag_id = agglomeration_id()
    print("LISTA DE AGLOMERADOS:")
    for item in ag_id:
            print(f"{item}: {ag_id[item]}")
    while True:
        conglomerate = input("Ingrese el número de aglomerado: ")
        if conglomerate not in conglomerates:
            print("ERROR: El aglomerado que introdujo no es válido, por favor, intente de nuevo.")
            continue
        break
    
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

    for row in reader:
        #Verifico si el aglomerado es el que me pidieron 
        if row["AGLOMERADO"] == conglomerate:
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
    print(f"\n{ag_id[conglomerate]}")
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
    max_year, max_quarter = last_quarter(path_home)
    with path_home.open("r", newline="") as file:
        dict_reader = csv.DictReader(file, delimiter=";")
        dict_agglomerate = {}
        ag_id = agglomeration_id()
        # Se realiza una lista filtrada con el ultimo trimestre
        quarter_filtered =  [
            row for row in dict_reader 
            if int(row["ANO4"]) == max_year and int(row["TRIMESTRE"]) == max_quarter
        ]

        # Se Itera cada fila del reader y si no tiene baño y tiene mas de 2 habitantes se guarda en un diccionario el aglomerado y el ponderador com ovalor
        for row in quarter_filtered:
            if int(row["IV8"]) == 2 and int(row["IX_TOT"]) > 2:
                agglomerate = ag_id[row["AGLOMERADO"]]
                weighter = int(row["PONDERA"])  
                if agglomerate not in dict_agglomerate:
                    dict_agglomerate[agglomerate] = 0
                dict_agglomerate[agglomerate] += weighter

        # Se calcula el maximo si no esta vacio el dicionario
        print("----------------------------------")
        print("\nAglomerado con mayor cantidad de viviendas con más de dos ocupantes y sin baño:")
        print("----------------------------------")
        if dict_agglomerate:
            max_agglomerate = max(dict_agglomerate.items(), key=lambda x: x[1])
            print(f"Aglomerado: {max_agglomerate[0]}, cantidad hogares: {max_agglomerate[1]}")
        else:
            print("No se encontraron viviendas que cumplan la condición.")
        print("----------------------------------")

def percentage_university_level_clusters(path_individual):
    """
        Informar para cada aglomerado el porcentaje de personas que hayan cursado al
        menos en nivel universitario o superior. UNIVERSITARIO
    """
    ag_id = agglomeration_id()
    max_year, max_quarter = last_quarter(path_individual)
    with path_individual.open("r", newline="") as file:
        dict_reader = csv.DictReader(file, delimiter=";")

        # Se realiza una lista filtrada con el ultimo trimestre
        quarter_filtered =  [
            row for row in dict_reader 
            if int(row["ANO4"]) == max_year and int(row["TRIMESTRE"]) == max_quarter
        ]

        university_counts = {}
        total_counts = {}
        
        for row in quarter_filtered:
            education_level = int(row["UNIVERSITARIO"])
            
            # Filtro los casos que no aplican si UNIVERSITARIO = 2
            if education_level in [0, 1]:
                cluster = ag_id[row["AGLOMERADO"]]
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
        for cluster in sorted(total_counts.keys(), key=str):
            if total_counts[cluster] > 0:
                percentage = (university_counts[cluster] / total_counts[cluster]) * 100
                print("{:<36} {:<8}".format(f"{cluster}:", f"{round(percentage, 2)} %"))
        
        print("----------------------------------")
        
def owners_occupation_per_ag(dataH):
    """Devuelve el porcentaje de viviendas ocupadas por sus propietarios, por aglomerado"""
    def occupant_clasificator(value):
        """Devuelve 'None' si desestima los datos, 'True' si es vivienda
        ocupada por propietarios y 'False' en caso contrario."""
        # II7 -> "8" (en suceción) lo considero como un 'gris' y prefiero desestimarlo
        # II7 -> "9" (Otra situacón) también es desestimada
        if value not in ("1", "2", "3", "4", "5", "6", "7"):
            return None
        elif value in ("1", "2"):
            return True
        else:
            return False
    ag_id = agglomeration_id().copy()
    
    dict_ag_list_ow_oc = {}
    #Defino un diccionario "aglomerado" : [ocupantes propietarios, total]
    for agglomeration in ag_id:
        dict_ag_list_ow_oc.update({agglomeration : [0, 0]})
    
    with dataH.open() as file:
        dict_reader = csv.DictReader(file, delimiter=";")
        for row in dict_reader:
            # Desestima datos que no definan la condición de ocupación
            if occupant_clasificator(row["II7"]) == None:
                continue
            else:
                # Actualiza la cuenta de hogares
                dict_ag_list_ow_oc[row["AGLOMERADO"]][1] += int(row["PONDERA"])
                # Actualiza la cuenta de hogares con ocupantes propietarios
                if occupant_clasificator(row["II7"]):
                    dict_ag_list_ow_oc[row["AGLOMERADO"]][0] += int(row["PONDERA"])
                    
    print("PORCENTAJE DE VIVIENDAS OCUPADAS POR SUS PROPIETARIOS:")
    
    for agglo in dict_ag_list_ow_oc:
        print("{:<36} {:<8}".format(f"{ag_id[agglo]}:", f"{(dict_ag_list_ow_oc[agglo][0] * 100 / dict_ag_list_ow_oc[agglo][1]):.3f} %"))
        
def university_insufficient(path_individual, path_home):
    # Pido año al usuario y lo valido
    while True:
        try:
            year = int(input("Ingrese un año (entre 2016 y 2024): "))
            if 2016 <= year <= 2024:
                break
            else:
                print("Por favor, ingrese un año entre 2016 y 2024.")
        except:
            print("Entrada invalida. Ingrese un numero entero.")

    with path_individual.open("r", newline="") as individual, path_home.open("r", newline="") as home:
        # Inicializo contador 
        university_counter_insufficient = 0 
        
        # Convierto en lista de diccionarios porque necesito correrlo mas de 1 vez 
        individual_reader = list(csv.DictReader(individual, delimiter=";")) 
        home_reader = list(csv.DictReader(home, delimiter=";"))
        
        # Calculo el ultimo trimestre y me guardo su numero
        max_quarter = max(int(row["TRIMESTRE"]) for row in individual_reader if int(row["ANO4"]) == year)

        # Guardo las casas que corresponden al ultimo trimestre en un diccionario
        houses = {house["CODUSU"]: house for house in home_reader if int(house["ANO4"]) == year and int(house["TRIMESTRE"]) == max_quarter}
        
        # Sumo al contador la cantidad de personas correspondientes
        for person in individual_reader:
            if person["ANO4"] == str(year) and person["TRIMESTRE"] == str(max_quarter) and person["NIVEL_ED_str"] == "SUPERIOR O UNIVERSITARIO" and houses[person["CODUSU"]]["CONDICION_DE_HABITABILIDAD"] == "INSUFICIENTE":
                university_counter_insufficient += (int(person["PONDERA"]))
        
        # Imprimo la cantidad 
        print(f"\nCANTIDAD DE PERSONAS CON NIVEL DE EDUCACION UNIVERSITARIO O SUPERIOR VIVIENDO EN CONDICION DE HABITABILIDAD INSUFICIENTE EN EL AÑO {year}, TRIMESTRE {max_quarter}: {university_counter_insufficient}")
def tenant_for_region(dataH):
    re_id = region_id()
    dict_region_tenant_data = {}
    #Defino un diccionario: {"región" : [ocupantes inquilinos, total]}
    for region in re_id:
        dict_region_tenant_data.update({region : [0, 0]})
    with dataH.open() as file:
        dict_reader = csv.DictReader(file, delimiter=";")
        for row in dict_reader:
            # Desestima los régimenes de tenencia indeterminados
            if row["II7"] in ("8", "9"):
                continue
            # Si son inquilinos de la vivienda, se actualiza la cuenta de ocupantes inquilinos
            if row["II7"] == "3":
                dict_region_tenant_data[row["REGION"]][0] += int(row["PONDERA"])
            # Actualiza la cuenta total
            dict_region_tenant_data[row["REGION"]][1] += int(row["PONDERA"])
    # Calcula los porcentajes para cada región
    region_tenant_percentage = map(lambda x: (x, dict_region_tenant_data[x][0] * 100 / dict_region_tenant_data[x][1]), dict_region_tenant_data)
    list_to_print = sorted(region_tenant_percentage, key=lambda x: x[1], reverse=True)
    print("PORCENTAJE DE INQUILINOS POR REGIÓN")
    for item in list_to_print:
        print("{:<24} {:<8}".format(f"{re_id[item[0]]}:", f"{item[1]:.3f} %"))

def literacy(path_file_individual):
    with open(path_file_individual, newline="") as file:
        reader = csv.reader(file, delimiter=";")
        try:
            header = next(reader)
        except StopIteration:
            return "El archivo de entrada está vacío."

        column_year = header.index("ANO4")
        column_tri = header.index("TRIMESTRE")
        column_pond = header.index("PONDERA")
        column_age = header.index("CH06")
        column_lit = header.index("CH09")

        data_by_year = {}
        for line in reader:
            try:
                year = int(line[column_year])
                tri = int(line[column_tri])
                pond = int(line[column_pond])
                age = int(line[column_age])
                can_read = int(line[column_lit])
            except ValueError:
                continue
            #Busca el cuarto trimestre de cada año
            if tri != 4:
                continue
            #Agrega el año al diccionario si todavía no está agregado
            if year not in data_by_year:
                data_by_year[year] = {'total': 0, 'cap': 0, 'incap': 0}

            data_by_year[year]['total'] += pond
            #Evalúa que se cumpla la condición de edad y diferencia si saben leer y escribir o no
            if age >= 6:
                if can_read == 1:
                    data_by_year[year]['cap'] += pond
                elif can_read == 2:
                    data_by_year[year]['incap'] += pond
        #Cálculo de porcentajes por año
        result = {}
        for year, values in data_by_year.items():
            total = values['total']
            cap = values['cap']
            incap = values['incap']
            percentage_cap = round((cap / total) * 100, 2) if total else 0
            percentage_incap = round((incap / total) * 100, 2) if total else 0
            result[year] = {
                "Porcentaje alfabetizados": f"{percentage_cap}%",
                "Porcentaje no alfabetizados": f"{percentage_incap}%"
            }
        #Impresión estilizada de los datos
        print("Año | % Alfabetizados | % No alfabetizados")
        print("-" * 40)

        for year in sorted(result):
            cap = result[year]["Porcentaje alfabetizados"]
            incap = result[year]["Porcentaje no alfabetizados"]
            print(f"{year} | {cap.rjust(14)} | {incap.rjust(18)}")

def top5_university_occupancy(path_individual, path_home):
    """
    Calcula los 5 aglomerados con mayor porcentaje de hogares con dos o más ocupantes con estudios universitarios 
    o superiores finalizados del último trimestre procesado. 
    Args:
        path_individual (Path): Ruta al archivo usu_individual_final del cual se leera la información de las personas.
        path_home (Path): Ruta al archivo usu_home_final del cual se leera la información de las casas.
    Return:
        None
    """

    ag_id = agglomeration_id()

    # Calculo el ultimo trimestre y me guardo su número y el año correspondiente
    max_year, max_quarter = last_quarter(path_individual)

    
    with path_individual.open("r", newline="") as individual, path_home.open("r", newline="") as home:
        individual_reader = csv.DictReader(individual, delimiter=";")
        home_reader = csv.DictReader(home, delimiter=";")

        # Creo un contador donde para cada casa iré contando cuantas personas cumplen con el requisito, otro donde para
        # cada aglomerado contaré la cantidad de casas que tiene, y un último donde para cada aglomerado contará las
        # casas que cumplen con los requisitos
        required_per_house = Counter()
        houses_per_conglomerate = Counter()
        required_houses = Counter()
        
        # Para cada persona verifico si cumple los requisitos y la sumo a su correspondiente casa
        for person in individual_reader:
            if person["ANO4"] == str(max_year) and person["TRIMESTRE"] == str(max_quarter):
                if person["NIVEL_ED_str"] == "SUPERIOR O UNIVERSITARIO":
                    required_per_house.update({person["CODUSU"]: 1})
        
        # Para cada casa la cuento en su respectivo aglomerado y si cumple la condición la cuento en las buscadas
        for house in home_reader:
            if house["ANO4"] == str(max_year) and house["TRIMESTRE"] == str(max_quarter):
                houses_per_conglomerate.update({house["AGLOMERADO"]: 1})
                if required_per_house[house["CODUSU"]] >= 2:
                    required_houses.update({house["AGLOMERADO"]: 1})

        # Calculo los porcentajes de las casas buscadas por aglomerado
        percentages = dict()
        for conglomerate in houses_per_conglomerate:
            try:
                percentages[conglomerate] = 100 * required_houses[conglomerate] / houses_per_conglomerate[conglomerate]
            except ZeroDivisionError:
                percentages[conglomerate] = 0
        
        # Me quedo con el top 5 y se lo muestro al usuario
        top5 = sorted(percentages.items(), key=lambda x: x[1], reverse=True)[:5]
        print("TOP 5 AGLOMERADOS CON MAYOR PORCENTAJE DE HOGARES CON DOS O MÁS OCUPANTES CON ESTUDIOS UNIVERSITARIOS O SUPERIORES FINALIZADOS:")
        for top, elem in enumerate(top5):
            print(f"{top+1}. {ag_id[elem[0]]}: {elem[1]:.2f}%")
