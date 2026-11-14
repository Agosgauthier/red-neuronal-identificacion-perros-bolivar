"""Piezas falsas compartidas por los tests (no cargan TensorFlow)."""
import numpy as np
from PIL import Image


def predictor_falso(a, b):
    """Probabilidad = qué parecido es el color promedio de las dos imágenes."""
    return 1 - np.abs(a.mean(axis=(1, 2)) - b.mean(axis=(1, 2))).mean()


def guardar_color(ruta, rgb, tamano=40):
    Image.fromarray(np.full((tamano, tamano, 3), rgb, dtype=np.uint8)).save(ruta)