"""RedSiamesaService: el servicio del modelo. Construye, entrena, prueba y guarda la red siamesa.

Reemplaza al notebook: toda la lógica de la red vive acá, en una clase.
La red se entrena desde cero: todos los pesos parten de valores aleatorios.
"""
from pathlib import Path

import numpy as np

from src.domain.configuracion_entrenamiento import ConfiguracionEntrenamiento
from src.services.aumento_service import AumentoService
from src.services.capas_personalizadas import CapasPersonalizadas
from src.services.extractor_service import ExtractorService
from src.services.lotes_service import LotesService


class RedSiamesaService:
    def __init__(self, config: ConfiguracionEntrenamiento,
                 extractor_service: ExtractorService = None,
                 lotes: LotesService = None):
        self.config = config
        self.extractor_service = extractor_service or ExtractorService(config.tamano)
        self.lotes = lotes or LotesService(AumentoService(), config.semilla)
        self.extractor = None
        self.modelo = None
        self.historia = None

    # ---------- 2 y 3: elegir y configurar el modelo ----------
    def construir(self):
        import tensorflow as tf
        from tensorflow.keras import Model, layers

        t = self.config.tamano
        self.extractor = self.extractor_service.construir(activacion_final="relu")

        imagen_1 = layers.Input(shape=(t, t, 3), name="imagen_1")
        imagen_2 = layers.Input(shape=(t, t, 3), name="imagen_2")
        diferencia = CapasPersonalizadas.abs_difference()(name="diferencia")(
            [self.extractor(imagen_1), self.extractor(imagen_2)])
        x = layers.Dense(64, activation="relu", name="comparacion")(diferencia)
        salida = layers.Dense(1, activation="sigmoid", name="salida")(x)

        self.modelo = Model([imagen_1, imagen_2], salida)
        self.modelo.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=self.config.learning_rate),
            loss="binary_crossentropy",
            metrics=["accuracy"],
        )
        return self.modelo

    # ---------- 4: entrenar ----------
    def entrenar(self, x1, x2, y, x1_val, x2_val, y_val):
        import tensorflow as tf

        c = self.config
        t = c.tamano
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor="val_loss", patience=c.paciencia_early_stopping,
                restore_best_weights=True),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor="val_loss", factor=c.factor_reduce_lr,
                patience=c.paciencia_reduce_lr, min_lr=c.lr_minimo),
        ]
        firma = ({"imagen_1": tf.TensorSpec((None, t, t, 3), tf.float32),
                  "imagen_2": tf.TensorSpec((None, t, t, 3), tf.float32)},
                 tf.TensorSpec((None,), tf.float32))
        datos = tf.data.Dataset.from_generator(
            lambda: self.lotes.generar(x1, x2, y, c.batch_size),
            output_signature=firma,
        ).prefetch(2)
        self.historia = self.modelo.fit(
            datos,
            steps_per_epoch=self.lotes.cantidad_de_lotes(len(y), c.batch_size),
            validation_data=([x1_val, x2_val], y_val),
            epochs=c.epocas, callbacks=callbacks,
        )
        return self.historia

    # ---------- 5: probarlo ----------
    def predecir(self, x1, x2) -> np.ndarray:
        """Probabilidad de 'mismo perro' para cada par."""
        return self.modelo.predict([x1, x2], verbose=0).ravel()

    def extraer_vectores(self, x) -> np.ndarray:
        return self.extractor.predict(x, verbose=0)

    # ---------- guardar ----------
    def guardar(self, ruta: Path) -> float:
        """Guarda el modelo, comprueba que existe y devuelve su tamaño en MB."""
        ruta = Path(ruta)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        self.modelo.save(str(ruta))
        if not ruta.exists():
            raise RuntimeError(f"No se pudo guardar el modelo en {ruta}")
        return round(ruta.stat().st_size / (1024 * 1024), 2)