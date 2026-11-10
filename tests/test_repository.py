import tempfile
import unittest
from pathlib import Path

from src.models.perro import PerroEncontrado
from src.services.perros_repository import PerrosRepository


class TestPerrosRepository(unittest.TestCase):
    def test_registrar_y_buscar(self):
        with tempfile.TemporaryDirectory() as d:
            repo = PerrosRepository(Path(d) / "t.db")
            nuevo_id = repo.registrar(PerroEncontrado(
                imagen="a.jpg", zona="Plaza", fecha="8/10/2026",
                contacto="WhatsApp", fecha_registro="2026-10-08T14:00:00"))
            self.assertEqual(nuevo_id, 1)
            self.assertEqual(repo.obtener_por_imagen("a.jpg").zona, "Plaza")
            self.assertIsNone(repo.obtener_por_imagen("x.jpg"))
            self.assertEqual(len(repo.listar()), 1)


if __name__ == "__main__":
    unittest.main()