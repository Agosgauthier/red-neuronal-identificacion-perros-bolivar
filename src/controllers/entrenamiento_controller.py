"""EntrenamientoController: ejecuta los 5 pasos de la red, en orden.

1 dataset -> 2 elegir modelo -> 3 configurar -> 4 entrenar -> 5 probarlo.
Reemplaza al notebook: la lógica está en los services, acá solo se dirige el orden.
"""
from src import config as rutas
from src.domain.configuracion_entrenamiento import ConfiguracionEntrenamiento
from src.domain.resultado_experimento import ResultadoExperimento
from src.services.dataset_service import DatasetService
from src.services.descarga_dataset_service import DescargaDatasetService
from src.services.evaluacion_service import EvaluacionService
from src.services.red_siamesa_service import RedSiamesaService
from src.views.consola_view import ConsolaView


class EntrenamientoController:
    def __init__(self, config: ConfiguracionEntrenamiento, descarga: DescargaDatasetService,
                 dataset: DatasetService, red: RedSiamesaService,
                 evaluacion: EvaluacionService, vista: ConsolaView):
        self.config = config
        self.descarga = descarga
        self.dataset = dataset
        self.red = red
        self.evaluacion = evaluacion
        self.vista = vista
        self._datos = {}

    def ejecutar(self, descargar: bool = False) -> ResultadoExperimento:
        if descargar:
            self.descargar_dataset()
        self.preparar_dataset()          # paso 1
        self.construir_modelo()          # pasos 2 y 3
        self.entrenar()                  # paso 4
        resultado = self.probar()        # paso 5
        self.vista.mostrar_resultado(resultado)
        return resultado

    def descargar_dataset(self) -> None:
        self.vista.paso("Descargando el dataset YT-BB-Dog (si hace falta)")
        self.descarga.descargar()

    def preparar_dataset(self) -> None:
        self.vista.paso("1. Dataset: armando pares de entrenamiento, validación y prueba")
        conjuntos = self.dataset.dividir(self.config)
        self.dataset.guardar_pares(conjuntos, rutas.RUTA_PARES)
        self._datos = {nombre: self.dataset.cargar_arrays(df) for nombre, df in conjuntos.items()}
        self.vista.mostrar_tamanos({n: len(d[2]) for n, d in self._datos.items()})

    def construir_modelo(self) -> None:
        self.vista.paso("2 y 3. Modelo: red siamesa con CNN propia, configurada")
        self.red.construir()
        self.vista.mostrar_configuracion(self.config)

    def entrenar(self) -> None:
        self.vista.paso("4. Entrenamiento")
        self.red.entrenar(*self._datos["train"], *self._datos["val"])

    def probar(self) -> ResultadoExperimento:
        self.vista.paso("5. Prueba con perros que la red nunca vio")
        x1v, x2v, yv = self._datos["val"]
        x1t, x2t, yt = self._datos["test"]

        # Salida de la red: el umbral se elige con VALIDACIÓN, nunca con test.
        umbral, f1_val = self.evaluacion.elegir_umbral(yv, self.red.predecir(x1v, x2v))
        pred_test = self.red.predecir(x1t, x2t)

        # Alternativa: similitud coseno entre los vectores del extractor.
        sim_val = self.evaluacion.similitud_coseno(
            self.red.extraer_vectores(x1v), self.red.extraer_vectores(x2v))
        sim_test = self.evaluacion.similitud_coseno(
            self.red.extraer_vectores(x1t), self.red.extraer_vectores(x2t))
        umbral_cos, f1_cos = self.evaluacion.elegir_umbral(yv, sim_val, 0.30, 1.00, 0.01)

        # Buscador: ¿el perro correcto queda entre los primeros lugares?
        galeria, consultas = self.dataset.crear_consultas_ranking(
            "test", self.config.perros_ranking, self.config.semilla_ranking)
        imagenes = self.dataset.imagenes
        ranking = self.evaluacion.ranking(
            self.red.extraer_vectores(imagenes.cargar_lote(galeria)),
            self.red.extraer_vectores(imagenes.cargar_lote(consultas)))

        ruta = rutas.RUTA_MODELO_ENTRENADO
        tamano_mb = self.red.guardar(ruta)

        return ResultadoExperimento(
            umbral_red=umbral, f1_validacion_red=f1_val,
            test_umbral_05=self.evaluacion.evaluar(yt, pred_test, 0.5),
            test_umbral_red=self.evaluacion.evaluar(yt, pred_test, umbral),
            umbral_coseno=umbral_cos, f1_validacion_coseno=f1_cos,
            test_coseno=self.evaluacion.evaluar(yt, sim_test, umbral_cos),
            ranking=ranking, ruta_modelo=ruta, tamano_mb=tamano_mb,
        )