import unittest
from pathlib import Path

from src.domain.coincidencia import Coincidencia
from src.domain.perro_encontrado import PerroEncontrado
from src.domain.resultado_busqueda import ResultadoBusqueda
from src.domain.resultado_comparacion import ResultadoComparacion
from src.views.resultados_view import ResultadosView


class TestResultadosView(unittest.TestCase):
    def setUp(self):
        self.vista = ResultadosView()

    def test_resumen_con_coincidencia(self):
        r = ResultadoBusqueda([Coincidencia(Path("perro_01.jpg"), 0.9)], 3, True, 0.9)
        html = self.vista.resumen(r)
        self.assertIn("Principal coincidencia", html)
        self.assertIn("Perro 01", html)
        self.assertIn("90.00%", html)

    def test_resumen_sin_coincidencia(self):
        html = self.vista.resumen(ResultadoBusqueda(analizadas=4, mejor_similitud=0.1))
        self.assertIn("No se encontró", html)

    def test_tarjeta_escapa_html_de_los_datos(self):
        datos = PerroEncontrado("a.jpg", "<b>Plaza</b>", "1/1", "x")
        html = self.vista.tarjetas([Coincidencia(Path("a_b.jpg"), 0.9, datos)], 0.5)
        self.assertNotIn("<b>Plaza</b>", html)
        self.assertIn("&lt;b&gt;Plaza", html)

    def test_comparacion(self):
        self.assertIn("MISMO PERRO", self.vista.comparacion(ResultadoComparacion(True, 0.9)))

    def test_sin_coincidencias_muestra_estado_vacio(self):
        self.assertIn("Todavía no hay resultados", self.vista.tarjetas([], 0.5))


if __name__ == "__main__":
    unittest.main()