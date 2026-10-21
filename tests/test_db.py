import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src import db


class TestDb(unittest.TestCase):

    def test_registrar_y_buscar(self):
        with tempfile.TemporaryDirectory() as carpeta:
            with patch.object(db, "RUTA_BASE_DATOS", Path(carpeta) / "test.db"):
                db.inicializar_base_datos()
                db.registrar_perro(
                    "a.jpg", "Plaza", "8/10/2026", "", "WhatsApp", "2026-10-08T14:00:00"
                )
                self.assertEqual(db.obtener_perro_por_imagen("a.jpg")["zona"], "Plaza")
                self.assertIsNone(db.obtener_perro_por_imagen("x.jpg"))


if __name__ == "__main__":
    unittest.main()