from pathlib import Path
import sys
PROJECT_PATH = Path(__file__).parent.parent # Path al directorio del proyecto
DATA_PATH = PROJECT_PATH / "files" # Path a los archivos de la EPH
DATA_OUT_PATH = PROJECT_PATH / "data_out" # Path para los archivos procesados
SRC_PATH = PROJECT_PATH / "src" # Agregar 'src' al path si no está
if str(SRC_PATH) not in sys.path:
    sys.path.append(str(SRC_PATH))