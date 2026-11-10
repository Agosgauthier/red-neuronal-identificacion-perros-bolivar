"""EvaluacionService: métricas y elección del umbral (siempre con VALIDACIÓN)."""
import numpy as np
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)


class EvaluacionService:
    @staticmethod
    def elegir_umbral(y_val, puntajes_val, desde=0.30, hasta=1.00, paso=0.01):
        mejor_u, mejor_f1 = desde, -1.0
        for u in np.arange(desde, hasta, paso):
            f1 = f1_score(y_val, (puntajes_val >= u).astype(int), zero_division=0)
            if f1 > mejor_f1:
                mejor_u, mejor_f1 = float(u), float(f1)
        return mejor_u, mejor_f1

    @staticmethod
    def metricas(y_real, puntajes, umbral) -> dict:
        y_pred = (np.asarray(puntajes) >= umbral).astype(int)
        return {
            "umbral": umbral,
            "accuracy": accuracy_score(y_real, y_pred),
            "precision": precision_score(y_real, y_pred, zero_division=0),
            "recall": recall_score(y_real, y_pred, zero_division=0),
            "f1": f1_score(y_real, y_pred, zero_division=0),
            "matriz_confusion": confusion_matrix(y_real, y_pred).tolist(),
        }

    @staticmethod
    def ranking(vectores_galeria, vectores_consulta, tops=(1, 3, 5)) -> dict:
        """La consulta i debe encontrar a la galería i."""
        def norm(m):
            return m / np.maximum(np.linalg.norm(m, axis=1, keepdims=True), 1e-9)
        sims = norm(vectores_consulta) @ norm(vectores_galeria).T
        aciertos = {k: 0 for k in tops}
        for i in range(len(sims)):
            pos = int(np.where(np.argsort(-sims[i]) == i)[0][0])
            for k in tops:
                aciertos[k] += pos < k
        return aciertos