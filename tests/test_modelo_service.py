import unittest

import numpy as np

from src.services.modelo_service import ModeloService


def extractor_falso(x):
    """Vector = promedio de color RGB (3 valores), solo para probar."""
    return x.mean(axis=(1, 2))


class TestModeloService(unittest.TestCase):
    def setUp(self):
        self.servicio = ModeloService(
            extractor=extractor_falso,
            predictor=lambda a, b: np.array([[0.8]]),
        )

    def test_preparar_imagen_forma_y_rango(self):
        img = np.full((256, 200, 3), 255, dtype=np.uint8)
        r = self.servicio.preparar_imagen(img)
        self.assertEqual(r.shape, (1, 128, 128, 3))
        self.assertAlmostEqual(float(r.max()), 1.0)

    def test_preparar_imagen_gris_y_rgba(self):
        gris = np.zeros((50, 50), dtype=np.uint8)
        rgba = np.zeros((50, 50, 4), dtype=np.uint8)
        self.assertEqual(self.servicio.preparar_imagen(gris).shape, (1, 128, 128, 3))
        self.assertEqual(self.servicio.preparar_imagen(rgba).shape, (1, 128, 128, 3))

    def test_similitud_coseno(self):
        a = np.array([1.0, 0.0])
        self.assertAlmostEqual(ModeloService.similitud_coseno(a, a), 1.0)
        self.assertAlmostEqual(ModeloService.similitud_coseno(a, np.array([0.0, 1.0])), 0.0)
        self.assertEqual(ModeloService.similitud_coseno(a, np.zeros(2)), 0.0)

    def test_probabilidad_mismo(self):
        img = np.zeros((20, 20, 3), dtype=np.uint8)
        self.assertAlmostEqual(self.servicio.probabilidad_mismo(img, img), 0.8)

    def test_sin_modelo_cargado(self):
        img = np.zeros((10, 10, 3), dtype=np.uint8)
        with self.assertRaises(RuntimeError):
            ModeloService().probabilidad_mismo(img, img)


if __name__ == "__main__":
    unittest.main()