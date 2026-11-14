"""Entidad PerroEncontrado: un perro que alguien registró en la calle."""
from dataclasses import dataclass
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
