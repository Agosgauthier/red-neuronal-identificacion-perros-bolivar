import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from src.controllers.buscador_controller import BuscadorController
from src.services.buscador_service import BuscadorService
from src.services.modelo_service import ModeloService
from src.services.perros_repository import PerrosRepository


def predictor_falso(a, b):
    return 1 - np.abs(a.mean(axis=(1, 2)) - b.mean(axis=(1, 2))).mean()


class TestController(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        (base / "c").mkdir()
        Image.fromarray(
            np.full((30, 30, 3), (200, 30, 30), dtype=np.uint8)
        ).save(base / "c" / "perro_01.jpg")
        servicio = BuscadorService(
            ModeloService(predictor=predictor_falso),
            PerrosRepository(base / "t.db"),
            base / "c", base / "f", umbral=0.9)
        self.ctrl = BuscadorController(servicio)

    def tearDown(self):
        self.tmp.cleanup()

    def test_buscar_sin_imagen(self):
        resumen, tarjetas = self.ctrl.buscar(None)
        self.assertIn("Primero cargá", resumen)

    def test_buscar_con_resultado(self):
        resumen, tarjetas = self.ctrl.buscar(
            np.full((40, 40, 3), (210, 20, 20), dtype=np.uint8))
        self.assertIn("Principal coincidencia", resumen)
        self.assertIn("Perro 01", tarjetas)

    def test_comparar_sin_imagenes(self):
        self.assertEqual(self.ctrl.comparar(None, None), "⚠️ Cargá las dos imágenes.")

    def test_registrar_incompleto(self):
        msg = self.ctrl.registrar(
            np.zeros((10, 10, 3), dtype=np.uint8), "", "x", "", "y")
        self.assertIn("dónde", msg)


if __name__ == "__main__":
    unittest.main()