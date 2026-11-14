"""TrillizosService: entrena el extractor con pérdida de trillizos (experimento D).

TensorFlow se importa adentro de los métodos que lo usan.
"""
import random

import numpy as np

from src.services.extractor_service import ExtractorService
from src.services.imagen_service import ImagenService


class TrillizosService:
    def __init__(self, tamano=128, perros_por_tanda=16, fotos_por_perro=4, margen=0.3,
                 extractor_service: ExtractorService = None, imagenes: ImagenService = None):
        self.tamano = tamano
        self.perros_por_tanda = perros_por_tanda    # P: perros distintos en cada tanda
        self.fotos_por_perro = fotos_por_perro      # K: fotos de cada perro en la tanda
        self.margen = margen
        self.extractor_service = extractor_service or ExtractorService(tamano)
        self.imagenes = imagenes or ImagenService(tamano)

    def construir_extractor(self):
        return self.extractor_service.construir(con_brillo=True)

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

    def generador_tandas(self, perros_train):
        """Cada tanda: P perros distintos x K fotos de cada uno. perros_train = [PerroDataset]."""
        while True:
            elegidos = random.sample(range(len(perros_train)), self.perros_por_tanda)
            imgs, etiquetas = [], []
            for idx in elegidos:
                fotos = perros_train[idx].fotos
                if len(fotos) >= self.fotos_por_perro:
                    seleccion = random.sample(fotos, self.fotos_por_perro)
                else:
                    seleccion = random.choices(fotos, k=self.fotos_por_perro)
                for foto in seleccion:
                    imgs.append(self.imagenes.cargar_normalizada(foto))
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

    def entrenar(self, perros_train, epocas=30, pasos_por_epoca=100, learning_rate=0.001):
        import tensorflow as tf

        extractor = self.construir_extractor()
        extractor.compile(optimizer=tf.keras.optimizers.Adam(learning_rate),
                          loss=self.perdida_trillizos)
        extractor.fit(self.crear_dataset(perros_train),
                      steps_per_epoch=pasos_por_epoca, epochs=epocas)
        return extractor