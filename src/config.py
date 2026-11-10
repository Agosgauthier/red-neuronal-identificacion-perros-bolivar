"""Configuración central del proyecto: rutas y parámetros."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RUTA_MODELO = BASE_DIR / "model" / "extractor_D_trillizos.keras"
RUTA_CANDIDATOS = BASE_DIR / "data" / "candidates"
RUTA_ENCONTRADOS = BASE_DIR / "data" / "found"
RUTA_BASE_DATOS = BASE_DIR / "data" / "perros.db"

EXTENSIONES_VALIDAS = {".jpg", ".jpeg", ".png", ".webp"}

TAMANO_IMAGEN = 128
CAPA_EXTRACTOR = "extractor_128"

# Modelo D (extractor + similitud coseno): el coseno se reescala con una sigmoide
# centrada en CENTRO_COSENO (el umbral elegido en validación). Por eso 0.5 equivale
# a un coseno de 0,999876.
UMBRAL_COINCIDENCIA = 0.5
CENTRO_COSENO = 0.999876
ESCALA_COSENO = 0.0001

CANTIDAD_RESULTADOS = 5