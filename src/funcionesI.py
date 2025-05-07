import csv

from src.constantes import DATA_PATH

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

def university(path_entrada, path_salida):
    """
    Agrega la columna UNIVERSITARIO y le calcula su resultado para cada fila.
    Args:
        path_entrada (Path): Ruta al archivo de individuos del cual se leera.
        path_salida (Path): Ruta al directorio donde se guardara el archivo procesado.
    Returns:
        None
    """

    # Abro el archivo correspondiente de lectura y escritura
    with path_entrada.open("r", newline="") as entrada, path_salida.open("w+", newline="") as salida:
        new_column = "UNIVERSITARIO"
        reader = csv.DictReader(entrada, delimiter=";")
        columns = reader.fieldnames + [new_column]
        writer = csv.DictWriter(salida, fieldnames=columns, delimiter=";")
        writer.writeheader()
        for row in reader:
            row[new_column] = 2 if int(row["CH06"]) < 18 else (1 if row["NIVEL_ED"] == "6" else 0)
            writer.writerow(row)


def education_level_ref(line, column):
    """Diccionario de referencia para los niveles educativos"""
    dict_ref = {
        "1" : "PRIMARIO INCOMPLETO",
        "2" : "PRIMARIO COMPLETO",
        "3" : "SECUNDARIO INCOMPLETO",
        "4" : "SECUNDARIO COMPLETO",
        "5" : "SUPERIOR O UNIVERSITARIO",
        "6" : "SUPERIOR O UNIVERSITARIO",
        "7" : "SIN INFORMACIÓN",
        "9" : "SIN INFORMACIÓN"
    }
    return dict_ref[line[column]]
    
def education_level(archivo_entrada, archivo_salida):
    """Agrega la columna 'NIVEL_ED_str' que indica el máximo nivel educativo en cadena de texto."""
    with open(archivo_entrada, "r") as data_ind, open(archivo_salida, "w", newline="") as data_out:
        data_ind = csv.reader(data_ind, delimiter=";")
        data_out_csv = csv.writer(data_out, delimiter=";")
        header = next(data_ind)
        header.append("NIVEL_ED_str")
        data_out_csv.writerow(header)
        column = header.index("NIVEL_ED")
        for line in data_ind:
            row = line[:] + [education_level_ref(line, column)]
            data_out_csv.writerow(row)

def gender(archivo_entrada, archivo_salida):
    'Agrega la columna CH04_str que indica el género según los valores de CH04.'
    with open(archivo_entrada, "r") as data_ind, open(archivo_salida, "w", newline="") as data_out:
        data_ind = csv.reader(data_ind, delimiter=";")
        data_out_csv = csv.writer(data_out, delimiter=";")
        header = next(data_ind)
        header.append("CH04_str")  
        data_out_csv.writerow(header)
        CHO4_INDEX = header.index("CH04")
        
        for line in data_ind:
            CH04_value = line[CHO4_INDEX]  
            if CH04_value == "1":
                gender = "Masculino"
            else:
                gender = "Femenino"
            row = line[:] + [gender]
            data_out_csv.writerow(row)

def condition(archivo_entrada, archivo_salida):
    with open(archivo_entrada, newline="") as data_in, open(archivo_salida, "w", newline="") as data_out:
        reader = csv.reader(data_in, delimiter=";")
        writer = csv.writer(data_out, delimiter=";")
        
        try:
            header = next(reader)
        except StopIteration:
            print("El archivo de entrada está vacío.")
            return
        
        column_estado = header.index("ESTADO")
        column_cat = header.index("CAT_OCUP")

        header.append("CONDICION_LABORAL")
        writer.writerow(header)

        for line in reader:
            state = int(line[column_estado])
            cat = int(line[column_cat])
            if (state == 1) and (cat in (1,2)):
                label = "Ocupado autónomo"
            elif (state == 1) and (cat in (3,4,9)):
                label = "Ocupado dependiente"
            elif state == 2:
                label = "Desocupado"
            elif state == 3:
                label = "Inactivo"
            elif state == 4:
                label = "Fuera de categoría/sin información"
            else:
                label = "No sé qué onda, en estos casos no se explicita qué es lo que se quiere que pase."
            
            row = line[:] + [label] 
            writer.writerow(row)