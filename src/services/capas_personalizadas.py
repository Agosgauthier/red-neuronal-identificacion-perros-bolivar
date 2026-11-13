"""CapasPersonalizadas: capas Keras propias, registradas una sola vez.

TensorFlow se importa recién al pedir la capa, así el resto del proyecto
(y los tests del CI) funciona sin instalarlo.
"""


class CapasPersonalizadas:
    _abs_difference = None

    @classmethod
    def abs_difference(cls):
        """Devuelve la capa |a - b| (se crea y registra la primera vez)."""
        if cls._abs_difference is None:
            import tensorflow as tf

            @tf.keras.utils.register_keras_serializable(package="Perros")
            class AbsDifference(tf.keras.layers.Layer):
                def call(self, inputs):
                    return tf.abs(inputs[0] - inputs[1])

            cls._abs_difference = AbsDifference
        return cls._abs_difference