"""ExtractorService: construye la CNN propia (desde cero) que convierte una foto en un vector.

Lo comparten la red siamesa y el experimento de trillizos. TensorFlow se importa
adentro de los métodos para que el resto del proyecto funcione sin instalarlo.
"""


class ExtractorService:
    FILTROS = (32, 64, 128, 256)

    def __init__(self, tamano: int = 128):
        self.tamano = tamano

    def _bloque(self, x, filtros: int):
        from tensorflow.keras import layers

        x = layers.Conv2D(filtros, 3, padding="same", use_bias=False)(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation("relu")(x)
        return layers.MaxPooling2D()(x)

    def construir(self, con_brillo: bool = False, activacion_final=None):
        """Todos los pesos parten de valores aleatorios: NO hay redes preentrenadas."""
        from tensorflow.keras import Model, layers

        entrada = layers.Input(shape=(self.tamano, self.tamano, 3))
        x = layers.RandomFlip("horizontal")(entrada)
        x = layers.RandomRotation(0.05)(x)
        x = layers.RandomZoom(0.1)(x)
        if con_brillo:
            x = layers.RandomBrightness(0.2, value_range=(0, 1))(x)
        for filtros in self.FILTROS:
            x = self._bloque(x, filtros)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dropout(0.3)(x)
        x = layers.Dense(128, activation=activacion_final)(x)
        return Model(entrada, x, name="extractor_128")