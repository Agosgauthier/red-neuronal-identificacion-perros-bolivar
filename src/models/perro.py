"""Modelos de datos (la M de MVC)."""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class PerroEncontrado:
    imagen: str
    zona: str
    fecha: str
    contacto: str
    descripcion: str = ""
    fecha_registro: str = ""
    id: Optional[int] = None


@dataclass
class Coincidencia:
    ruta: Path
    similitud: float
    datos: Optional[PerroEncontrado] = None

    @property
    def porcentaje(self) -> float:
        return self.similitud * 100


@dataclass
class ResultadoBusqueda:
    coincidencias: list
    analizadas: int
    hay_coincidencia: bool
    mejor_similitud: float = 0.0
    mensaje: str = ""