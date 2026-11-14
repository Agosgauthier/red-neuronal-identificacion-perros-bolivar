"""Entidad MetricasEvaluacion: métricas de un clasificador con un umbral dado."""
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class MetricasEvaluacion:
    umbral: float
    accuracy: float
    precision: float
    recall: float
    f1: float
    matriz_confusion: List[List[int]]
