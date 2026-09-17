from pathlib import Path
import json
import zipfile

import tensorflow as tf


PROYECTO = Path(__file__).resolve().parents[1]

MODELO_ORIGINAL = (
    PROYECTO
    / "model"
    / "modelo_perros_bolivar_12000.keras"
)

MODELO_NUEVO = (
    PROYECTO
    / "model"
    / "modelo_perros_bolivar_12000_app.keras"
)


@tf.keras.utils.register_keras_serializable(package="Perros")
class AbsDifference(tf.keras.layers.Layer):

    def call(self, inputs):
        return tf.abs(inputs[0] - inputs[1])


def reemplazar_lambda(obj):
    cantidad = 0

    if isinstance(obj, dict):

        if obj.get("class_name") == "Lambda":

            config = obj.get("config", {})

            obj["module"] = None
            obj["class_name"] = "AbsDifference"
            obj["registered_name"] = "Perros>AbsDifference"

            obj["config"] = {
                "name": config.get(
                    "name",
                    "abs_difference"
                ),
                "trainable": config.get(
                    "trainable",
                    True
                ),
                "dtype": config.get(
                    "dtype",
                    "float32"
                ),
            }

            cantidad += 1

        for valor in obj.values():
            cantidad += reemplazar_lambda(valor)

    elif isinstance(obj, list):

        for valor in obj:
            cantidad += reemplazar_lambda(valor)

    return cantidad


print()
print("Modificando el modelo...")
print(MODELO_ORIGINAL)


with zipfile.ZipFile(
    MODELO_ORIGINAL,
    "r"
) as entrada:

    with zipfile.ZipFile(
        MODELO_NUEVO,
        "w",
        zipfile.ZIP_DEFLATED
    ) as salida:

        for archivo in entrada.infolist():

            datos = entrada.read(archivo.filename)

            if archivo.filename == "config.json":

                config = json.loads(
                    datos.decode("utf-8")
                )

                cantidad = reemplazar_lambda(config)

                print()
                print(
                    f"Capas Lambda encontradas: {cantidad}"
                )

                if cantidad != 1:

                    raise RuntimeError(
                        "Se esperaba exactamente "
                        "1 capa Lambda."
                    )

                datos = json.dumps(
                    config,
                    ensure_ascii=False,
                    indent=2
                ).encode("utf-8")

            salida.writestr(
                archivo,
                datos
            )


print()
print("Archivo creado:")
print(MODELO_NUEVO)


print()
print("Probando carga del modelo...")


modelo = tf.keras.models.load_model(
    MODELO_NUEVO,
    custom_objects={
        "AbsDifference": AbsDifference
    },
    compile=False
)


print()
print("========================================")
print("MODELO CARGADO CORRECTAMENTE")
print("========================================")
print(
    f"Capas: {len(modelo.layers)}"
)
print(
    f"Entrada 1: {modelo.inputs[0].shape}"
)
print(
    f"Entrada 2: {modelo.inputs[1].shape}"
)
print(
    f"Salida: {modelo.outputs[0].shape}"
)