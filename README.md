# 🐕 Identificación de Perros en Bolívar — Red Neuronal

## Proyecto de Redes Neuronales

**Sistema de comparación de imágenes para determinar si dos fotografías corresponden al mismo perro.**

---

# 🎯 Objetivos del Proyecto

1. **Definir un problema de visión por computadora** aplicado a la identificación de perros.
2. **Seleccionar y preparar un dataset adecuado** para entrenar el modelo.
3. **Construir una red neuronal** capaz de comparar dos imágenes.
4. **Entrenar y evaluar diferentes versiones del modelo** utilizando métricas de clasificación.
5. **Aplicar un ciclo de mejora** a partir de los resultados obtenidos.
6. **Guardar el modelo entrenado** para utilizarlo posteriormente en una aplicación.
7. **Desarrollar una aplicación** que permita cargar dos fotografías y obtener una predicción.
8. **Adaptar progresivamente el sistema al contexto de Bolívar**.

---

# 🏗️ Arquitectura

El proyecto utiliza una arquitectura de tipo **Siamese Network**, orientada a comparar dos imágenes y determinar si pertenecen al mismo individuo.

## Tecnologías utilizadas

- Python
- TensorFlow
- Keras
- MobileNetV2
- OpenCV
- NumPy
- Pandas
- Scikit-learn
- Matplotlib
- Google Colab
- Visual Studio Code
- Git
- GitHub

## Funcionamiento

```text
                    ┌──► MobileNetV2 ──► Vector 1 ──┐
📷 Imagen 1 ────────┤                                │
                    │                                ├──► Comparación ──► Resultado
📷 Imagen 2 ────────┤                                │
                    └──► MobileNetV2 ──► Vector 2 ──┘
```

### Resultado

```text
1 → Mismo perro
0 → Perros diferentes
```

---

# 🗂️ Dataset

Para el desarrollo del proyecto se utiliza el dataset **YT-BB-Dog**.

El dataset utilizado contiene:

- **2.723 perros**
- **27.036 imágenes**

Las imágenes están organizadas mediante identificadores numéricos. Cada identificador representa un perro y contiene diferentes fotografías del mismo individuo.

## Organización del dataset

```text
YT-BB-Dog/
│
├── train/
│   ├── 1760/
│   │   ├── 1760_1.jpg
│   │   ├── 1760_2.jpg
│   │   └── ...
│   │
│   ├── 225/
│   └── ...
│
└── test/
    ├── 2000/
    ├── 2001/
    └── ...
```

---

# 🧠 Modelo de Predicción

Se implementó una **Siamese Network** para comparar dos fotografías.

Como extractor de características se utilizó **MobileNetV2** con pesos preentrenados sobre ImageNet.

Posteriormente se realizó **fine-tuning** sobre las últimas capas de la red para adaptar el modelo al problema específico de identificación de perros.

## Extracción de características

```text
Imagen
   ↓
Rescaling
   ↓
MobileNetV2
   ↓
GlobalAveragePooling2D
   ↓
Dense(128)
   ↓
Vector de características
```

Las dos imágenes utilizan la misma red para obtener representaciones comparables.

## Comparación de imágenes

```text
Vector 1 ─────┐
              │
              ├──► Diferencia absoluta
              │
Vector 2 ─────┘
                       ↓
                   Dense(64)
                       ↓
                    Dense(1)
                       ↓
                    Sigmoid
                       ↓
                  0 o 1
```

---

# ⚙️ Proceso de Entrenamiento

Las imágenes fueron redimensionadas a:

```text
128 × 128 píxeles
```

Los valores de los píxeles fueron normalizados antes de ingresar al modelo.

## Dataset experimental final

```text
100 perros → entrenamiento
20 perros  → prueba

4.000 pares → entrenamiento
800 pares   → prueba
```

Los pares fueron balanceados:

```text
50 % → mismo perro
50 % → perros diferentes
```

## Parámetros principales

```text
Tamaño de imagen:             128 × 128
Batch size:                   32
Learning rate inicial:        0.0001
Learning rate fine-tuning:    0.00001
Épocas iniciales:             10
Épocas fine-tuning:           5
```

---

# 📈 Evaluación

El modelo fue evaluado utilizando:

- **Accuracy**
- **Precision**
- **Recall**
- **F1-score**
- **Matriz de confusión**

El conjunto de prueba contiene perros que **no fueron utilizados durante el entrenamiento**.

## Resultados del modelo final

| Métrica | Resultado |
|---|---:|
| **Accuracy** | **72,13 %** |
| **Precision** | **72,18 %** |
| **Recall** | **72,00 %** |
| **F1-score** | **72,09 %** |

## Matriz de Confusión

```text
[[289 111]
 [112 288]]
```

### Interpretación

```text
289 → perros diferentes correctamente clasificados
111 → perros diferentes clasificados como mismo perro

112 → pares del mismo perro clasificados como diferentes
288 → pares del mismo perro correctamente clasificados
```

---

# 🔄 Feedback Loop — Ciclo de Mejora

Durante el desarrollo se realizaron diferentes iteraciones del modelo siguiendo el proceso:

```text
Entrenamiento
      ↓
Evaluación
      ↓
Detección de problemas
      ↓
Ajuste del modelo / datos
      ↓
Nuevo entrenamiento
      ↓
Nueva evaluación
```

Este proceso permitió comparar diferentes estrategias y mejorar progresivamente el rendimiento del modelo.

---

# 1️⃣ Modelo Inicial — CNN

La primera versión utilizó una red convolucional creada desde cero para analizar las imágenes.

Resultado obtenido:

```text
Accuracy: 56,25 %
```

El modelo presentó dificultades para reconocer correctamente los pares correspondientes al mismo perro.

---

# 2️⃣ Transfer Learning — MobileNetV2

Se reemplazó la CNN inicial por **MobileNetV2** con pesos preentrenados.

La utilización de características visuales previamente aprendidas permitió construir una representación más robusta de las imágenes.

Resultado:

```text
Accuracy: 56,25 %
F1-score: 58,82 %
```

Aunque algunas métricas mejoraron, el rendimiento general todavía no era suficiente.

---

# 3️⃣ Aumento del Dataset

Se amplió el conjunto experimental utilizando:

```text
100 perros → entrenamiento
20 perros  → prueba

4.000 pares → entrenamiento
800 pares   → prueba
```

Resultado:

```text
Accuracy: 69,25 %
F1-score: 68,94 %
```

El aumento de datos permitió mejorar la capacidad de generalización del modelo.

---

# 4️⃣ Fine-tuning

Se descongelaron las últimas capas de MobileNetV2 para permitir que el modelo se adaptara mejor a las características específicas del problema.

Se utilizó un learning rate menor:

```text
0.00001
```

Resultado final:

```text
Accuracy: 72,13 %
Precision: 72,18 %
Recall: 72,00 %
F1-score: 72,09 %
```

## Evolución del modelo

```text
56,25 %
   ↓
69,25 %
   ↓
72,13 %
```

---

# 💾 Modelo Entrenado

El modelo final se encuentra almacenado en:

```text
modelo/modelo_perros_bolivar_final.keras
```

Formato utilizado:

```text
.keras
```

Tamaño aproximado:

```text
9,85 MB
```

---

# 🧪 Entornos de Trabajo

## Google Colab

Google Colab es el entorno utilizado para ejecutar el código relacionado con la red neuronal.

Se utiliza para:

- Preparación del dataset.
- Procesamiento de imágenes.
- Creación de pares.
- Entrenamiento.
- Fine-tuning.
- Evaluación.
- Experimentación con diferentes modelos.
- Exportación del modelo final.

## Visual Studio Code

Visual Studio Code se utiliza para:

- Organización del proyecto.
- Desarrollo del código.
- Documentación.
- Integración del modelo.
- Desarrollo de la futura aplicación.
- Gestión del repositorio Git.

---

# 🤖 Agente de Inteligencia Artificial

El proyecto incluye documentación destinada a facilitar el trabajo autónomo de agentes de inteligencia artificial.

Los archivos relacionados son:

```text
AGENT.md
memoria.md
comandos.md
Skill.md
```

## Objetivo

Permitir que un agente pueda:

- Comprender la estructura del proyecto.
- Conocer el objetivo de la red neuronal.
- Ejecutar los comandos necesarios.
- Mantener información relevante entre interacciones.
- Realizar tareas de forma organizada y reproducible.

---

# 📁 Estructura del Proyecto

```text
red-neuronal-identificacion-perros-bolivar/
│
├── 📂 modelo/
│   └── 📄 modelo_perros_bolivar_final.keras
│
├── 📂 data/
│   ├── 📂 raw/
│   └── 📂 processed/
│
├── 📂 notebooks/
│
├── 📂 src/
│
├── 📂 tests/
│
├── 📄 README.md
├── 📄 AGENT.md
├── 📄 memoria.md
├── 📄 comandos.md
├── 📄 Skill.md
└── 📄 .gitignore
```

---

# 🛠️ Requisitos Previos

Para trabajar con el proyecto se requiere:

- Python 3.10 o superior
- Git
- Visual Studio Code
- Google Colab
- Cuenta de Google para utilizar Google Colab

## Principales bibliotecas

```text
TensorFlow
Keras
OpenCV
NumPy
Pandas
Scikit-learn
Matplotlib
```

---

# 🚀 Puesta en Marcha

## Entrenamiento

El entrenamiento y la evaluación se realizan en **Google Colab**.

El notebook utilizado contiene el proceso de:

```text
Carga del dataset
      ↓
Preparación de imágenes
      ↓
Creación de pares
      ↓
Construcción del modelo
      ↓
Entrenamiento
      ↓
Evaluación
      ↓
Fine-tuning
      ↓
Exportación del modelo
```

---

# 🤖 Trabajo con Agentes

El proyecto incluye archivos de configuración y documentación para facilitar el trabajo de agentes de inteligencia artificial.

```text
AGENT.md
memoria.md
comandos.md
Skill.md
```

Estos archivos permiten documentar:

- Contexto del proyecto.
- Objetivos.
- Comandos de ejecución.
- Estructura del repositorio.
- Procedimientos de trabajo.
- Habilidades y tareas disponibles para el agente.

---

# 📌 Estado Actual del Proyecto

## ✅ Completado

- [x] Definición del problema.
- [x] Selección del dataset.
- [x] Descarga del dataset.
- [x] Validación del dataset.
- [x] Extracción del dataset.
- [x] Exploración de imágenes.
- [x] Preparación de los datos.
- [x] Creación de pares positivos y negativos.
- [x] Construcción de una CNN inicial.
- [x] Evaluación de la primera versión.
- [x] Implementación de MobileNetV2.
- [x] Aumento del conjunto experimental.
- [x] Fine-tuning.
- [x] Evaluación del modelo final.
- [x] Exportación del modelo.
- [x] Creación del repositorio GitHub.
- [x] Creación de la estructura base del proyecto.
- [x] Incorporación del modelo entrenado al repositorio.

## 🚧 Pendiente

- [ ] Crear la interfaz de usuario.
- [ ] Permitir cargar dos fotografías.
- [ ] Procesar ambas imágenes mediante el modelo.
- [ ] Mostrar el resultado de la comparación.
- [ ] Realizar pruebas con fotografías externas al dataset.
- [ ] Mejorar el rendimiento del modelo.
- [ ] Incorporar nuevos datos de entrenamiento.
- [ ] Realizar nuevas iteraciones del feedback loop.
- [ ] Adaptar el sistema al contexto específico de Bolívar.

---

# 🎯 Próximo Objetivo

El próximo objetivo es integrar el modelo entrenado en una aplicación capaz de recibir dos fotografías y realizar automáticamente la comparación.

## Flujo esperado

```text
📷 Subir imagen 1
        +
📷 Subir imagen 2
        ↓
🧠 Red neuronal
        ↓
   Comparación
        ↓
┌────────────────────────┐
│ Resultado              │
│                        │
│ ✅ Mismo perro         │
│        o               │
│ ❌ Perros diferentes   │
└────────────────────────┘
```

A partir de esta funcionalidad se buscará evolucionar el MVP hacia un sistema de identificación y re-identificación de perros aplicable al contexto de **Bolívar**.

---

# 📚 Documentación del Proyecto

| Archivo | Descripción |
|---|---|
| `README.md` | Documentación general del proyecto |
| `AGENT.md` | Información e instrucciones para el agente de IA |
| `memoria.md` | Información relevante para futuras interacciones |
| `comandos.md` | Comandos necesarios para trabajar con el proyecto |
| `Skill.md` | Habilidades y procedimientos disponibles para el agente |

---

# 🐕 Identificación de Perros en Bolívar

## Proyecto de Redes Neuronales

**Computer Vision · Deep Learning · TensorFlow · Keras**