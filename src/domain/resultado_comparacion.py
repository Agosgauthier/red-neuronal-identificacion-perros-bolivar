"""Entidad ResultadoComparacion: resultado de comparar dos fotos."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ResultadoComparacion:
    mismo_perro: bool
    similitud: float

    @property
    def porcentaje(self) -> float:
        return self.similitud * 100
