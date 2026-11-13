import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

from src.controllers.entrenamiento_controller import EntrenamientoController
from src.domain.configuracion_entrenamiento import ConfiguracionEntrenamiento
from src.services.dataset_service import DatasetService
from src.services.evaluacion_service import EvaluacionService
from tests.test_dataset_y_evaluacion import crear_dataset_falso


class ImagenesFalsas:
    def cargar_lote(self, rutas):
        return np.zeros((len(list(rutas)), 4, 4, 3), dtype="float32")


class RedFalsa:
    """Sin TensorFlow: devuelve puntajes fijos y anota qué pasos se ejecutaron."""

    def __init__(self):
        self.pasos = []

    def construir(self):
        self.pasos.append("construir")

    def entrenar(self, *datos):
        self.pasos.append("entrenar")

    def predecir(self, x1, x2):
        return np.linspace(0, 1, len(x1))

    def extraer_vectores(self, x):
        return np.ones((len(x), 3))

    def guardar(self, ruta):
        self.pasos.append("guardar")
        return 1.5


class VistaFalsa:
    def __init__(self):
        self.mostro_resultado = False

    def paso(self, titulo): pass
    def mostrar_tamanos(self, tamanos): pass
    def mostrar_configuracion(self, config): pass

    def mostrar_resultado(self, resultado):
        self.mostro_resultado = True


class TestEntrenamientoController(unittest.TestCase):
    def test_ejecuta_los_pasos_en_orden(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            crear_dataset_falso(base, perros_train=12, perros_test=6)
            config = ConfiguracionEntrenamiento(
                perros_train=8, perros_val=4, perros_test=4,
                pares_por_perro=2, perros_ranking=4)
            dataset = DatasetService(base, ImagenesFalsas())
            red, vista = RedFalsa(), VistaFalsa()
            controlador = EntrenamientoController(
                config, None, dataset, red, EvaluacionService(), vista)

            with mock.patch("src.controllers.entrenamiento_controller.rutas.RUTA_PARES",
                            base / "pares"):
                resultado = controlador.ejecutar()

            self.assertEqual(red.pasos, ["construir", "entrenar", "guardar"])
            self.assertTrue(vista.mostro_resultado)
            self.assertEqual(resultado.ranking.total, 4)
            self.assertEqual(resultado.tamano_mb, 1.5)
            self.assertTrue((base / "pares" / "pares_train.csv").exists())


if __name__ == "__main__":
    unittest.main()