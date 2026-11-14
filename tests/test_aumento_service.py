import unittest

import numpy as np

from src.services.aumento_service import AumentoService


class TestAumentoService(unittest.TestCase):
    def setUp(self):
        self.servicio = AumentoService(semilla=1)
        self.imagen = np.full((64, 64, 3), 0.5, dtype="float32")

    def test_mantiene_forma_y_rango(self):
        for _ in range(50):
            resultado = self.servicio.aplicar(self.imagen)
            self.assertEqual(resultado.shape, (64, 64, 3))
            self.assertGreaterEqual(float(resultado.min()), 0.0)
            self.assertLessEqual(float(resultado.max()), 1.0)

    def test_no_modifica_la_imagen_original(self):
        copia = self.imagen.copy()
        for _ in range(20):
            self.servicio.aplicar(self.imagen)
        np.testing.assert_array_equal(self.imagen, copia)

    def test_ocluir_tapa_una_zona(self):
        resultado = self.servicio.ocluir(self.imagen)
        self.assertTrue((resultado != self.imagen).any())


if __name__ == "__main__":
    unittest.main()