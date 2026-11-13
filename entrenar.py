"""Punto de entrada del entrenamiento (reemplaza al notebook).

Uso:
    python entrenar.py --descargar          # baja el dataset y entrena
    python entrenar.py --epocas 1           # prueba rápida
"""
import argparse

from src.aplicacion_entrenamiento import AplicacionEntrenamiento

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Entrena la red siamesa desde cero.")
    parser.add_argument("--descargar", action="store_true", help="descargar el dataset YT-BB-Dog")
    parser.add_argument("--epocas", type=int, default=None, help="cantidad máxima de épocas")
    args = parser.parse_args()
    AplicacionEntrenamiento().ejecutar(descargar=args.descargar, epocas=args.epocas)