"""AplicacionWeb: arma las piezas (inyección de dependencias) y lanza la app Gradio."""
from src import config
from src.controllers.buscador_controller import BuscadorController
from src.controllers.registro_controller import RegistroController
from src.repositories.perros_repository import PerrosRepository
from src.services.buscador_service import BuscadorService
from src.services.galeria_service import GaleriaService
from src.services.modelo_service import ModeloService
from src.services.registro_service import RegistroService
from src.views.interfaz_view import InterfazView
from src.views.resultados_view import ResultadosView


class AplicacionWeb:
    def __init__(self, ruta_modelo=config.RUTA_MODELO):
        self.ruta_modelo = ruta_modelo

    def construir(self):
        modelo = ModeloService().cargar_desde_archivo(self.ruta_modelo)
        repositorio = PerrosRepository()
        galeria = GaleriaService()

        buscador = BuscadorController(BuscadorService(modelo, galeria, repositorio), galeria)
        registro = RegistroController(RegistroService(repositorio))
        return InterfazView(buscador, registro, ResultadosView()).construir()

    def ejecutar(self) -> None:
        self.construir().launch()