from pathlib import Path
import random
import pandas as pd


random.seed(42)

# Proyecto
PROYECTO = Path(__file__).resolve().parents[1]

# Dataset
TRAIN_PATH = PROYECTO / "dataset" / "perros" / "YT-BB-Dog" / "train"
TEST_PATH = PROYECTO / "dataset" / "perros" / "YT-BB-Dog" / "test"


def obtener_perros(ruta):
    perros = []

    for carpeta in ruta.iterdir():
        if not carpeta.is_dir():
            continue

        imagenes = list(carpeta.glob("*.jpg"))

        if len(imagenes) >= 2:
            perros.append((carpeta.name, imagenes))

    return perros


def par_mismo_perro(imagenes):
    img1, img2 = random.sample(imagenes, 2)

    return {
        "imagen1": str(img1),
        "imagen2": str(img2),
        "label": 1
    }


def par_diferente_perro(perros):
    perro1, imagenes1 = random.choice(perros)
    perro2, imagenes2 = random.choice(perros)

    while perro1 == perro2:
        perro2, imagenes2 = random.choice(perros)

    return {
        "imagen1": str(random.choice(imagenes1)),
        "imagen2": str(random.choice(imagenes2)),
        "label": 0
    }


def crear_dataset(perros, pares_por_perro):
    positivos = []

    for perro, imagenes in perros:
        for _ in range(pares_por_perro):
            positivos.append(par_mismo_perro(imagenes))

    negativos = [
        par_diferente_perro(perros)
        for _ in range(len(positivos))
    ]

    pares = positivos + negativos

    random.shuffle(pares)

    return pd.DataFrame(pares)


# ---------------------------------------
# Cargar perros
# ---------------------------------------

todos_train = obtener_perros(TRAIN_PATH)
todos_test = obtener_perros(TEST_PATH)

print("Perros disponibles en train:", len(todos_train))
print("Perros disponibles en test:", len(todos_test))


# ---------------------------------------
# Seleccionar perros
# ---------------------------------------

perros_train = random.sample(todos_train, 100)
perros_test = random.sample(todos_test, 20)


# ---------------------------------------
# Crear datasets
# ---------------------------------------

df_train = crear_dataset(
    perros_train,
    pares_por_perro=60
)

df_test = crear_dataset(
    perros_test,
    pares_por_perro=40
)


# ---------------------------------------
# Guardar
# ---------------------------------------

df_train.to_csv(
    PROYECTO / "dataset" / "pares_train_grande.csv",
    index=False
)

df_test.to_csv(
    PROYECTO / "dataset" / "pares_test_grande.csv",
    index=False
)


# ---------------------------------------
# Mostrar resultado
# ---------------------------------------

print()
print("========== ENTRENAMIENTO ==========")
print("Total:", len(df_train))
print("Mismo perro:", int((df_train["label"] == 1).sum()))
print("Diferentes:", int((df_train["label"] == 0).sum()))

print()
print("========== PRUEBA ==========")
print("Total:", len(df_test))
print("Mismo perro:", int((df_test["label"] == 1).sum()))
print("Diferentes:", int((df_test["label"] == 0).sum()))

print()
print("CSV generados correctamente.")