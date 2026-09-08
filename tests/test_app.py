import unittest

import numpy as np

from src.app import comparar_perros, preparar_imagen


class TestApp(unittest.TestCase):

    def test_preparar_imagen(self):
        imagen = np.zeros((256, 256, 3), dtype=np.uint8)

        resultado = preparar_imagen(imagen)

        self.assertEqual(resultado.shape, (1, 128, 128, 3))

    def test_comparar_sin_imagenes(self):
        resultado = comparar_perros(None, None)

        self.assertEqual(
            resultado,
            "⚠️ Cargá las dos imágenes."
        )


if __name__ == "__main__":
    unittest.main()