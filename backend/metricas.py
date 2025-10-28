import csv
import os
from datetime import datetime
from typing import Dict, List

BASE_DIR = os.path.dirname(__file__)
BUSQUEDAS_FILE = os.path.join(BASE_DIR, "busquedas.csv")


def registrar_busqueda(marca: str, modelo: str, motor: str, anio: str, cantidad_resultados: int) -> None:
    """Registra una búsqueda en el archivo de métricas."""
    os.makedirs(BASE_DIR, exist_ok=True)
    archivo_existe = os.path.exists(BUSQUEDAS_FILE)

    with open(BUSQUEDAS_FILE, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo, delimiter=";")
        if not archivo_existe:
            escritor.writerow(["timestamp", "marca", "modelo", "motor", "anio", "total_resultados"])

        escritor.writerow(
            [
                datetime.now().isoformat(timespec="seconds"),
                marca.strip(),
                modelo.strip(),
                motor.strip(),
                anio.strip(),
                int(cantidad_resultados),
            ]
        )


def cargar_busquedas() -> List[Dict[str, str]]:
    """Devuelve la lista de búsquedas registradas."""
    if not os.path.exists(BUSQUEDAS_FILE):
        return []

    with open(BUSQUEDAS_FILE, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo, delimiter=";")
        return list(lector)
