import tempfile
import unittest
from pathlib import Path

import numpy as np

from src.controllers.buscador_controller import BuscadorController
from src.controllers.registro_controller import RegistroController
from src.domain.errores import ErrorRegistro, ValidacionError
from src.repositories.perros_repository import PerrosRepository
from src.services.buscador_service import BuscadorService
from src.services.galeria_service import GaleriaService
from src.services.modelo_service import ModeloService
from src.services.registro_service import RegistroService
from tests.helpers import guardar_color, predictor_falso


class TestControllers(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        (base / "c").mkdir()
        guardar_color(base / "c" / "perro_01.jpg", (200, 30, 30), 30)
        repo = PerrosRepository(base / "t.db")
        galeria = GaleriaService(base / "c", base / "f")
        buscador = BuscadorService(ModeloService(predictor=predictor_falso),
                                   galeria, repo, umbral=0.9)
        self.buscador = BuscadorController(buscador, galeria)
        self.registro = RegistroController(RegistroService(repo, base / "f"))

    def tearDown(self):
        self.tmp.cleanup()

    def test_buscar_sin_imagen(self):
        with self.assertRaises(ValidacionError):
            self.buscador.buscar(None)

    def test_buscar_con_resultado(self):
        r = self.buscador.buscar(np.full((40, 40, 3), (210, 20, 20), dtype=np.uint8))
        self.assertTrue(r.hay_coincidencia)
        self.assertEqual(r.coincidencias[0].nombre, "Perro 01")

    def test_comparar_sin_imagenes(self):
        with self.assertRaises(ValidacionError):
            self.buscador.comparar(None, None)

    def test_foto_decorativa(self):
        self.assertEqual(self.buscador.foto_decorativa().name, "perro_01.jpg")

    def test_registrar_incompleto(self):
        with self.assertRaises(ValidacionError):
            self.registro.registrar(np.zeros((10, 10, 3), dtype=np.uint8), "", "x", "", "y")

    def test_registrar_falla_tecnica_se_traduce(self):
        class ServicioRoto:
            def registrar(self, *args):
                raise OSError("disco lleno")

        with self.assertRaises(ErrorRegistro):
            RegistroController(ServicioRoto()).registrar(None, "a", "b", "c", "d")


if __name__ == "__main__":
    unittest.main()