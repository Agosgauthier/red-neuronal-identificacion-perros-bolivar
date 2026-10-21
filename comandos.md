# 🛠️ Comandos del Proyecto

## 📌 Descripción

Este archivo contiene los principales comandos utilizados para trabajar con el proyecto de identificación de perros mediante una red neuronal.

Los comandos están organizados según las tareas de configuración, ejecución, entrenamiento, evaluación y control de versiones.

La red neuronal del proyecto se construye y entrena **desde cero, sin redes preentrenadas**.

---

# 🐍 Entorno de Python

## Crear entorno virtual

```bash
python -m venv .venv
```

## Activar entorno virtual en Windows - Git Bash

```bash
source .venv/Scripts/activate
```

## Actualizar pip

```bash
python -m pip install --upgrade pip
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Desactivar entorno virtual

```bash
deactivate
```

---

# 📦 Gestión de Dependencias

## Guardar las dependencias instaladas

```bash
pip freeze > requirements.txt
```

## Instalar una biblioteca

```bash
pip install nombre-paquete
```

Ejemplo:

```bash
pip install tensorflow
```

---

# 🧠 Google Colab

El entrenamiento de la red neuronal se realiza en **Google Colab**, con GPU.

## Activar la GPU

Menú: *Entorno de ejecución → Cambiar tipo de entorno de ejecución → GPU T4 → Guardar*.

## Comprobar que la GPU está activa

```python
import tensorflow as tf

print(tf.config.list_physical_devices("GPU"))
```

Debe mostrar un dispositivo `GPU:0`. Si muestra `[]`, la GPU no está activada.

## Comprobar versión de Python

```python
!python --version
```

## Comprobar versión de TensorFlow

```python
import tensorflow as tf

print(tf.__version__)
```

## Ver archivos del entorno

```python
!ls
```

## Ver estructura de carpetas

```python
!find dataset -maxdepth 3 -type f | head -30
```

**Importante:** Colab borra toda la memoria (variables, dataset y modelo) cuando se reinicia o se desconecta. Hay que volver a ejecutar las celdas de descarga, pares y modelo.

---

# 🗂️ Dataset

## Descargar y extraer el dataset (en Colab)

El dataset YT-BB-Dog se descarga y se descomprime en dos pasos, porque el ZIP contiene otro ZIP adentro:

```python
!wget -q -O "YT-BB-Dog.zip" "https://www.lirmm.fr/YT-BB-Dog_Sibetan/files/YT-BB-dog.zip"
!unzip -q "YT-BB-Dog.zip" -d "dataset"
!unzip -q "dataset/YT-BB-dog/YT-BB-Dog.zip" -d "dataset/perros"
!ls dataset/perros/YT-BB-Dog
```

Debe mostrar las carpetas `test` y `train`.

## Comprobar el archivo descargado

```bash
ls -lh YT-BB-Dog.zip
```

El archivo pesa aproximadamente 583 MB.

## Verificar que el ZIP no esté corrupto

```bash
unzip -t YT-BB-Dog.zip
```

## Contar perros e imágenes

```python
import os
from glob import glob

base = "dataset/perros/YT-BB-Dog"

for parte in ["train", "test"]:
    ruta = os.path.join(base, parte)
    perros = [d for d in os.listdir(ruta) if os.path.isdir(os.path.join(ruta, d))]
    imagenes = glob(os.path.join(ruta, "*", "*.jpg"))
    print(parte, len(perros), "perros", len(imagenes), "imágenes")
```

Resultado esperado:

```text
train: 2.000 perros, 19.932 imágenes
test:    723 perros,  7.104 imágenes
```

---

# 🖼️ Preparación de Imágenes

Las imágenes utilizadas por el modelo se redimensionan a:

```text
128 × 128 píxeles
```

y se transforman a formato RGB.

Los valores de los píxeles se dividen por 255 antes de ingresar al modelo.

```python
import cv2
import numpy as np

TAMANO = 128

def cargar_imagen(ruta):
    imagen = cv2.imread(ruta)
    imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    imagen = cv2.resize(imagen, (TAMANO, TAMANO))
    return imagen.astype("float32") / 255.0
```

---

# 🔗 Creación de Pares

El modelo trabaja con pares de imágenes.

Formato:

```text
imagen1 + imagen2 + label
```

Labels:

```text
1 → mismo perro
0 → perros diferentes
```

Configuración del experimento final:

```text
400 perros → entrenamiento
100 perros → prueba

8.000 pares → entrenamiento (4.000 mismo perro + 4.000 distintos)
2.000 pares → prueba (1.000 mismo perro + 1.000 distintos)

Total: 10.000 pares
```

Se generan con 10 pares del mismo perro por cada perro seleccionado y la misma cantidad de pares de perros distintos.

## Archivos generados

```text
pares/pares_train.csv
pares/pares_test.csv
```

---

# 🧠 Construcción del Modelo (CNN propia)

La red se construye desde cero, sin pesos preentrenados.

```python
import tensorflow as tf
from tensorflow.keras import layers, Model

@tf.keras.utils.register_keras_serializable(package="Perros")
class AbsDifference(layers.Layer):
    def call(self, inputs):
        return tf.abs(inputs[0] - inputs[1])

def bloque(x, filtros):
    x = layers.Conv2D(filtros, 3, padding="same", use_bias=False)(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.MaxPooling2D()(x)
    return x

entrada = layers.Input(shape=(128, 128, 3))
x = layers.RandomFlip("horizontal")(entrada)
x = layers.RandomRotation(0.05)(x)
x = layers.RandomZoom(0.1)(x)

for filtros in [32, 64, 128, 256]:
    x = bloque(x, filtros)

x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.3)(x)
x = layers.Dense(128, activation="relu")(x)

extractor = Model(entrada, x, name="extractor_128")

imagen_1 = layers.Input(shape=(128, 128, 3), name="imagen_1")
imagen_2 = layers.Input(shape=(128, 128, 3), name="imagen_2")

diferencia = AbsDifference(name="diferencia")(
    [extractor(imagen_1), extractor(imagen_2)]
)
x = layers.Dense(64, activation="relu", name="comparacion")(diferencia)
salida = layers.Dense(1, activation="sigmoid", name="salida")(x)

modelo = Model([imagen_1, imagen_2], salida)

modelo.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="binary_crossentropy",
    metrics=["accuracy"],
)

modelo.summary()
```

El resumen debe mostrar 431.073 parámetros en total.

---

# 🏋️ Entrenamiento del Modelo

El entrenamiento se realiza utilizando TensorFlow y Keras, en Google Colab con GPU.

```python
callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=5, restore_best_weights=True
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss", factor=0.5, patience=3, min_lr=1e-6
    ),
]

historia = modelo.fit(
    [X1_train, X2_train],
    y_train,
    validation_split=0.2,
    epochs=40,
    batch_size=32,
    callbacks=callbacks,
)
```

`EarlyStopping` detiene el entrenamiento cuando el modelo deja de mejorar y conserva los mejores pesos. En el entrenamiento final se detuvo en la época 14 y se conservó la época 9.

---

# 📈 Evaluación

Las métricas utilizadas son:

```text
Accuracy
Precision
Recall
F1-score
Matriz de confusión
```

## Evaluar con perros nuevos

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)

predicciones = modelo.predict([X1_test, X2_test]).ravel()
predicciones_clase = (predicciones >= 0.5).astype(int)

print("Accuracy :", accuracy_score(y_test, predicciones_clase))
print("Precision:", precision_score(y_test, predicciones_clase))
print("Recall   :", recall_score(y_test, predicciones_clase))
print("F1-score :", f1_score(y_test, predicciones_clase))
print(confusion_matrix(y_test, predicciones_clase))
```

El umbral por defecto (0,5) no fue el mejor para este modelo, por eso se ajusta con datos de validación.

---

# 🎚️ Ajuste de Umbrales

Los umbrales se eligen con **datos de validación** (los últimos 1.600 pares de entrenamiento), nunca con los datos de prueba.

## Umbral de la salida de la red

```python
X1_val, X2_val, y_val = X1_train[6400:], X2_train[6400:], y_train[6400:]
pred_val = modelo.predict([X1_val, X2_val]).ravel()

mejor_umbral, mejor_f1 = 0.5, 0
for umbral in np.arange(0.05, 0.96, 0.05):
    f1 = f1_score(y_val, (pred_val >= umbral).astype(int))
    if f1 > mejor_f1:
        mejor_umbral, mejor_f1 = umbral, f1

print("Mejor umbral:", mejor_umbral)
```

Resultado del modelo final: **0,15**.

## Umbral de similitud coseno (el que usa la aplicación)

```python
def similitud_coseno(a, b):
    num = np.sum(a * b, axis=1)
    den = np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1)
    return num / np.maximum(den, 1e-9)

sim_val = similitud_coseno(
    extractor.predict(X1_val, verbose=0),
    extractor.predict(X2_val, verbose=0),
)

mejor_umbral, mejor_f1 = 0.5, 0
for umbral in np.arange(0.30, 1.00, 0.01):
    f1 = f1_score(y_val, (sim_val >= umbral).astype(int))
    if f1 > mejor_f1:
        mejor_umbral, mejor_f1 = umbral, f1

print("Mejor umbral de similitud:", mejor_umbral)
```

Resultado del modelo final: **0,90**. Ese valor se configura en `src/app.py`:

```python
UMBRAL_COINCIDENCIA = 0.90
```

**Si se entrena un modelo nuevo, hay que volver a calcular este umbral.**

---

# 🔍 Prueba como Buscador

Mide qué tan seguido queda el perro correcto en los primeros lugares, registrando una foto de cada perro y buscando con otra foto distinta.

```python
galeria = extractor.predict(np.array(galeria_imgs), verbose=0)
consultas = extractor.predict(np.array(consultas_imgs), verbose=0)

def normalizar(m):
    return m / np.maximum(np.linalg.norm(m, axis=1, keepdims=True), 1e-9)

similitudes = normalizar(consultas) @ normalizar(galeria).T
```

Resultado del modelo final con 100 perros del conjunto de prueba:

```text
Primer lugar:          54 de 100
Entre los 3 primeros:  77 de 100
Entre los 5 primeros:  78 de 100
```

---

# 💾 Guardar el Modelo

## Guardar el modelo final

```python
modelo.save(
    "modelo_perros_bolivar_scratch.keras"
)
```

## Comprobar que existe

```python
import os

ruta = "modelo_perros_bolivar_scratch.keras"

print(os.path.exists(ruta))
```

## Ver tamaño del modelo

```python
import os

tamaño = os.path.getsize(
    "modelo_perros_bolivar_scratch.keras"
)

print(
    round(tamaño / (1024 * 1024), 2),
    "MB"
)
```

El modelo final pesa aproximadamente 5 MB.

---

# 📥 Descargar el Modelo desde Google Colab

```python
from google.colab import files

files.download(
    "modelo_perros_bolivar_scratch.keras"
)
```

Después, copiar el archivo a la carpeta `model/` del proyecto.

---

# 📤 Subir el Modelo a Google Colab

Cuando Colab se reinicia hay que volver a cargar el modelo guardado:

```python
import tensorflow as tf
from tensorflow.keras import layers
from google.colab import files

@tf.keras.utils.register_keras_serializable(package="Perros")
class AbsDifference(layers.Layer):
    def call(self, inputs):
        return tf.abs(inputs[0] - inputs[1])

subido = files.upload()
nombre_modelo = list(subido.keys())[0]

modelo = tf.keras.models.load_model(
    nombre_modelo,
    custom_objects={"AbsDifference": AbsDifference},
    safe_mode=False,
    compile=False,
)
extractor = modelo.get_layer("extractor_128")
```

---

# 🚀 Ejecución de la Aplicación

## Ejecutar la aplicación

Con el entorno virtual activado:

```bash
python -m src.app
```

La aplicación estará disponible en:

```text
http://127.0.0.1:7860
```

Para detener la aplicación:

```text
Ctrl + C
```

## Modelo que usa la aplicación

En `src/app.py`, la ruta del modelo y el umbral son:

```python
RUTA_MODELO = (
    BASE_DIR
    / "model"
    / "modelo_perros_bolivar_scratch.keras"
)

UMBRAL_COINCIDENCIA = 0.90
```

## Ejecutar las pruebas

```bash
python -m unittest discover -s tests -v
```

Las pruebas verifican el procesamiento de imágenes y el comportamiento cuando no se cargan las dos imágenes.

---

# 💻 Visual Studio Code

Visual Studio Code se utiliza para organizar y desarrollar el proyecto.

## Abrir el proyecto

Desde Git Bash:

```bash
code .
```

---

# 🌿 Git

## Comprobar estado

```bash
git status
```

## Agregar todos los archivos

```bash
git add .
```

## Crear un commit

```bash
git commit -m "agregar red neuronal propia desde cero y actualizar documentacion"
```

## Subir cambios a GitHub

```bash
git push
```

## Descargar cambios del repositorio

```bash
git pull
```

## Ver historial

```bash
git log --oneline
```

---

# 📂 Estructura del Repositorio

```text
red-neuronal-identificacion-perros-bolivar/
│
├── model/
│   ├── modelo_perros_bolivar_scratch.keras
│   ├── modelo_perros_bolivar_12000_app.keras
│   └── modelo_perros_bolivar_final.keras
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── src/
│
├── tests/
│
├── README.md
├── AGENT.md
├── memoria.md
├── comandos.md
├── Skill.md
└── .gitignore
```

---

# 🔄 Flujo General del Proyecto

```text
1. Activar GPU en Colab
        ↓
2. Descargar y extraer dataset
        ↓
3. Verificar dataset
        ↓
4. Crear pares
        ↓
5. Preparar imágenes
        ↓
6. Construir la CNN propia
        ↓
7. Entrenar
        ↓
8. Evaluar con perros nuevos
        ↓
9. Ajustar umbrales con validación
        ↓
10. Probar como buscador
        ↓
11. Guardar y descargar el modelo
        ↓
12. Integrar en la aplicación
```

---

# ⚠️ Reglas Importantes

- No utilizar datos de prueba durante el entrenamiento.
- No utilizar datos de prueba para elegir umbrales.
- No utilizar redes ni pesos preentrenados en el modelo entregado.
- Verificar el dataset antes de comenzar un entrenamiento.
- Registrar los resultados de cada experimento.
- No sobrescribir un modelo funcional sin comprobar la nueva versión.
- Recalcular el umbral de similitud cuando se entrene un modelo nuevo.
- Mantener actualizada la documentación.
- Utilizar Git para versionar cambios importantes.

---

# 🤖 Uso por parte del Agente

El agente puede utilizar este archivo como referencia para ejecutar tareas relacionadas con:

- Configuración del entorno.
- Preparación de datos.
- Entrenamiento.
- Evaluación.
- Ajuste de umbrales.
- Gestión del modelo.
- Git y GitHub.

Antes de ejecutar un comando destructivo, debe comprobar primero el estado del proyecto.