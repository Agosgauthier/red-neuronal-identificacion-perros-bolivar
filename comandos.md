# 🛠️ Comandos del Proyecto

## 📌 Descripción

Este archivo contiene los principales comandos utilizados para trabajar con el proyecto de identificación de perros mediante una red neuronal.

Los comandos están organizados según las tareas de configuración, ejecución, entrenamiento, evaluación y control de versiones.

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

El entrenamiento de la red neuronal se realiza en **Google Colab**.

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

---

# 🗂️ Dataset

## Descargar el dataset

El dataset YT-BB-Dog puede descargarse directamente desde su fuente mediante:

```bash
wget -O "YT-BB-Dog.zip" "https://www.lirmm.fr/YT-BB-Dog_Sibetan/files/YT-BB-dog.zip"
```

## Comprobar el archivo descargado

```bash
ls -lh YT-BB-Dog.zip
```

## Verificar que el ZIP no esté corrupto

```bash
unzip -t YT-BB-Dog.zip
```

## Extraer el archivo

```bash
unzip -q YT-BB-Dog.zip -d dataset
```

## Ver archivos del dataset

```bash
find dataset -type f | head -30
```

---

# 🖼️ Preparación de Imágenes

Las imágenes utilizadas por el modelo se redimensionan a:

```text
128 × 128 píxeles
```

y se transforman a formato RGB.

Los valores de los píxeles se normalizan antes de ingresar al modelo.

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

## Archivos generados

```text
dataset/pares_train.csv
dataset/pares_test.csv
```

y para el experimento ampliado:

```text
dataset/pares_train_grande.csv
dataset/pares_test_grande.csv
```

---

# 🧠 Entrenamiento del Modelo

El entrenamiento se realiza utilizando TensorFlow y Keras.

## Entrenar el modelo

El proceso se ejecuta desde Google Colab utilizando el código definido en el notebook.

Ejemplo general:

```python
modelo.fit(
    [X1_train, X2_train],
    y_train,
    validation_split=0.2,
    epochs=10,
    batch_size=32,
    shuffle=True
)
```

---

# 🔬 Fine-tuning

Para adaptar MobileNetV2 al problema específico se habilitan las últimas capas de la red.

Se utiliza un learning rate reducido:

```text
0.00001
```

Ejemplo:

```python
modelo.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.00001
    ),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)
```

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

Las predicciones se convierten en clases utilizando un umbral de:

```text
0.5
```

Ejemplo:

```python
predicciones_clase = (
    predicciones >= 0.5
).astype(int)
```

---

# 💾 Guardar el Modelo

## Guardar el modelo final

```python
modelo.save(
    "modelo_perros_bolivar_final.keras"
)
```

## Comprobar que existe

```python
import os

ruta = "modelo_perros_bolivar_final.keras"

print(os.path.exists(ruta))
```

## Ver tamaño del modelo

```python
import os

tamaño = os.path.getsize(
    "modelo_perros_bolivar_final.keras"
)

print(
    round(tamaño / (1024 * 1024), 2),
    "MB"
)
```

---

# 📥 Descargar el Modelo desde Google Colab

```python
from google.colab import files

files.download(
    "modelo_perros_bolivar_final.keras"
)
```
---
# 🚀 Ejecución de la Aplicación

## Ejecutar la aplicación

Con el entorno virtual activado:

```bash
python src/app.py
```

La aplicación estará disponible en:

```text
http://127.0.0.1:7860
```

Para detener la aplicación:

```text
Ctrl + C
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
git commit -m "agregar modelo y documentacion inicial"
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
1. Descargar dataset
        ↓
2. Validar dataset
        ↓
3. Extraer imágenes
        ↓
4. Preparar imágenes
        ↓
5. Crear pares
        ↓
6. Construir modelo
        ↓
7. Entrenar
        ↓
8. Evaluar
        ↓
9. Analizar resultados
        ↓
10. Mejorar modelo
        ↓
11. Fine-tuning
        ↓
12. Evaluar nuevamente
        ↓
13. Guardar modelo
        ↓
14. Integrar en la aplicación
```

---

# ⚠️ Reglas Importantes

- No utilizar datos de prueba durante el entrenamiento.
- Verificar el dataset antes de comenzar un entrenamiento.
- Registrar los resultados de cada experimento.
- No sobrescribir un modelo funcional sin comprobar la nueva versión.
- Mantener actualizada la documentación.
- Utilizar Git para versionar cambios importantes.

---

# 🤖 Uso por parte del Agente

El agente puede utilizar este archivo como referencia para ejecutar tareas relacionadas con:

- Configuración del entorno.
- Preparación de datos.
- Entrenamiento.
- Evaluación.
- Fine-tuning.
- Gestión del modelo.
- Git y GitHub.

Antes de ejecutar un comando destructivo, debe comprobar primero el estado del proyecto.
