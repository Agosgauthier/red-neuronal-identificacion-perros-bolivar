"""EntrenamientoService: construye y entrena el extractor (modelo D) con pérdida de trillizos.

TensorFlow y OpenCV se importan adentro de los métodos que los usan,
así el resto del proyecto (y los tests del CI) funciona sin instalarlos.
"""
import random

import numpy as np


class EntrenamientoService:
    def __init__(self, tamano=128, perros_por_tanda=16, fotos_por_perro=4, margen=0.3):
        self.tamano = tamano
        self.perros_por_tanda = perros_por_tanda    # P: perros distintos en cada tanda
        self.fotos_por_perro = fotos_por_perro      # K: fotos de cada perro en la tanda
        self.margen = margen

    # ---------- la red ----------
    def bloque(self, x, filtros):
        from tensorflow.keras import layers
        x = layers.Conv2D(filtros, 3, padding="same", use_bias=False)(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation("relu")(x)
        x = layers.MaxPooling2D()(x)
        return x

    def construir_extractor(self):
        from tensorflow.keras import layers, Model

        entrada = layers.Input(shape=(self.tamano, self.tamano, 3))
        x = layers.RandomFlip("horizontal")(entrada)
        x = layers.RandomRotation(0.05)(x)
        x = layers.RandomZoom(0.1)(x)
        x = layers.RandomBrightness(0.2, value_range=(0, 1))(x)
        for filtros in [32, 64, 128, 256]:
            x = self.bloque(x, filtros)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dropout(0.3)(x)
        x = layers.Dense(128)(x)
        return Model(entrada, x, name="extractor_128")

    # ---------- la pérdida ----------
    def perdida_trillizos(self, etiquetas, embeddings):
        import tensorflow as tf

        etiquetas = tf.reshape(etiquetas, [-1])
        emb = tf.math.l2_normalize(embeddings, axis=1)
        dist = 1.0 - tf.matmul(emb, emb, transpose_b=True)
        mismo = tf.equal(etiquetas[:, None], etiquetas[None, :])
        yo = tf.eye(tf.shape(etiquetas)[0], dtype=tf.bool)
        mask_pos = tf.logical_and(mismo, tf.logical_not(yo))
        mask_neg = tf.logical_not(mismo)
        pos = tf.reduce_max(tf.where(mask_pos, dist, tf.zeros_like(dist)), axis=1)
        neg = tf.reduce_min(tf.where(mask_neg, dist, 10.0 * tf.ones_like(dist)), axis=1)
        return tf.reduce_mean(tf.maximum(pos - neg + self.margen, 0.0))

    # ---------- los datos ----------
    def cargar_imagen(self, ruta):
        import cv2

        imagen = cv2.imread(str(ruta))
        if imagen is None:
            raise ValueError(f"No se pudo cargar: {ruta}")
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        imagen = cv2.resize(imagen, (self.tamano, self.tamano))
        return imagen.astype("float32") / 255.0

    def generador_tandas(self, perros_train):
        """Cada tanda: P perros distintos x K fotos de cada uno. perros_train = [(id, [rutas])]."""
        while True:
            elegidos = random.sample(range(len(perros_train)), self.perros_por_tanda)
            imgs, etiquetas = [], []
            for idx in elegidos:
                _, fotos = perros_train[idx]
                if len(fotos) >= self.fotos_por_perro:
                    seleccion = random.sample(fotos, self.fotos_por_perro)
                else:
                    seleccion = random.choices(fotos, k=self.fotos_por_perro)
                for foto in seleccion:
                    imgs.append(self.cargar_imagen(foto))
                    etiquetas.append(idx)
            yield np.array(imgs), np.array(etiquetas, dtype="int32")

    def crear_dataset(self, perros_train):
        import tensorflow as tf

        tanda = self.perros_por_tanda * self.fotos_por_perro
        return tf.data.Dataset.from_generator(
            lambda: self.generador_tandas(perros_train),
            output_signature=(
                tf.TensorSpec(shape=(tanda, self.tamano, self.tamano, 3), dtype=tf.float32),
                tf.TensorSpec(shape=(tanda,), dtype=tf.int32),
            ),
        ).prefetch(4)

    # ---------- entrenar ----------
    def entrenar(self, perros_train, epocas=30, pasos_por_epoca=100, learning_rate=0.001):
        import tensorflow as tf

        extractor = self.construir_extractor()
        extractor.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate),
            loss=self.perdida_trillizos,
        )
        extractor.fit(
            self.crear_dataset(perros_train),
            steps_per_epoch=pasos_por_epoca,
            epochs=epocas,
        )
        return extractor