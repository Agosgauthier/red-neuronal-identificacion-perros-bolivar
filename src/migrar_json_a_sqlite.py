
import json
from pathlib import Path
from contextlib import closing

from src.db import (
    inicializar_base_datos,
    obtener_conexion,
)


BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_JSON = BASE_DIR / "data" / "found" / "datos.json"


def migrar_registros():
    if not RUTA_JSON.exists():
        print("No se encontró datos/found/datos.json.")
        return

    with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
        registros = json.load(archivo)

    if not isinstance(registros, list):
        raise ValueError("El JSON debe contener una lista de registros.")

    inicializar_base_datos()

    migrados = 0
    omitidos = 0

    with closing(obtener_conexion()) as conexion:
        with conexion:
            for registro in registros:
                nombre_imagen = registro.get("imagen")

                if not nombre_imagen:
                    print("Se omitió un registro sin nombre de imagen.")
                    omitidos += 1
                    continue

                existe = conexion.execute(
                    """
                    SELECT 1
                    FROM perros_encontrados
                    WHERE imagen = ?
                    LIMIT 1
                    """,
                    (nombre_imagen,),
                ).fetchone()

                if existe:
                    omitidos += 1
                    continue

                conexion.execute(
                    """
                    INSERT INTO perros_encontrados (
                        imagen,
                        zona,
                        fecha,
                        descripcion,
                        contacto,
                        fecha_registro
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        nombre_imagen,
                        registro.get("zona", ""),
                        registro.get("fecha", ""),
                        registro.get("descripcion", ""),
                        registro.get("contacto", ""),
                        registro.get("fecha_registro", ""),
                    ),
                )

                migrados += 1

    print(f"Registros migrados: {migrados}")
    print(f"Registros omitidos: {omitidos}")
    print("El JSON original se conservó sin modificaciones.")


if __name__ == "__main__":
    migrar_registros()
