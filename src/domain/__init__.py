"""Capa de dominio: las entidades del proyecto, una clase por archivo."""
from src.domain.coincidencia import Coincidencia
from src.domain.configuracion_entrenamiento import ConfiguracionEntrenamiento
from src.domain.errores import ErrorRegistro, ValidacionError
from src.domain.metricas_evaluacion import MetricasEvaluacion
from src.domain.perro_dataset import PerroDataset
from src.domain.perro_encontrado import PerroEncontrado
from src.domain.resultado_busqueda import ResultadoBusqueda
from src.domain.resultado_comparacion import ResultadoComparacion
from src.domain.resultado_experimento import ResultadoExperimento
from src.domain.resultado_ranking import ResultadoRanking

__all__ = [
    "Coincidencia", "ConfiguracionEntrenamiento", "ErrorRegistro", "ValidacionError",
    "MetricasEvaluacion", "PerroDataset", "PerroEncontrado", "ResultadoBusqueda",
    "ResultadoComparacion", "ResultadoExperimento", "ResultadoRanking",
]
