import csv
from src.constantes import DATA_PATH

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

def home_type(path_entrada, path_salida):
    """
    Genera una nueva columna llamada TIPO_HOGAR que indica el tipo de hogar:
        - "Unipersonal" (una persona).
        - "Nuclear" (2 a 4 personas).
        - "Extendido" (5 o más personas).
    """
    with path_entrada.open("r", newline="") as file_in, path_salida.open("w", newline="") as file_out:
        reader = csv.DictReader(file_in, delimiter=";")
        columns = reader.fieldnames + ["TIPO_HOGAR"]
    # Escribir los datos con la nueva columna
        writer = csv.DictWriter(file_out, fieldnames=columns, delimiter=";")
        writer.writeheader()
        for row in reader:
            amount = int(row["IX_TOT"])
            row["TIPO_HOGAR"] = (
                "Unipersonal" if amount == 1 else
                "Nuclear" if 2 <= amount <= 4 else
                "Extendido"
            )
            writer.writerow(row)
                        
def home_density(path_entrada, path_salida):
    """
    Agrega la columna DENSIDAD_HOGAR y le calcula su resultado para cada fila.
    Args:
        path_entrada (Path): Ruta al archivo de hogares del cual se leera.
        path_salida (Path): Ruta al directorio donde se guardara el archivo procesado.
    Returns:
        None
    """
    
    # Abro el archivo correspondiente de lectura y escritura
    with path_entrada.open("r", newline="") as entrada, path_salida.open("w", newline="") as salida:
        new_column = "DENSIDAD_HOGAR"
        reader = csv.DictReader(entrada, delimiter=";")
        columns = reader.fieldnames + [new_column]
        writer = csv.DictWriter(salida, fieldnames=columns, delimiter=";")
        writer.writeheader()
        for row in reader:
            try:
                density = int(row["IX_TOT"]) / int(row["II1"]) if int(row["II1"]) != 0 else 0
            except ValueError:
                row[new_column] = "FALTA INFORMACIÓN"
            else:
                row[new_column] = "BAJO" if density < 1 else ("ALTO" if density > 2 else "MEDIO")
            writer.writerow(row)

def habitability_condition(header, data, out_data):
    """calcula un coeficiciente que define una categoría de condición de habitabilidad
    y agrega dicha categoria en la columna "CONDICION DE HABITABILIDAD" """
    def verif_data(line):
        """Verifica las condiciones para calcular el coeficiente"""
        c = ["IV6", "IV7", "IV8", "IV9", "IV10", "IV11"]
        r = ["0", "1", "2", "3", "4"]
        for column in c:
            if (line[header.index(column)] not in r or line[header.index("IV7")] == "4"):
                return False
        return True
    def verif_hab_cond(coef):
        """define la condicion de habitabilidad en base al valor del coeficiente"""
        if coef <= 0.3:
            return "INSUFICIENTE"
        elif coef <= 0.7:
            return "REGULAR"
        elif coef <= 0.9:
            return "SALUDABLE"
        else:
            return "BUENA"

    # DICCIONARIOS DE CALIFICACIÓN
    d_iv6 = {       # ¿Tiene agua?
        "1" : 1,    # En la vivienda
        "2" : 0.5,  # Fuera de la vivienda, dentro del terreno
        "3" : 0,    # Fuera del terreno
        "0" : 0     # No tiene agua
    }
    d_iv7 = {       # Tipo de agua
        "1" : 1,    # Red pública (agua corriente)
        "2" : 0.8,  # Perforación en pozo con bomba
        "3" : 0.5,  # Perforación con bomba manual
        "4" : None, # Otra fuente
        "0" : None  # No hay información
    }
    d_iv8 = {       # ¿Tiene baño/letrina?
        "1" : 1,    # Si
        "2" : 0,    # No
        "0" : None  # No hay información
    }
    d_iv9 = {       # El baño/letrina está...
        "1" : 1,    # Dentro de la vivienda
        "2" : 0.5,  # Fuera de la vivienda, dentro del terreno
        "3" : 0,    # Fuera del terreno
        "0" : 0     # No tiene baño/letrina
    }               
    d_iv10 = {      # El baño tiene...
        "1" : 1,    # Inodoro con botón/mochila/cadena y arrastre de agua
        "2" : 0.7,  # Inodoro sin botón/cadena y con arrastre de agua (a balde)
        "3" : 0,    # Letrina (sin arrastre de agua)
        "0" : 0     # No tiene baño/letrina
    }
    d_iv11 = {      # El desagüe del baño es...
        "1" : 1,    # A red pública (cloaca)
        "2" : 0.8,  # A cámara séptica y pozo ciego
        "3" : 0.5,  # Solo a pozo ciego
        "4" : 0,    # Hoyo/excavación en la tierra
        "0" : 0,    # No tiene baño/letrina
    }
    
    header.append("CONDICION_DE_HABITABILIDAD")
    out_data.writerow(header)
    for line in data:
        if verif_data(line):
            c_iv6 = d_iv6[line[header.index("IV6")]]
            c_iv7 = d_iv7[line[header.index("IV7")]]
            c_iv8 = d_iv8[line[header.index("IV8")]]
            c_iv9 = d_iv9[line[header.index("IV9")]]
            c_iv10 = d_iv10[line[header.index("IV10")]]
            c_iv11 = d_iv11[line[header.index("IV11")]]
            # Hace una salvedad de los datos que serian descartados, pero que por lógica daría "INSUFICIENTE"
            if 0 in (c_iv6, c_iv7, c_iv8, c_iv9, c_iv10, c_iv11):
                coef = 0
            else:
                coef = c_iv6 * c_iv7 * c_iv8 * c_iv9 * c_iv10 * c_iv11
            out_data.writerow(line[:] + [verif_hab_cond(coef)])
        else:
            out_data.writerow(line[:] + ["SIN DATOS"])

def set_habitability_condition(archivo_completo, archivo_salida):
    with open(archivo_completo, "r", newline="") as data, open(archivo_salida, "w", newline="") as data_out:
        data_reader = csv.reader(data, delimiter=";")
        header = next(data_reader)
        data_out_csv = csv.writer(data_out, delimiter=";")
        habitability_condition(header, data_reader, data_out_csv)

def material(path_entrada, path_salida):
    """Genera una nueva columna llamada MATERIAL_TECHUMBRE que indica el tipo de hogar basado en el campo V4
    Material durable: si la cubierta exterior del techo es de membrana/cubierta asfáltica, baldosa/losa sin cubierta, pizarra/teja, o
    chapa de metal sin cubierta.
    Material precario: si la cubierta exterior del techo es de chapa de fibrocemento/plástico, chapa de cartón o saña/tabla/paja con barro/
    paja sola.
    No aplica: si el departamento está en propiedad horizontal
    """
    with open(path_entrada, "r", encoding="utf-8", newline="") as data_in, open(path_salida, "w", encoding="utf-8", newline="") as data_out:
        reader = csv.reader(data_in, delimiter=";")
        writer = csv.writer(data_out, delimiter=";")
        
        try:
            header = next(reader)
        except StopIteration:
            print("El archivo de entrada está vacío.")
            return
    
        header.append("MATERIAL_TECHUMBRE")
        writer.writerow(header)
        
        column = header.index("IV4")
        
        for line in reader:
            try:
                material = int(line[column])
                if material in (1, 2, 3, 4):
                    label = "Material durable"
                elif material in (5, 6, 7):
                    label = "Material precario"
                elif material == 9:
                    label = "No aplica"
                else:
                    label = "N/D"
            except (ValueError, IndexError):
                label = "Dato inválido"
            row = line[:] + [label]
            writer.writerow(row)