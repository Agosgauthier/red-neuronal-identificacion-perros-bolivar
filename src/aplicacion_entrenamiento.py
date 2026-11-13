"""AplicacionEntrenamiento: arma las piezas y ejecuta el entrenamiento (reemplaza al notebook)."""
from dataclasses import replace
from typing import Optional

from src import config
from src.controllers.entrenamiento_controller import EntrenamientoController
from src.domain.configuracion_entrenamiento import ConfiguracionEntrenamiento
from src.services.dataset_service import DatasetService
from src.services.descarga_dataset_service import DescargaDatasetService
from src.services.evaluacion_service import EvaluacionService
from src.services.imagen_service import ImagenService
from src.services.red_siamesa_service import RedSiamesaService
from src.views.consola_view import ConsolaView


class AplicacionEntrenamiento:
    def __init__(self, configuracion: Optional[ConfiguracionEntrenamiento] = None):
        self.configuracion = configuracion or ConfiguracionEntrenamiento()

    def construir(self) -> EntrenamientoController:
        c = self.configuracion
        imagenes = ImagenService(c.tamano)
        return EntrenamientoController(
            config=c,
            descarga=DescargaDatasetService(),
            dataset=DatasetService(config.RUTA_DATASET, imagenes, c.semilla),
            red=RedSiamesaService(c),
            evaluacion=EvaluacionService(),
            vista=ConsolaView(),
        )

    def ejecutar(self, descargar: bool = False, epocas: Optional[int] = None):
        if epocas is not None:
            self.configuracion = replace(self.configuracion, epocas=epocas)
        return self.construir().ejecutar(descargar=descargar)