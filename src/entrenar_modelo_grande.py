from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import tensorflow as tf

from tensorflow.keras import layers, Model
from tensorflow.keras.applications import MobileNetV2


# ============================================================
# RUTAS
# ============================================================

PROYECTO = Path(__file__).resolve().parents[1]

TRAIN_CSV = PROYECTO / "dataset" / "pares_train_grande.csv"
TEST_CSV = PROYECTO / "dataset" / "pares_test_grande.csv"

RUTA_MODELO = (
    PROYECTO
    / "model"
    / "modelo_perros_bolivar_12000.keras"
)


# ============================================================
# SEMILLAS
# ============================================================

SEED = 42

np.random.seed(SEED)
tf.random.set_seed(SEED)


# ============================================================
# PARÁMETROS
# ============================================================

TAMANO = 128
BATCH_SIZE = 32

EPOCHS_INICIALES = 10
EPOCHS_FINE_TUNING = 5


# ============================================================
# CARGAR DATAFRAMES
# ============================================================

df_train = pd.read_csv(TRAIN_CSV)
df_test = pd.read_csv(TEST_CSV)

print("========================================")
print("DATASET")
print("========================================")

print("Entrenamiento:", len(df_train))
print("Prueba:", len(df_test))

print(
    "Train mismo:",
    int((df_train["label"] == 1).sum())
)

print(
    "Train diferentes:",
    int((df_train["label"] == 0).sum())
)

print(
    "Test mismo:",
    int((df_test["label"] == 1).sum())
)

print(
    "Test diferentes:",
    int((df_test["label"] == 0).sum())
)


# ============================================================
# SEPARAR VALIDACIÓN
# ============================================================

df_train = df_train.sample(
    frac=1,
    random_state=SEED
).reset_index(drop=True)

cantidad_validacion = int(
    len(df_train) * 0.20
)

df_val = df_train.iloc[
    :cantidad_validacion
].copy()

df_train = df_train.iloc[
    cantidad_validacion:
].copy()

print()
print("Train:", len(df_train))
print("Validación:", len(df_val))
print("Test:", len(df_test))


# ============================================================
# GENERADOR DE DATOS
# ============================================================

class ParesSequence(tf.keras.utils.Sequence):

    def __init__(
        self,
        dataframe,
        batch_size=32,
        shuffle=True
    ):

        self.df = dataframe.reset_index(drop=True)
        self.batch_size = batch_size
        self.shuffle = shuffle

        self.indices = np.arange(
            len(self.df)
        )

        self.on_epoch_end()


    def __len__(self):

        return int(
            np.ceil(
                len(self.df)
                / self.batch_size
            )
        )


    def on_epoch_end(self):

        if self.shuffle:

            np.random.shuffle(
                self.indices
            )


    def cargar(self, ruta):

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


    def __getitem__(self, numero_batch):

        inicio = (
            numero_batch
            * self.batch_size
        )

        fin = min(
            inicio + self.batch_size,
            len(self.df)
        )

        indices_batch = self.indices[
            inicio:fin
        ]

        filas = self.df.iloc[
            indices_batch
        ]

        x1 = []
        x2 = []
        y = []

        for _, fila in filas.iterrows():

            x1.append(
                self.cargar(
                    fila["imagen1"]
                )
            )

            x2.append(
                self.cargar(
                    fila["imagen2"]
                )
            )

            y.append(
                fila["label"]
            )

        return (
            (
                np.asarray(
                    x1,
                    dtype="float32"
                ),
                np.asarray(
                    x2,
                    dtype="float32"
                )
            ),
            np.asarray(
                y,
                dtype="float32"
            )
        )


# ============================================================
# CREAR GENERADORES
# ============================================================

train_generator = ParesSequence(
    df_train,
    batch_size=BATCH_SIZE,
    shuffle=True
)

val_generator = ParesSequence(
    df_val,
    batch_size=BATCH_SIZE,
    shuffle=False
)

test_generator = ParesSequence(
    df_test,
    batch_size=BATCH_SIZE,
    shuffle=False
)


# ============================================================
# MOBILE NET V2
# ============================================================

base_model = MobileNetV2(
    input_shape=(
        TAMANO,
        TAMANO,
        3
    ),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False


# ============================================================
# EXTRACTOR
# ============================================================

entrada = layers.Input(
    shape=(
        TAMANO,
        TAMANO,
        3
    )
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

red_mejorada = Model(
    entrada,
    x,
    name="extractor_128"
)


# ============================================================
# SIAMESE NETWORK
# ============================================================

entrada1 = layers.Input(
    shape=(
        TAMANO,
        TAMANO,
        3
    ),
    name="imagen_1"
)

entrada2 = layers.Input(
    shape=(
        TAMANO,
        TAMANO,
        3
    ),
    name="imagen_2"
)

vector1 = red_mejorada(
    entrada1
)

vector2 = red_mejorada(
    entrada2
)


diferencia = layers.Lambda(
    lambda x: tf.abs(
        x[0] - x[1]
    )
)(
    [vector1, vector2]
)


x = layers.Dense(
    64,
    activation="relu"
)(
    diferencia
)

salida = layers.Dense(
    1,
    activation="sigmoid"
)(
    x
)


modelo = Model(
    inputs=[
        entrada1,
        entrada2
    ],
    outputs=salida
)


# ============================================================
# COMPILAR
# ============================================================

modelo.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.0001
    ),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)


modelo.summary()


# ============================================================
# CALLBACKS
# ============================================================

callbacks = [

    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True
    ),

    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=2,
        min_lr=1e-7
    )

]


# ============================================================
# ENTRENAMIENTO INICIAL
# ============================================================

print()
print("========================================")
print("ENTRENAMIENTO INICIAL")
print("========================================")

historia = modelo.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS_INICIALES,
    callbacks=callbacks
)


# ============================================================
# FINE-TUNING
# ============================================================

print()
print("========================================")
print("FINE-TUNING")
print("========================================")


base_model.trainable = True


for layer in base_model.layers[:-20]:

    layer.trainable = False


for layer in base_model.layers:

    if isinstance(
        layer,
        tf.keras.layers.BatchNormalization
    ):

        layer.trainable = False


modelo.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.00001
    ),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)


historia_finetuning = modelo.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS_FINE_TUNING,
    callbacks=callbacks
)


# ============================================================
# EVALUACIÓN
# ============================================================

print()
print("========================================")
print("EVALUACIÓN")
print("========================================")


resultados = modelo.evaluate(
    test_generator,
    verbose=1
)

print()
print(
    "Loss:",
    resultados[0]
)

print(
    "Accuracy:",
    resultados[1]
)


# ============================================================
# GUARDAR
# ============================================================

modelo.save(
    RUTA_MODELO
)

print()
print(
    "Modelo guardado correctamente:"
)

print(
    RUTA_MODELO
)