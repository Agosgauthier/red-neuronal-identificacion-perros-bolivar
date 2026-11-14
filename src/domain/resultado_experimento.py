"""Entidad ResultadoExperimento: todo lo que mide una corrida de entrenamiento."""
from dataclasses import dataclass
from pathlib import Path

from src.domain.metricas_evaluacion import MetricasEvaluacion
from src.domain.resultado_ranking import ResultadoRanking


@dataclass(frozen=True)
class ResultadoExperimento:
    umbral_red: float                     # elegido con VALIDACIÓN (salida de la red)
    f1_validacion_red: float
    test_umbral_05: MetricasEvaluacion    # test con umbral 0,5
    test_umbral_red: MetricasEvaluacion   # test con el umbral elegido en validación
    umbral_coseno: float                  # elegido con VALIDACIÓN (similitud coseno)
    f1_validacion_coseno: float
    test_coseno: MetricasEvaluacion
    ranking: ResultadoRanking
    ruta_modelo: Path
    tamano_mb: float
