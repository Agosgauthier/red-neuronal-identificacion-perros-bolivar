import sqlite3
from pathlib import Path
from contextlib import closing

# --------------------------------------------------
# Configuración de la base de datos
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RUTA_BASE_DATOS = BASE_DIR / "data" / "perros.db"


# --------------------------------------------------
# Conexión con SQLite
# --------------------------------------------------

def obtener_conexion():
    """
    Abre una conexión con la base de datos SQLite.

    Si la carpeta data no existe, la crea.
    """
    RUTA_BASE_DATOS.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    conexion = sqlite3.connect(RUTA_BASE_DATOS)
    conexion.row_factory = sqlite3.Row

    return conexion


# --------------------------------------------------
# Inicialización de la base de datos
# --------------------------------------------------

def inicializar_base_datos():
    """
    Crea la tabla de perros encontrados si todavía no existe.
    """
    with closing(obtener_conexion()) as conexion:
        with conexion:
            conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS perros_encontrados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    imagen TEXT NOT NULL,
                    zona TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    descripcion TEXT NOT NULL DEFAULT '',
                    contacto TEXT NOT NULL,
                    fecha_registro TEXT NOT NULL
                )
                """
            )

# --------------------------------------------------
# Registrar un perro encontrado
# --------------------------------------------------

def registrar_perro(
    imagen,
    zona,
    fecha,
    descripcion,
    contacto,
    fecha_registro
):
    """
    Guarda los datos de un perro encontrado.
    Devuelve el identificador del registro creado.
    """
    with closing(obtener_conexion()) as conexion:
        with conexion:
            cursor = conexion.execute(
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
                    imagen,
                    zona,
                    fecha,
                    descripcion,
                    contacto,
                    fecha_registro
                )
            )

            return cursor.lastrowid

# --------------------------------------------------
# Buscar un perro por el nombre de su fotografía
# --------------------------------------------------

def obtener_perro_por_imagen(nombre_imagen):
    """
    Busca el registro asociado a una fotografía.

    Devuelve un diccionario si lo encuentra o None si no existe.
    """
    with closing(obtener_conexion()) as conexion:
        with conexion:
            fila = conexion.execute(
                """
                SELECT
                    id,
                    imagen,
                    zona,
                    fecha,
                    descripcion,
                    contacto,
                    fecha_registro
                FROM perros_encontrados
                WHERE imagen = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (nombre_imagen,)
            ).fetchone()

    if fila is None:
        return None

    return dict(fila)

# --------------------------------------------------
# Obtener todos los perros encontrados
# --------------------------------------------------


def obtener_perros():
    """
    Devuelve todos los registros, del más reciente al más antiguo.
    """
    with closing(obtener_conexion()) as conexion:
        with conexion:
            filas = conexion.execute(
                """
                SELECT
                    id,
                    imagen,
                    zona,
                    fecha,
                    descripcion,
                    contacto,
                    fecha_registro
                FROM perros_encontrados
                ORDER BY id DESC
                """
            ).fetchall()

    return [dict(fila) for fila in filas]
