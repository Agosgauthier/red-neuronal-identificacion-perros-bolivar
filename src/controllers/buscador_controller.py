"""Controlador (la C de MVC): conecta la vista con los services."""
from src.services.buscador_service import BuscadorService, ValidacionError
from src.views import renderizado


class BuscadorController:
    def __init__(self, servicio: BuscadorService):
        self.servicio = servicio

    def buscar(self, imagen_perdido):
        """Devuelve (html_resumen, html_tarjetas)."""
        if imagen_perdido is None:
            return renderizado.aviso("Primero cargá una fotografía del perro perdido."), renderizado.estado_vacio()
        resultado = self.servicio.buscar(imagen_perdido)
        return renderizado.resumen(resultado), renderizado.tarjetas(resultado.coincidencias)

    def comparar(self, imagen1, imagen2) -> str:
        if imagen1 is None or imagen2 is None:
            return "⚠️ Cargá las dos imágenes."
        mismo, sim = self.servicio.comparar(imagen1, imagen2)
        titulo = "🐕✅ MISMO PERRO" if mismo else "🐕❌ PERROS DIFERENTES"
        return f"{titulo}\n\nSimilitud: {sim * 100:.2f}%"

    def registrar(self, imagen, zona, fecha, descripcion, contacto) -> str:
        try:
            self.servicio.registrar_encontrado(imagen, zona, fecha, descripcion, contacto)
        except ValidacionError as error:
            return f"⚠️ {error}"
        except Exception as error:
            print(f"Error al registrar el perro: {error}")
            return "❌ No se pudieron guardar los datos del perro. Intentá nuevamente."
        return ("✅ Perro registrado correctamente.\n\n"
                "La fotografía ya forma parte de la base de búsqueda.")