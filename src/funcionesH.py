import csv
from src.constantes import DATA_PATH

def all_togetherH(path_salida):
    """Junta todos los datos de los archivos hogar a un único archivo."""
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

def home_density(path_entrada, path_salida):
    """Agrega la columna DENSIDAD_HOGAR y le calcula su resultado para cada fila."""
    # Abro la salida en "r+" porque el archivo ya estará creado y modificado previamente por mis compañeros
    with path_entrada.open("r", newline="") as entrada, path_salida.open("r+", newline="") as salida:
        new_column = "DENSIDAD_HOGAR"
        reader = csv.DictReader(entrada, delimiter=";")
        columns = reader.fieldnames + [new_column]
        writer = csv.DictWriter(salida, fieldnames=columns, delimiter=";")
        writer.writeheader()
        for row in reader:
            density = int(row["IX_TOT"]) / int(row["II1"]) if int(row["II1"]) != 0 else 0
            row[new_column] = "BAJO" if density < 1 else ("ALTO" if density > 2 else "MEDIO")
            writer.writerow(row)