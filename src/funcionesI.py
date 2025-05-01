import csv
from src.constantes import DATA_PATH

def all_togetherI(path_salida):
    """Junta todos los datos de los archivos individuales a un único archivo."""
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
    """Agrega la columna UNIVERSITARIO y le calcula su resultado para cada fila."""
    # Abro la salida en "r+" porque el archivo ya estará creado y modificado previamente por mis compañeros
    with path_entrada.open("r", newline="") as entrada, path_salida.open("r+", newline="") as salida:
        new_column = "UNIVERSITARIO"
        reader = csv.DictReader(entrada, delimiter=";")
        columns = reader.fieldnames + [new_column]
        writer = csv.DictWriter(salida, fieldnames=columns, delimiter=";")
        writer.writeheader()
        for row in reader:
            row[new_column] = 2 if int(row["CH06"]) < 18 else (1 if row["NIVEL_ED"] == "6" else 0)
            writer.writerow(row)