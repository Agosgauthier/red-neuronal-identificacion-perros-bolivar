from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


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
    / "modelo_perros_bolivar_12000_app.keras"
)


# ============================================================
# PARÁMETROS
# ============================================================

TAMANO = 128
BATCH_SIZE = 32


# ============================================================
# CAPA PERSONALIZADA
# ============================================================

@tf.keras.utils.register_keras_serializable(
    package="Perros"
)
class AbsDifference(tf.keras.layers.Layer):

    def call(self, inputs):
        return tf.abs(
            inputs[0] - inputs[1]
        )


# ============================================================
# CARGAR TEST
# ============================================================

df_test = pd.read_csv(
    TEST_CSV
)

print()
print("========================================")
print("EVALUACIÓN DE SIMILITUD")
print("========================================")

print(
    "Pares de prueba:",
    len(df_test)
)

print(
    "Mismo perro:",
    int((df_test["label"] == 1).sum())
)

print(
    "Perros diferentes:",
    int((df_test["label"] == 0).sum())
)


# ============================================================
# CARGAR MODELO
# ============================================================

print()
print("Cargando modelo...")

modelo = tf.keras.models.load_model(
    MODELO,
    custom_objects={
        "AbsDifference": AbsDifference
    },
    compile=False
)

print(
    "Modelo cargado correctamente."
)


# ============================================================
# OBTENER EXTRACTOR
# ============================================================

extractor = modelo.get_layer(
    "extractor_128"
)

print(
    "Extractor encontrado:",
    extractor.name
)


# ============================================================
# CARGAR IMAGEN
# ============================================================

def cargar_imagen(ruta):

    imagen = cv2.imread(
        str(ruta)
    )

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
# SIMILITUD COSENO
# ============================================================

def similitud_coseno(vector1, vector2):

    norma1 = np.linalg.norm(
        vector1,
        axis=1,
        keepdims=True
    )

    norma2 = np.linalg.norm(
        vector2,
        axis=1,
        keepdims=True
    )

    norma1 = np.maximum(
        norma1,
        1e-8
    )

    norma2 = np.maximum(
        norma2,
        1e-8
    )

    vector1 = vector1 / norma1
    vector2 = vector2 / norma2

    similitud = np.sum(
        vector1 * vector2,
        axis=1
    )

    return similitud


# ============================================================
# OBTENER EMBEDDINGS
# ============================================================

todos_v1 = []
todos_v2 = []
y_real = []


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

    v1 = extractor.predict(
        x1,
        verbose=0
    )

    v2 = extractor.predict(
        x2,
        verbose=0
    )

    todos_v1.append(v1)
    todos_v2.append(v2)

    y_real.extend(
        lote["label"].astype(int).tolist()
    )

    print(
        f"Procesados: "
        f"{min(inicio + BATCH_SIZE, len(df_test))}"
        f"/{len(df_test)}"
    )


v1 = np.concatenate(
    todos_v1,
    axis=0
)

v2 = np.concatenate(
    todos_v2,
    axis=0
)

y_real = np.asarray(
    y_real,
    dtype=int
)


# ============================================================
# CALCULAR SIMILITUDES
# ============================================================

similitudes = similitud_coseno(
    v1,
    v2
)


# ============================================================
# SEPARAR POSITIVOS Y NEGATIVOS
# ============================================================

similitudes_mismo = similitudes[
    y_real == 1
]

similitudes_diferente = similitudes[
    y_real == 0
]


# ============================================================
# ESTADÍSTICAS
# ============================================================

print()
print("========================================")
print("DISTRIBUCIÓN DE SIMILITUD")
print("========================================")

print()
print("MISMO PERRO")

print(
    f"Promedio : {np.mean(similitudes_mismo):.4f}"
)

print(
    f"Mínimo   : {np.min(similitudes_mismo):.4f}"
)

print(
    f"Máximo   : {np.max(similitudes_mismo):.4f}"
)

print(
    f"Mediana  : {np.median(similitudes_mismo):.4f}"
)


print()
print("PERROS DIFERENTES")

print(
    f"Promedio : {np.mean(similitudes_diferente):.4f}"
)

print(
    f"Mínimo   : {np.min(similitudes_diferente):.4f}"
)

print(
    f"Máximo   : {np.max(similitudes_diferente):.4f}"
)

print(
    f"Mediana  : {np.median(similitudes_diferente):.4f}"
)


# ============================================================
# PRUEBA DE UMBRALES
# ============================================================

print()
print("========================================")
print("PRUEBA DE UMBRALES")
print("========================================")

mejor_f1 = -1
mejor_umbral = None

for umbral in np.arange(
    0.50,
    1.001,
    0.01
):

    predicciones = (
        similitudes >= umbral
    ).astype(int)

    f1 = f1_score(
        y_real,
        predicciones,
        zero_division=0
    )

    if f1 > mejor_f1:

        mejor_f1 = f1
        mejor_umbral = umbral


print(
    f"Mejor umbral por F1: "
    f"{mejor_umbral:.2f}"
)

print(
    f"F1 obtenido: "
    f"{mejor_f1:.4f}"
)


# ============================================================
# MÉTRICAS DEL MEJOR UMBRAL
# ============================================================

y_pred = (
    similitudes >= mejor_umbral
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


print()
print("========================================")
print("MÉTRICAS DEL UMBRAL")
print("========================================")

print(
    f"Accuracy : {accuracy:.4f}"
)

print(
    f"Precision: {precision:.4f}"
)

print(
    f"Recall   : {recall:.4f}"
)

print(
    f"F1-score : {f1:.4f}"
)


# ============================================================
# PERCENTILES DE NEGATIVOS
# ============================================================

print()
print("========================================")
print("PERCENTILES DE PERROS DIFERENTES")
print("========================================")

for porcentaje in [90, 95, 97, 99]:

    valor = np.percentile(
        similitudes_diferente,
        porcentaje
    )

    print(
        f"P{porcentaje}: {valor:.4f}"
    )


print()
print("========================================")
print("FIN DE LA EVALUACIÓN")
print("========================================")