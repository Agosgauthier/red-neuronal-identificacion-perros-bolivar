from pathlib import Path

import gradio as gr
import numpy as np
import tensorflow as tf


# --------------------------------------------------
# Capa utilizada por nuestro modelo
# --------------------------------------------------

@tf.keras.utils.register_keras_serializable(package="Perros")
class AbsDifference(tf.keras.layers.Layer):
    def call(self, inputs):
        return tf.abs(inputs[0] - inputs[1])


# --------------------------------------------------
# Ruta del modelo
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RUTA_MODELO = (
    BASE_DIR
    / "model"
    / "modelo_perros_bolivar_final.keras"
)


# --------------------------------------------------
# Cargar el modelo final
# --------------------------------------------------

modelo_final = tf.keras.models.load_model(
    RUTA_MODELO,
    custom_objects={"AbsDifference": AbsDifference},
    safe_mode=False,
    compile=False
)


print("Modelo cargado correctamente.")


# --------------------------------------------------
# Preparar imagen
# --------------------------------------------------

def preparar_imagen(imagen):
    imagen = np.array(imagen)

    # Si tiene canal alfa, conservar solamente RGB
    if imagen.shape[-1] == 4:
        imagen = imagen[:, :, :3]

    # Redimensionar
    imagen = tf.image.resize(
        imagen,
        (128, 128)
    )

    # Convertir a valores entre 0 y 1
    imagen = tf.cast(
        imagen,
        tf.float32
    ) / 255.0

    # Agregar dimensión del batch
    imagen = tf.expand_dims(
        imagen,
        axis=0
    )

    return imagen


# --------------------------------------------------
# Comparar dos perros
# --------------------------------------------------

def comparar_perros(imagen1, imagen2):

    if imagen1 is None or imagen2 is None:
        return "⚠️ Cargá las dos imágenes."

    imagen1 = preparar_imagen(imagen1)
    imagen2 = preparar_imagen(imagen2)

    # Predicción
    prediccion = modelo_final.predict(
        [imagen1, imagen2],
        verbose=0
    )[0][0]

    probabilidad_mismo = float(prediccion)
    probabilidad_diferente = 1 - probabilidad_mismo

    if probabilidad_mismo >= 0.5:
        return (
            "🐕✅ MISMO PERRO\n\n"
            f"Probabilidad de mismo perro: "
            f"{probabilidad_mismo * 100:.2f}%"
        )

    return (
        "🐕❌ PERROS DIFERENTES\n\n"
        f"Probabilidad de perros diferentes: "
        f"{probabilidad_diferente * 100:.2f}%"
    )


# --------------------------------------------------
# Interfaz visual
# --------------------------------------------------

with gr.Blocks() as demo:

    gr.Markdown(
        """
        # 🐕 Identificación de Perros en Bolívar

        ## Comparación de dos fotografías

        Cargá dos fotografías para determinar
        si corresponden al mismo perro o a perros diferentes.
        """
    )

    with gr.Row():

        imagen1 = gr.Image(
            type="numpy",
            label="📷 Imagen 1"
        )

        imagen2 = gr.Image(
            type="numpy",
            label="📷 Imagen 2"
        )

    boton = gr.Button(
        "🔎 Comparar perros"
    )

    resultado = gr.Textbox(
        label="Resultado",
        lines=3
    )

    boton.click(
        fn=comparar_perros,
        inputs=[imagen1, imagen2],
        outputs=resultado
    )


# --------------------------------------------------
# Ejecutar interfaz
# --------------------------------------------------

if __name__ == "__main__":
    demo.launch()