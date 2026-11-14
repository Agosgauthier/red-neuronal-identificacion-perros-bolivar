"""Entidad ConfiguracionEntrenamiento: todos los parámetros de un entrenamiento."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ConfiguracionEntrenamiento:
    tamano: int = 128
    perros_train: int = 600
    perros_val: int = 100
    perros_test: int = 100
    pares_por_perro: int = 10
    learning_rate: float = 0.001
    epocas: int = 60
    batch_size: int = 32
    paciencia_early_stopping: int = 5
    paciencia_reduce_lr: int = 3
    factor_reduce_lr: float = 0.5
    lr_minimo: float = 1e-6
    semilla: int = 42
    perros_ranking: int = 100
    semilla_ranking: int = 7
