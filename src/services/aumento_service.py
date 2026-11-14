"""AumentoService: variaciones aleatorias de una foto para entrenar (tapar zonas, recortar, luz).

Trabaja con arrays numpy (T, T, 3) con valores entre 0 y 1. No usa TensorFlow.
"""
import numpy as np


class AumentoService:
    def __init__(self, prob_oclusion=0.5, prob_recorte=0.5, prob_luz=0.5, semilla=None):
        self.prob_oclusion = prob_oclusion
        self.prob_recorte = prob_recorte
        self.prob_luz = prob_luz
        self.azar = np.random.default_rng(semilla)

    def aplicar(self, imagen):
        """Aplica al azar recorte, cambio de luz y oclusión. No modifica la imagen original."""
        img = imagen
        if self.azar.random() < self.prob_recorte:
            img = self.recortar(img)
        if self.azar.random() < self.prob_luz:
            img = self.variar_luz(img)
        if self.azar.random() < self.prob_oclusion:
            img = self.ocluir(img)
        return img.astype("float32")

    def recortar(self, imagen, minimo=0.6):
        """Se queda con una zona al azar (60 a 100 % del lado) y la estira al tamaño original."""
        t = imagen.shape[0]
        lado = int(t * self.azar.uniform(minimo, 1.0))
        y = int(self.azar.integers(0, t - lado + 1))
        x = int(self.azar.integers(0, t - lado + 1))
        zona = imagen[y:y + lado, x:x + lado]
        posiciones = (np.arange(t) * lado / t).astype(int)
        return zona[posiciones][:, posiciones]

    def variar_luz(self, imagen):
        brillo = self.azar.uniform(-0.15, 0.15)
        contraste = self.azar.uniform(0.8, 1.2)
        return np.clip((imagen - 0.5) * contraste + 0.5 + brillo, 0.0, 1.0)

    def ocluir(self, imagen):
        """Tapa un rectángulo (5 a 30 % del área) con un color liso o ruido: simula una mano o un objeto."""
        t = imagen.shape[0]
        area = self.azar.uniform(0.05, 0.30) * t * t
        proporcion = self.azar.uniform(0.5, 2.0)
        alto = int(min(t, np.sqrt(area * proporcion)))
        ancho = int(min(t, np.sqrt(area / proporcion)))
        y = int(self.azar.integers(0, t - alto + 1))
        x = int(self.azar.integers(0, t - ancho + 1))
        salida = imagen.copy()
        if self.azar.random() < 0.5:
            salida[y:y + alto, x:x + ancho] = self.azar.random(3)
        else:
            salida[y:y + alto, x:x + ancho] = self.azar.random((alto, ancho, 3))
        return salida