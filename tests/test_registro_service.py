import tempfile
import unittest
from pathlib import Path

import numpy as np

from src.domain.errores import ValidacionError
from src.repositories.perros_repository import PerrosRepository
from src.services.registro_service import RegistroService


class TestRegistroService(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.repo = PerrosRepository(base / "t.db")
        self.servicio = RegistroService(self.repo, base / "found")
        self.foto = np.zeros((20, 20, 3), dtype=np.uint8)

    def tearDown(self):
        self.tmp.cleanup()

    def test_registrar_guarda_foto_y_fila(self):
        perro = self.servicio.registrar(self.foto, " Plaza ", "8/10", "", "WhatsApp")
        self.assertIsNotNone(perro.id)
        self.assertEqual(perro.zona, "Plaza")
        self.assertTrue((self.servicio.ruta_encontrados / perro.imagen).exists())
        self.assertEqual(len(self.repo.listar()), 1)

    def test_valida_campos(self):
        with self.assertRaises(ValidacionError):
            self.servicio.registrar(None, "x", "y", "", "z")
        with self.assertRaises(ValidacionError):
            self.servicio.registrar(self.foto, " ", "y", "", "z")
        with self.assertRaises(ValidacionError):
            self.servicio.registrar(self.foto, "x", "", "", "z")
        with self.assertRaises(ValidacionError):
            self.servicio.registrar(self.foto, "x", "y", "", "")

    def test_si_falla_la_base_no_queda_la_foto(self):
        class RepoRoto:
            def registrar(self, perro):
                raise RuntimeError("base caída")

        servicio = RegistroService(RepoRoto(), self.servicio.ruta_encontrados)
        with self.assertRaises(RuntimeError):
            servicio.registrar(self.foto, "x", "y", "", "z")
        self.assertEqual(list(self.servicio.ruta_encontrados.glob("*.jpg")), [])


if __name__ == "__main__":
    unittest.main()