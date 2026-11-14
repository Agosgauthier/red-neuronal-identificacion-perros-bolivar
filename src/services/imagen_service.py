"""ImagenService: lee imágenes y las deja listas para la red (128x128, RGB, 0-1)."""
from pathlib import Path
from typing import Iterable

import numpy as np

from src import config


class ImagenService:
    def __init__(self, tamano: int = config.TAMANO_IMAGEN):
        self.tamano = tamano

    def cargar_normalizada(self, ruta) -> np.ndarray:
        """Lee una foto del disco -> (T, T, 3) float32 con valores entre 0 y 1."""
        import cv2  # se importa acá para que los tests no lo necesiten

        imagen = cv2.imread(str(Path(ruta)))
        if imagen is None:
            raise ValueError(f"No se pudo cargar: {ruta}")
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        imagen = cv2.resize(imagen, (self.tamano, self.tamano))
        return imagen.astype("float32") / 255.0

    def cargar_lote(self, rutas: Iterable) -> np.ndarray:
        return np.array([self.cargar_normalizada(r) for r in rutas])