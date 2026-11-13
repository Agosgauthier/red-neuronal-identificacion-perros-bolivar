"""PerrosRepository: acceso a SQLite (tabla perros_encontrados)."""
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Optional

from src import config
from src.domain.perro_encontrado import PerroEncontrado

_CAMPOS = "id, imagen, zona, fecha, descripcion, contacto, fecha_registro"


class PerrosRepository:
    def __init__(self, ruta_db: Path = config.RUTA_BASE_DATOS):
        self.ruta_db = Path(ruta_db)
        self.inicializar()

    def _conexion(self):
        self.ruta_db.parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(self.ruta_db)
        con.row_factory = sqlite3.Row
        return con

    def inicializar(self):
        with closing(self._conexion()) as con, con:
            con.execute(
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

    def registrar(self, perro: PerroEncontrado) -> int:
        with closing(self._conexion()) as con, con:
            cur = con.execute(
                "INSERT INTO perros_encontrados "
                "(imagen, zona, fecha, descripcion, contacto, fecha_registro) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (perro.imagen, perro.zona, perro.fecha, perro.descripcion,
                 perro.contacto, perro.fecha_registro),
            )
            return cur.lastrowid

    @staticmethod
    def _a_objeto(fila) -> PerroEncontrado:
        return PerroEncontrado(**dict(fila))

    def obtener_por_imagen(self, nombre_imagen: str) -> Optional[PerroEncontrado]:
        with closing(self._conexion()) as con:
            fila = con.execute(
                f"SELECT {_CAMPOS} FROM perros_encontrados "
                "WHERE imagen = ? ORDER BY id DESC LIMIT 1",
                (nombre_imagen,),
            ).fetchone()
        return self._a_objeto(fila) if fila else None

    def listar(self) -> list:
        with closing(self._conexion()) as con:
            filas = con.execute(
                f"SELECT {_CAMPOS} FROM perros_encontrados ORDER BY id DESC"
            ).fetchall()
        return [self._a_objeto(f) for f in filas]