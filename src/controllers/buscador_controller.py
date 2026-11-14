"""BuscadorController: recibe lo que pide la vista y lo delega en el service. No genera HTML."""
from src.domain.errores import ValidacionError
from src.domain.resultado_busqueda import ResultadoBusqueda
from src.domain.resultado_comparacion import ResultadoComparacion
from src.services.buscador_service import BuscadorService
from src.services.galeria_service import GaleriaService


class BuscadorController:
    def __init__(self, buscador: BuscadorService, galeria: GaleriaService):
        self.buscador = buscador
        self.galeria = galeria

    @property
    def umbral(self) -> float:
        return self.buscador.umbral

    def buscar(self, imagen_perdido) -> ResultadoBusqueda:
        if imagen_perdido is None:
            raise ValidacionError("Primero cargá una fotografía del perro perdido.")
        return self.buscador.buscar(imagen_perdido)

    def comparar(self, imagen1, imagen2) -> ResultadoComparacion:
        if imagen1 is None or imagen2 is None:
            raise ValidacionError("Cargá las dos imágenes.")
        return self.buscador.comparar(imagen1, imagen2)

    def foto_decorativa(self):
        """Primera foto de la galería (para la portada) o None si no hay."""
        rutas = self.galeria.listar()
        return rutas[0] if rutas else None