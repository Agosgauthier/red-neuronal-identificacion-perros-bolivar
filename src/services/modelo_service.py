"""ModeloService: carga la red siamesa y calcula la probabilidad de "mismo perro".

TensorFlow se importa solo al cargar el modelo, así el resto del proyecto
(y los tests) funciona sin él.
"""
import numpy as np
from PIL import Image

from src import config


class ModeloService:
    def __init__(self, predictor=None, extractor=None, tamano=config.TAMANO_IMAGEN):
        """predictor: callable(x1, x2) -> probabilidad (red completa).
        extractor: callable(x) -> vector (para similitud coseno)."""
        self._predictor = predictor
        self._extractor = extractor
        self.tamano = tamano
        self._redimensionar = self._redimensionar_pil
        self._leer = self._leer_pil

    # ---------- carga del modelo real ----------
    def cargar_desde_archivo(self, ruta=config.RUTA_MODELO):
        import tensorflow as tf

        @tf.keras.utils.register_keras_serializable(package="Perros")
        class AbsDifference(tf.keras.layers.Layer):
            def call(self, inputs):
                return tf.abs(inputs[0] - inputs[1])

        modelo = tf.keras.models.load_model(
            ruta,
            custom_objects={"AbsDifference": AbsDifference},
            safe_mode=False,
            compile=False,
        )
        extractor = modelo.get_layer(config.CAPA_EXTRACTOR)

        self._predictor = lambda a, b: modelo([a, b], training=False).numpy()
        self._extractor = lambda x: extractor(x, training=False).numpy()

        # Igual que la app original: se redimensiona y se lee con TensorFlow.
        self._redimensionar = lambda arr: tf.image.resize(
            arr, (self.tamano, self.tamano)).numpy()

        def leer(ruta_imagen):
            contenido = tf.io.read_file(str(ruta_imagen))
            img = tf.image.decode_image(contenido, channels=3, expand_animations=False)
            return img.numpy()

        self._leer = leer
        return self

    # ---------- lectura y preprocesamiento ----------
    @staticmethod
    def _leer_pil(ruta):
        with Image.open(ruta) as img:
            return np.asarray(img.convert("RGB"))

    def _redimensionar_pil(self, arr):
        pil = Image.fromarray(arr.astype(np.uint8)).resize(
            (self.tamano, self.tamano), Image.BILINEAR)
        return np.asarray(pil, dtype="float32")

    def leer_imagen(self, ruta):
        return self._leer(ruta)

    def preparar_imagen(self, imagen) -> np.ndarray:
        """Devuelve (1, T, T, 3), float32, valores 0-1."""
        arr = np.array(imagen)
        if arr.ndim == 2:
            arr = np.stack([arr, arr, arr], axis=-1)
        if arr.shape[-1] == 4:
            arr = arr[:, :, :3]
        arr = np.asarray(self._redimensionar(arr), dtype="float32") / 255.0
        return arr[np.newaxis, ...]

    # ---------- resultados ----------
    def probabilidad_mismo(self, imagen1, imagen2) -> float:
        """Probabilidad (0-1) de que sean el mismo perro, según la red."""
        if self._predictor is None:
            raise RuntimeError("El modelo no está cargado.")
        resultado = np.asarray(self._predictor(
            self.preparar_imagen(imagen1), self.preparar_imagen(imagen2)))
        return float(np.clip(resultado.reshape(-1)[0], 0.0, 1.0))

    def calcular_vector(self, imagen) -> np.ndarray:
        if self._extractor is None:
            raise RuntimeError("El modelo no está cargado.")
        return np.asarray(self._extractor(self.preparar_imagen(imagen)))[0]

    @staticmethod
    def similitud_coseno(v1, v2) -> float:
        n1, n2 = np.linalg.norm(v1), np.linalg.norm(v2)
        if n1 == 0 or n2 == 0:
            return 0.0
        return float(np.clip(np.dot(v1, v2) / (n1 * n2), 0.0, 1.0))