"""Entidad ResultadoBusqueda: lo que devuelve una búsqueda completa."""
from dataclasses import dataclass, field
from typing import List

from src.domain.coincidencia import Coincidencia


@dataclass
class ResultadoBusqueda:
    coincidencias: List[Coincidencia] = field(default_factory=list)
    analizadas: int = 0
    hay_coincidencia: bool = False
    mejor_similitud: float = 0.0
    mensaje: str = ""
