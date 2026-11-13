"""Entidad Coincidencia: una foto candidata y qué tan parecida es a la buscada."""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from src.domain.perro_encontrado import PerroEncontrado


@dataclass
class Coincidencia:
    ruta: Path
    similitud: float
    datos: Optional[PerroEncontrado] = None

    @property
    def porcentaje(self) -> float:
        return self.similitud * 100

    @property
    def nombre(self) -> str:
        return self.ruta.stem.replace("_", " ").title()
