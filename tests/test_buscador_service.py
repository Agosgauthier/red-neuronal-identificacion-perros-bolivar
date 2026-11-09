import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from src.services.buscador_service import BuscadorService, ValidacionError
from src.services.modelo_service import ModeloService
from src.services.perros_repository import PerrosRepository


def predictor_falso(a, b):
    """Probabilidad = qué parecido es el color promedio de las dos imágenes."""
    return 1 - np.abs(a.mean(axis=(1, 2)) - b.mean(axis=(1, 2))).mean()


def guardar_color(ruta, rgb):
    Image.fromarray(np.full((40, 40, 3), rgb, dtype=np.uint8)).save(ruta)


class TestBuscadorService(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.cand, self.enc = base / "cand", base / "found"
        self.cand.mkdir()
        guardar_color(self.cand / "rojo.jpg", (250, 10, 10))
        guardar_color(self.cand / "azul.jpg", (10, 10, 250))
        self.servicio = BuscadorService(
            ModeloService(predictor=predictor_falso),
            PerrosRepository(base / "t.db"),
            ruta_candidatos=self.cand, ruta_encontrados=self.enc,
            umbral=0.90, cantidad=5)

    def tearDown(self):
        self.tmp.cleanup()

    def test_encuentra_el_parecido_primero(self):
        consulta = np.full((60, 60, 3), (240, 20, 20), dtype=np.uint8)
        r = self.servicio.buscar(consulta)
        self.assertTrue(r.hay_coincidencia)
        self.assertEqual(r.coincidencias[0].ruta.name, "rojo.jpg")
        self.assertEqual(r.analizadas, 2)

    def test_sin_coincidencia_alta(self):
        servicio = BuscadorService(
            self.servicio.modelo, self.servicio.repositorio,
            self.cand, self.enc, umbral=0.9999)
        consulta = np.full((60, 60, 3), (200, 90, 40), dtype=np.uint8)
        r = servicio.buscar(consulta)
        self.assertFalse(r.hay_coincidencia)
        self.assertEqual(r.coincidencias, [])

    def test_sin_candidatos(self):
        vacio = BuscadorService(self.servicio.modelo, self.servicio.repositorio,
                                self.cand / "no_existe", self.enc)
        r = vacio.buscar(np.zeros((10, 10, 3), dtype=np.uint8))
        self.assertFalse(r.hay_coincidencia)
        self.assertTrue(r.mensaje)

    def test_registrar_y_aparece_en_la_busqueda(self):
        foto = np.full((50, 50, 3), (10, 240, 10), dtype=np.uint8)
        perro = self.servicio.registrar_encontrado(foto, "Plaza", "8/10/2026", "", "WhatsApp")
        self.assertIsNotNone(perro.id)
        r = self.servicio.buscar(foto)
        self.assertEqual(r.coincidencias[0].ruta.name, perro.imagen)
        self.assertEqual(r.coincidencias[0].datos.zona, "Plaza")

    def test_registrar_valida_campos(self):
        foto = np.zeros((20, 20, 3), dtype=np.uint8)
        with self.assertRaises(ValidacionError):
            self.servicio.registrar_encontrado(None, "x", "y", "", "z")
        with self.assertRaises(ValidacionError):
            self.servicio.registrar_encontrado(foto, " ", "y", "", "z")
        with self.assertRaises(ValidacionError):
            self.servicio.registrar_encontrado(foto, "x", "y", "", "")


if __name__ == "__main__":
    unittest.main()