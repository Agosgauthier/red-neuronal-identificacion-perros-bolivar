"""LotesService: arma lotes de pares, mezclados en cada pasada y con aumento de datos opcional.

Solo usa numpy: el service de la red lo conecta con TensorFlow.
"""
import math

import numpy as np

from src.services.aumento_service import AumentoService


class LotesService:
    def __init__(self, aumento: AumentoService = None, semilla: int = 42):
        self.aumento = aumento
        self.azar = np.random.default_rng(semilla)

    @staticmethod
    def cantidad_de_lotes(total: int, tamano_lote: int) -> int:
        return math.ceil(total / tamano_lote)

    def _aumentar(self, lote):
        if self.aumento is None:
            return lote
        return np.array([self.aumento.aplicar(imagen) for imagen in lote])

    def generar(self, x1, x2, y, tamano_lote: int):
        """Genera lotes para siempre: en cada pasada por los datos el orden cambia."""
        total = len(y)
        while True:
            orden = self.azar.permutation(total)
            for inicio in range(0, total, tamano_lote):
                indices = orden[inicio:inicio + tamano_lote]
                yield ({"imagen_1": self._aumentar(x1[indices]),
                        "imagen_2": self._aumentar(x2[indices])},
                       y[indices])