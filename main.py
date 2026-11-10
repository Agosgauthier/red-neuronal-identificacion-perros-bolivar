"""Punto de entrada: solo arma las piezas y lanza la aplicación."""
from src import config
from src.controllers.buscador_controller import BuscadorController
from src.services.buscador_service import BuscadorService
from src.services.modelo_service import ModeloService
from src.services.perros_repository import PerrosRepository
from src.views.interfaz import InterfazView
from src.views.renderizado import imagen_a_data_uri


def main():
    modelo = ModeloService().cargar_desde_archivo(config.RUTA_MODELO)
    servicio = BuscadorService(modelo, PerrosRepository())
    controlador = BuscadorController(servicio)

    candidatos = servicio.listar_candidatos()
    decorativa = imagen_a_data_uri(candidatos[0]) if candidatos else ""

    InterfazView(controlador, decorativa).construir().launch()


if __name__ == "__main__":
    main()