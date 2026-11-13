"""ConsolaView: muestra por consola el avance y los resultados del entrenamiento."""
from src.domain.configuracion_entrenamiento import ConfiguracionEntrenamiento
from src.domain.metricas_evaluacion import MetricasEvaluacion
from src.domain.resultado_experimento import ResultadoExperimento


class ConsolaView:
    def paso(self, titulo: str) -> None:
        print(f"\n=== {titulo} ===")

    def mostrar_tamanos(self, tamanos: dict) -> None:
        for nombre, cantidad in tamanos.items():
            print(f"  {nombre}: {cantidad} pares")

    def mostrar_configuracion(self, c: ConfiguracionEntrenamiento) -> None:
        print(f"  Adam lr={c.learning_rate} | batch={c.batch_size} | épocas máx={c.epocas} | "
              f"EarlyStopping paciencia={c.paciencia_early_stopping}")

    def _metricas(self, titulo: str, m: MetricasEvaluacion) -> None:
        print(f"\n{titulo} (umbral {m.umbral:.4g})")
        print(f"  Accuracy {m.accuracy:.2%} | Precision {m.precision:.2%} | "
              f"Recall {m.recall:.2%} | F1 {m.f1:.2%}")
        print(f"  Matriz de confusión: {m.matriz_confusion}")

    def mostrar_resultado(self, r: ResultadoExperimento) -> None:
        self.paso("RESULTADOS EN PERROS NUEVOS (prueba)")
        self._metricas("Salida de la red", r.test_umbral_05)
        self._metricas("Salida de la red, umbral elegido en validación", r.test_umbral_red)
        self._metricas("Similitud coseno", r.test_coseno)
        print(f"\nBuscador ({r.ranking.total} perros): "
              + " | ".join(f"entre los {k} primeros {v}" for k, v in r.ranking.aciertos.items()))
        print(f"\nModelo guardado en {r.ruta_modelo} ({r.tamano_mb} MB)")
        print("\nSi este modelo reemplaza al de la app, copiarlo a model/ y poner en src/config.py:")
        print(f"  UMBRAL_COINCIDENCIA = {r.umbral_red:.2f}   "
              f"# F1 de validación {r.f1_validacion_red:.4f}")