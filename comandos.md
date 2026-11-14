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

# 🏋️ Entrenamiento y Evaluación

El entrenamiento se ejecuta desde la raíz del proyecto, con el entorno virtual activado. `entrenar.py` solo arranca la clase `AplicacionEntrenamiento`: la lógica está en `src/services/` y el orden de los pasos lo dirige `EntrenamientoController`.

## Entrenar descargando el dataset YT-BB-Dog

```bash
python entrenar.py --descargar
```

## Prueba rápida (1 época)

```bash
python entrenar.py --epocas 1
```

## Qué hace el entrenamiento

```text
1. Dataset: arma los pares de entrenamiento, validación y prueba
2 y 3. Modelo: red siamesa con CNN propia, configurada
4. Entrena
5. Prueba con perros que la red nunca vio
```

El umbral se elige con los datos de validación (nunca con los de prueba) y el resultado se muestra en la consola.

## Dónde se guarda el modelo

El modelo entrenado sale con otro nombre, para no pisar el que usa la aplicación:

```text
model/modelo_perros_bolivar_scratch_nuevo.keras
```

Antes de reemplazar el modelo de la app hay que comprobar sus métricas, actualizar `UMBRAL_COINCIDENCIA` en `src/config.py` con el umbral nuevo y recién después renombrar el archivo.

## Entrenar en Google Colab (si hace falta GPU)

Menú: *Entorno de ejecución → Cambiar tipo de entorno de ejecución → GPU T4 → Guardar*. Después, clonar el repositorio y ejecutar los mismos comandos:

```python
!git clone https://github.com/Agosgauthier/red-neuronal-identificacion-perros-bolivar.git
%cd red-neuronal-identificacion-perros-bolivar
!pip install -r requirements.txt
!python entrenar.py --descargar
```

Para bajar el modelo entrenado y copiarlo a la carpeta `model/` del proyecto:

```python
from google.colab import files

files.download("model/modelo_perros_bolivar_scratch_nuevo.keras")
```

Colab borra todo cuando se reinicia o se desconecta, así que hay que descargar el modelo antes de cerrar la sesión.

---

# 🚀 Ejecución de la Aplicación

## Ejecutar la aplicación

Con el entorno virtual activado:

```bash
python main.py
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

En `src/config.py`, la ruta del modelo y el umbral son:

```python
RUTA_MODELO = BASE_DIR / "model" / "modelo_perros_bolivar_scratch.keras"

UMBRAL_COINCIDENCIA = 0.25     # sobre la probabilidad que devuelve la red
```

`CENTRO_COSENO` y `ESCALA_COSENO` solo se usan con el modelo D (experimento).

## Ejecutar las pruebas

```bash
python -m unittest discover -s tests -v
```

Las pruebas verifican los services, los controllers, las vistas y el repository, sin necesidad de cargar TensorFlow.

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
├── .github/workflows/
│   └── ci.yml
│
├── model/
│   ├── modelo_perros_bolivar_scratch.keras   (modelo final, el que usa la app)
│   └── extractor_D_trillizos.keras   (experimento con trillizos, comparación)
│
├── data/
│   ├── candidates/                (fotos candidatas de la galería)
│   ├── found/                     (fotos de perros encontrados, no se sube a Git)
│   ├── raw/
│   ├── processed/
│   └── perros.db                  (base SQLite, no se sube a Git)
│
├── main.py                       (solo arranca la app web)
├── entrenar.py                   (solo arranca el entrenamiento)
│
├── src/
│   ├── config.py                 (rutas y umbral)
│   ├── aplicacion_web.py         (arma las piezas y lanza la app)
│   ├── aplicacion_entrenamiento.py (arma las piezas y entrena)
│   ├── domain/                   (entidades, una clase por archivo)
│   ├── repositories/             (acceso a la base de datos)
│   ├── services/                 (toda la lógica, en clases)
│   ├── controllers/              (conecta la vista con los services)
│   └── views/                    (interfaz Gradio, consola, HTML y CSS)
│
├── scripts/
│   ├── diagnostico_ranking.py
│   └── migrar_json_a_sqlite.py
│
├── tests/                        (pruebas unitarias)
│
├── README.md
├── AGENT.md
├── memoria.md
├── comandos.md
├── Skill.md
├── requirements.txt
└── .gitignore
```

---

# 🔄 Flujo General del Proyecto

```text
1. Activar el entorno virtual e instalar dependencias
        ↓
2. python entrenar.py --descargar
   (dataset → pares → modelo → entrenamiento → prueba)
        ↓
3. Revisar las métricas y el umbral elegido con validación
        ↓
4. Actualizar UMBRAL_COINCIDENCIA en src/config.py
        ↓
5. Reemplazar el modelo de la app (model/modelo_perros_bolivar_scratch.keras)
        ↓
6. python main.py
        ↓
7. Correr las pruebas, hacer commit y push a develop
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