"""Configuración central del proyecto: rutas y parámetros."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RUTA_MODELO = BASE_DIR / "model" / "modelo_perros_bolivar_scratch.keras"
RUTA_CANDIDATOS = BASE_DIR / "data" / "candidates"
RUTA_ENCONTRADOS = BASE_DIR / "data" / "found"
RUTA_BASE_DATOS = BASE_DIR / "data" / "perros.db"

EXTENSIONES_VALIDAS = {".jpg", ".jpeg", ".png", ".webp"}

TAMANO_IMAGEN = 128
CAPA_EXTRACTOR = "extractor_128"

# Umbral elegido con datos de validación (mejor F1) para la red siamesa.
UMBRAL_COINCIDENCIA = 0.25
CENTRO_COSENO = 0.999876
ESCALA_COSENO = 0.0001

CANTIDAD_RESULTADOS = 5