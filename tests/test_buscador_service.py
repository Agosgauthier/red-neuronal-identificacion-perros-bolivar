import tempfile
import unittest
from pathlib import Path

import numpy as np

from src.repositories.perros_repository import PerrosRepository
from src.services.buscador_service import BuscadorService
from src.services.galeria_service import GaleriaService
from src.services.modelo_service import ModeloService
from src.services.registro_service import RegistroService
from tests.helpers import guardar_color, predictor_falso


class TestBuscadorService(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.cand, self.enc = base / "cand", base / "found"
        self.cand.mkdir()
        guardar_color(self.cand / "rojo.jpg", (250, 10, 10))
        guardar_color(self.cand / "azul.jpg", (10, 10, 250))
        self.modelo = ModeloService(predictor=predictor_falso)
        self.repo = PerrosRepository(base / "t.db")
        self.galeria = GaleriaService(self.cand, self.enc)
        self.servicio = BuscadorService(self.modelo, self.galeria, self.repo,
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
        servicio = BuscadorService(self.modelo, self.galeria, self.repo, umbral=0.9999)
        r = servicio.buscar(np.full((60, 60, 3), (200, 90, 40), dtype=np.uint8))
        self.assertFalse(r.hay_coincidencia)
        self.assertEqual(r.coincidencias, [])

    def test_sin_candidatos(self):
        vacia = GaleriaService(self.cand / "no_existe", self.enc)
        servicio = BuscadorService(self.modelo, vacia, self.repo)
        r = servicio.buscar(np.zeros((10, 10, 3), dtype=np.uint8))
        self.assertFalse(r.hay_coincidencia)
        self.assertTrue(r.mensaje)

    def test_comparar(self):
        rojo = np.full((30, 30, 3), (250, 10, 10), dtype=np.uint8)
        azul = np.full((30, 30, 3), (10, 10, 250), dtype=np.uint8)
        self.assertTrue(self.servicio.comparar(rojo, rojo).mismo_perro)
        self.assertFalse(self.servicio.comparar(rojo, azul).mismo_perro)

    def test_perro_registrado_aparece_en_la_busqueda_con_sus_datos(self):
        foto = np.full((50, 50, 3), (10, 240, 10), dtype=np.uint8)
        perro = RegistroService(self.repo, self.enc).registrar(
            foto, "Plaza", "8/10/2026", "", "WhatsApp")
        r = self.servicio.buscar(foto)
        self.assertEqual(r.coincidencias[0].ruta.name, perro.imagen)
        self.assertEqual(r.coincidencias[0].datos.zona, "Plaza")


if __name__ == "__main__":
    unittest.main()