from pathlib import Path
import zipfile
import tempfile

import cv2
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

from tensorflow.keras import layers, Model
from tensorflow.keras.applications import MobileNetV2


# ============================================================
# RUTAS
# ============================================================

PROYECTO = Path(__file__).resolve().parents[1]

TEST_CSV = (
    PROYECTO
    / "dataset"
    / "pares_test_grande.csv"
)

MODELO = (
    PROYECTO
    / "model"
    / "modelo_perros_bolivar_12000.keras"
)


# ============================================================
# PARÁMETROS
# ============================================================

TAMANO = 128
BATCH_SIZE = 32


# ============================================================
# CARGAR TEST
# ============================================================

df_test = pd.read_csv(TEST_CSV)

print("Pares de prueba:", len(df_test))


# ============================================================
# CARGAR IMAGEN
# ============================================================

def cargar_imagen(ruta):

    imagen = cv2.imread(str(ruta))

    if imagen is None:
        raise ValueError(
            f"No se pudo cargar: {ruta}"
        )

    imagen = cv2.cvtColor(
        imagen,
        cv2.COLOR_BGR2RGB
    )

    imagen = cv2.resize(
        imagen,
        (TAMANO, TAMANO)
    )

    imagen = (
        imagen.astype("float32")
        / 255.0
    )

    return imagen


# ============================================================
# EXTRAER PESOS DEL .KERAS
# ============================================================

with tempfile.TemporaryDirectory() as carpeta:

    carpeta = Path(carpeta)

    with zipfile.ZipFile(
        MODELO,
        "r"
    ) as archivo_zip:

        archivo_zip.extractall(carpeta)

    weights_file = carpeta / "model.weights.h5"

    if not weights_file.exists():
        raise FileNotFoundError(
            "No se encontró model.weights.h5 dentro del modelo .keras"
        )

    print("Pesos encontrados correctamente.")


    # ========================================================
    # RECREAR LA MISMA ARQUITECTURA
    # ========================================================

    base_model = MobileNetV2(
        input_shape=(TAMANO, TAMANO, 3),
        include_top=False,
        weights="imagenet"
    )

    base_model.trainable = True

    for layer in base_model.layers[:-20]:
        layer.trainable = False

    for layer in base_model.layers:
        if isinstance(
            layer,
            tf.keras.layers.BatchNormalization
        ):
            layer.trainable = False


    entrada = layers.Input(
        shape=(TAMANO, TAMANO, 3),
        name="imagen_entrada"
    )

    x = layers.Rescaling(
        scale=2.0,
        offset=-1.0
    )(entrada)

    x = base_model(
        x,
        training=False
    )

    x = layers.GlobalAveragePooling2D()(x)

    x = layers.Dense(
        128,
        activation="relu"
    )(x)

    extractor = Model(
        entrada,
        x,
        name="extractor_128"
    )


    entrada1 = layers.Input(
        shape=(TAMANO, TAMANO, 3),
        name="imagen_1"
    )

    entrada2 = layers.Input(
        shape=(TAMANO, TAMANO, 3),
        name="imagen_2"
    )

    vector1 = extractor(entrada1)
    vector2 = extractor(entrada2)

    diferencia = layers.Lambda(
        lambda x: tf.abs(x[0] - x[1]),
        output_shape=(128,)
    )(
        [vector1, vector2]
    )

    x = layers.Dense(
        64,
        activation="relu"
    )(diferencia)

    salida = layers.Dense(
        1,
        activation="sigmoid"
    )(x)


    modelo = Model(
        inputs=[entrada1, entrada2],
        outputs=salida
    )


    # Construir
    modelo.build(
        [
            (None, TAMANO, TAMANO, 3),
            (None, TAMANO, TAMANO, 3)
        ]
    )


    # ========================================================
    # CARGAR LOS PESOS ENTRENADOS
    # ========================================================

    print("Cargando pesos entrenados...")

    modelo.load_weights(
        weights_file
    )

    print("Pesos cargados correctamente.")


    # ========================================================
    # PREDICCIONES
    # ========================================================

    y_real = []
    y_pred_prob = []


    for inicio in range(
        0,
        len(df_test),
        BATCH_SIZE
    ):

        lote = df_test.iloc[
            inicio:inicio + BATCH_SIZE
        ]

        x1 = []
        x2 = []

        for _, fila in lote.iterrows():

            x1.append(
                cargar_imagen(
                    fila["imagen1"]
                )
            )

            x2.append(
                cargar_imagen(
                    fila["imagen2"]
                )
            )

        x1 = np.asarray(
            x1,
            dtype="float32"
        )

        x2 = np.asarray(
            x2,
            dtype="float32"
        )

        predicciones = modelo.predict(
            [x1, x2],
            verbose=0
        ).reshape(-1)

        y_real.extend(
            lote["label"].astype(int).tolist()
        )

        y_pred_prob.extend(
            predicciones.tolist()
        )


# ============================================================
# MÉTRICAS
# ============================================================

y_real = np.asarray(
    y_real,
    dtype=int
)

y_pred_prob = np.asarray(
    y_pred_prob
)

y_pred = (
    y_pred_prob >= 0.5
).astype(int)


accuracy = accuracy_score(
    y_real,
    y_pred
)

precision = precision_score(
    y_real,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_real,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_real,
    y_pred,
    zero_division=0
)

matriz = confusion_matrix(
    y_real,
    y_pred
)


# ============================================================
# RESULTADOS
# ============================================================

print()
print("========================================")
print("EVALUACIÓN DEL MODELO 12.000")
print("========================================")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1-score : {f1:.4f}")

print()
print("Matriz de confusión:")
print(matriz)

print()
print("Reporte completo:")

print(
    classification_report(
        y_real,
        y_pred,
        target_names=[
            "Perros diferentes",
            "Mismo perro"
        ],
        zero_division=0
    )
)