"""EvaluacionService: métricas y elección del umbral (siempre con VALIDACIÓN)."""
import numpy as np
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)

from src.domain.metricas_evaluacion import MetricasEvaluacion
from src.domain.resultado_ranking import ResultadoRanking


class EvaluacionService:
    def elegir_umbral(self, y_val, puntajes_val, desde=0.05, hasta=0.96, paso=0.05) -> tuple:
        """Devuelve (umbral, f1) con el mayor F1 sobre VALIDACIÓN."""
        mejor_u, mejor_f1 = desde, -1.0
        for u in np.arange(desde, hasta, paso):
            f1 = f1_score(y_val, (np.asarray(puntajes_val) >= u).astype(int), zero_division=0)
            if f1 > mejor_f1:
                mejor_u, mejor_f1 = float(u), float(f1)
        return mejor_u, mejor_f1

    def evaluar(self, y_real, puntajes, umbral: float) -> MetricasEvaluacion:
        y_pred = (np.asarray(puntajes) >= umbral).astype(int)
        return MetricasEvaluacion(
            umbral=umbral,
            accuracy=float(accuracy_score(y_real, y_pred)),
            precision=float(precision_score(y_real, y_pred, zero_division=0)),
            recall=float(recall_score(y_real, y_pred, zero_division=0)),
            f1=float(f1_score(y_real, y_pred, zero_division=0)),
            matriz_confusion=confusion_matrix(y_real, y_pred).tolist(),
        )

    def similitud_coseno(self, vectores_a, vectores_b) -> np.ndarray:
        """Coseno fila por fila entre dos matrices de vectores."""
        num = np.sum(vectores_a * vectores_b, axis=1)
        den = np.linalg.norm(vectores_a, axis=1) * np.linalg.norm(vectores_b, axis=1)
        return num / np.maximum(den, 1e-9)

    def ranking(self, vectores_galeria, vectores_consulta, tops=(1, 3, 5)) -> ResultadoRanking:
        """La consulta i debe encontrar a la galería i."""
        def normalizar(m):
            return m / np.maximum(np.linalg.norm(m, axis=1, keepdims=True), 1e-9)

        sims = normalizar(vectores_consulta) @ normalizar(vectores_galeria).T
        aciertos = {k: 0 for k in tops}
        for i in range(len(sims)):
            posicion = int(np.where(np.argsort(-sims[i]) == i)[0][0])
            for k in tops:
                aciertos[k] += posicion < k
        return ResultadoRanking(aciertos=aciertos, total=len(sims))