"""Diagnóstico: compara una foto con la galería y muestra el coseno crudo y el centrado."""
import sys

import numpy as np

from src import config
from src.services.galeria_service import GaleriaService
from src.services.modelo_service import ModeloService

consulta = sys.argv[1]
modelo = ModeloService().cargar_desde_archivo(config.RUTA_MODELO)
rutas = GaleriaService().listar()
vectores = np.array([modelo.calcular_vector(modelo.leer_imagen(r)) for r in rutas])
vq = modelo.calcular_vector(modelo.leer_imagen(consulta))
media = vectores.mean(axis=0)


def coseno(a, matriz):
    return matriz @ a / (np.linalg.norm(matriz, axis=1) * np.linalg.norm(a) + 1e-12)


crudo = coseno(vq, vectores)
centrado = coseno(vq - media, vectores - media)
print(f"{'foto':40} {'crudo':>8} {'centrado':>9}")
for i in np.argsort(-centrado):
    print(f"{rutas[i].name:40} {crudo[i]:8.4f} {centrado[i]:9.4f}")
print("rango crudo:", crudo.min().round(4), crudo.max().round(4))
print("rango centrado:", centrado.min().round(4), centrado.max().round(4))