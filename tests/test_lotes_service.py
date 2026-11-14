import unittest

import numpy as np

from src.services.aumento_service import AumentoService
from src.services.lotes_service import LotesService


class TestLotesService(unittest.TestCase):
    def setUp(self):
        self.x1 = np.random.rand(10, 16, 16, 3).astype("float32")
        self.x2 = np.random.rand(10, 16, 16, 3).astype("float32")
        self.y = np.arange(10, dtype="float32")

    def test_recorre_todos_los_pares_en_cada_pasada(self):
        lotes = LotesService(semilla=1).generar(self.x1, self.x2, self.y, 4)
        vistos = []
        for _ in range(LotesService.cantidad_de_lotes(10, 4)):
            _, etiquetas = next(lotes)
            vistos.extend(etiquetas.tolist())
        self.assertEqual(sorted(vistos), list(range(10)))

    def test_forma_de_los_lotes(self):
        entradas, etiquetas = next(
            LotesService(semilla=1).generar(self.x1, self.x2, self.y, 4))
        self.assertEqual(entradas["imagen_1"].shape, (4, 16, 16, 3))
        self.assertEqual(entradas["imagen_2"].shape, (4, 16, 16, 3))
        self.assertEqual(len(etiquetas), 4)

    def test_con_aumento_cambia_las_imagenes_pero_no_los_originales(self):
        copia = self.x1.copy()
        servicio = LotesService(AumentoService(prob_oclusion=1.0, semilla=2), semilla=1)
        entradas, _ = next(servicio.generar(self.x1, self.x2, self.y, 10))
        self.assertNotAlmostEqual(float(entradas["imagen_1"].sum()),
                                  float(self.x1.sum()), places=3)
        np.testing.assert_array_equal(self.x1, copia)

    def test_cantidad_de_lotes(self):
        self.assertEqual(LotesService.cantidad_de_lotes(10, 4), 3)


if __name__ == "__main__":
    unittest.main()