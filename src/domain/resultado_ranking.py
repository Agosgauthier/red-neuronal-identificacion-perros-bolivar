"""Entidad ResultadoRanking: qué tan seguido el perro correcto queda en los primeros lugares."""
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ResultadoRanking:
    aciertos: Dict[int, int]   # {1: 60, 3: 80, 5: 83}
    total: int
