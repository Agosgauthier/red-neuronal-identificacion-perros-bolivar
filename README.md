# 🐕 Identificación de Perros en Bolívar — Red Neuronal

## Proyecto de Redes Neuronales

**Sistema de comparación de imágenes basado en una red Siamese con CNN propia (sin redes preentrenadas) para identificar posibles coincidencias de un perro perdido entre fotografías candidatas.**

---

# 🎯 Objetivos del Proyecto

1. **Definir un problema de visión por computadora** aplicado a la identificación de perros.
2. **Seleccionar y preparar un dataset adecuado** para entrenar el modelo.
3. **Construir una red neuronal** capaz de comparar dos imágenes.
4. **Entrenar y evaluar diferentes versiones del modelo** utilizando métricas de clasificación.
5. **Aplicar un ciclo de mejora** a partir de los resultados obtenidos.
6. **Guardar el modelo entrenado** para integrarlo en una aplicación.
7. **Desarrollar una aplicación** que permita cargar una fotografía de un perro perdido y buscar posibles coincidencias entre las fotografías candidatas.
8. **Adaptar progresivamente el sistema al contexto de Bolívar**.

---

# 🏗️ Arquitectura

El proyecto utiliza una arquitectura de tipo **Siamese Network**, orientada a comparar dos imágenes y determinar si pertenecen al mismo individuo.

## Tecnologías utilizadas

- Python
- TensorFlow
- Keras
- OpenCV
- NumPy
- Pandas
- Scikit-learn
- Matplotlib
- Gradio
- Google Colab
- Visual Studio Code
- Git
- GitHub

## Funcionamiento

```text
                    ┌──► CNN propia ──► Vector 1 ──┐
📷 Imagen 1 ────────┤                                │
                    │                                ├──► Comparación ──► Resultado
📷 Imagen 2 ────────┤                                │
                    └──► CNN propia ──► Vector 2 ──┘
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

Como extractor de características se construyó una **red convolucional (CNN) propia, creada desde cero**. **No se utilizó ninguna red preentrenada**: todos los pesos parten de valores aleatorios y se aprenden con el dataset del proyecto.

## Extracción de características (`extractor_128`)

```text
Imagen 128 × 128 × 3
   ↓
RandomFlip · RandomRotation · RandomZoom   (solo durante el entrenamiento)
   ↓
Bloque 1:  Conv2D(32)  → BatchNormalization → ReLU → MaxPooling
   ↓
Bloque 2:  Conv2D(64)  → BatchNormalization → ReLU → MaxPooling
   ↓
Bloque 3:  Conv2D(128) → BatchNormalization → ReLU → MaxPooling
   ↓
Bloque 4:  Conv2D(256) → BatchNormalization → ReLU → MaxPooling
   ↓
GlobalAveragePooling2D
   ↓
Dropout(0.3)
   ↓
Dense(128, ReLU)
   ↓
Vector de características (la "huella" del perro)
```

Las dos imágenes utilizan **la misma red con los mismos pesos**, para obtener representaciones comparables.

## Comparación de imágenes

```text
Vector 1 ─────┐
              │
              ├──► Diferencia absoluta (capa AbsDifference)
              │
Vector 2 ─────┘
                       ↓
                Dense(64, ReLU)
                       ↓
                Dense(1, Sigmoid)
                       ↓
              Probabilidad (0 a 1)
```

## Parámetros del modelo

| Parte | Parámetros |
|---|---:|
| `extractor_128` | 422.752 |
| `comparacion` (Dense 64) | 8.256 |
| `salida` (Dense 1) | 65 |
| **Total** | **431.073** |

Entrenables: 430.113. No entrenables: 960 (estadísticas de BatchNormalization).

---

# ⚙️ Proceso de Entrenamiento

Las imágenes fueron redimensionadas a:

```text
128 × 128 píxeles
```

Los valores de los píxeles fueron normalizados dividiéndolos por 255.

## Dataset experimental final

```text
400 perros → entrenamiento
100 perros → prueba

8.000 pares → entrenamiento
2.000 pares → prueba

Total: 10.000 pares de fotografías
```

Los pares fueron balanceados:

```text
50 % → mismo perro
50 % → perros diferentes
```

Los perros del conjunto de prueba **no se usan durante el entrenamiento**. Además, el 20 % de los pares de entrenamiento se reserva como validación.

## Parámetros principales

```text
Tamaño de imagen:        128 × 128
Optimizador:             Adam
Learning rate inicial:   0.001
Función de pérdida:      binary_crossentropy
Batch size:              32
Validación:              20 % del entrenamiento
Épocas máximas:          40
EarlyStopping:           monitorea val_loss, paciencia 5, restaura los mejores pesos
ReduceLROnPlateau:       factor 0.5, paciencia 3, mínimo 1e-6
```

## Resultado del entrenamiento

El entrenamiento se detuvo automáticamente en la época 14 (EarlyStopping). Se conservaron los pesos de la época 9, con 75,94 % de accuracy de validación.

---

# 🔎 Búsqueda de Coincidencias

Para la búsqueda de perros candidatos, la aplicación utiliza el vector de características generado por la capa `extractor_128`.

Se calcula la **similitud coseno** entre la fotografía cargada por el usuario y cada fotografía candidata.

Las fotografías se ordenan de mayor a menor similitud y se muestran las principales coincidencias.

## Límite de similitud

Para evitar presentar como coincidencia una fotografía con una similitud demasiado baja, se estableció un límite de:

```text
0,90 → 90 %
```

Este valor se eligió buscando el mayor F1-score sobre datos de validación (los últimos 1.600 pares del entrenamiento), no sobre los datos de prueba.

Si la mayor similitud encontrada es inferior a este valor, la aplicación informa que no se encontró una coincidencia suficientemente alta.

## Evaluación de la búsqueda por similitud

Se evaluaron los **2.000 pares de prueba** (perros que el modelo nunca vio), con el límite de 0,90:

```text
1.000 pares → mismo perro
1.000 pares → perros diferentes
```

| Métrica | Resultado |
|---|---:|
| **Accuracy** | **87,55 %** |
| **Precision** | **89,24 %** |
| **Recall** | **85,40 %** |
| **F1-score** | **87,28 %** |

```text
[[897 103]
 [146 854]]
```

## Evaluación como buscador

Además de comparar pares, se midió qué tan bien funciona el sistema como buscador. Se tomaron **100 perros del conjunto de prueba**, se registró una fotografía de cada uno y se buscó con **otra fotografía distinta del mismo perro**:

| Posición del perro correcto | Resultado | Al azar sería |
|---|---:|---:|
| Primer lugar | 54 de 100 | 1 |
| Entre los 3 primeros | 77 de 100 | 3 |
| Entre los 5 primeros | 78 de 100 | 5 |

Aclaración: en el dataset, las fotografías de un mismo perro suelen ser muy parecidas entre sí, por lo que con fotografías reales de Bolívar el resultado podría ser menor.

---

# 📈 Evaluación

El modelo fue evaluado utilizando:

- **Accuracy**
- **Precision**
- **Recall**
- **F1-score**
- **Matriz de confusión**

El conjunto de prueba contiene perros que **no fueron utilizados durante el entrenamiento**.

## Clasificador (salida final de la red)

El umbral de decisión por defecto (0,5) no era adecuado para este modelo: casi no daba falsos positivos, pero dejaba pasar más de la mitad de los pares del mismo perro. Se buscó un umbral mejor usando datos de validación.

| Métrica | Umbral 0,5 | Umbral 0,15 |
|---|---:|---:|
| **Accuracy** | 71,85 % | **87,55 %** |
| **Precision** | 98,23 % | 88,20 % |
| **Recall** | 44,50 % | **86,70 %** |
| **F1-score** | 61,25 % | **87,44 %** |

## Matriz de Confusión (umbral 0,15)

```text
[[884 116]
 [133 867]]
```

### Interpretación

```text
884 → perros diferentes correctamente clasificados
116 → perros diferentes clasificados como mismo perro

133 → pares del mismo perro clasificados como diferentes
867 → pares del mismo perro correctamente clasificados
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

La primera versión utilizó una red convolucional creada desde cero (Conv2D 32 → 64 → 128, MaxPooling y Dense 128), entrenada con un conjunto muy pequeño: 16 perros para entrenar y 4 para probar.

Resultado obtenido:

```text
Accuracy: 56,25 %
```

El modelo presentó dificultades para reconocer correctamente los pares correspondientes al mismo perro. Con tan pocos perros, la red no tenía suficientes datos para aprender.

---

# 2️⃣ Experimento de comparación — MobileNetV2

Como experimento se reemplazó la CNN inicial por **MobileNetV2** con pesos preentrenados (transfer learning), y luego se realizó fine-tuning de sus últimas capas.

Resultados obtenidos en ese experimento:

```text
Con MobileNetV2 congelada:   Accuracy 56,25 %   F1-score 58,82 %
Con más datos:               Accuracy 69,25 %   F1-score 68,94 %
Con fine-tuning:             Accuracy 82,15 %   F1-score 82,83 %
Búsqueda por similitud:      Accuracy 87,81 %   F1-score 88,30 %  (1.600 pares)
```

Este experimento se conserva **solo como comparación**. Por la consigna del trabajo, el modelo entregado no utiliza redes preentrenadas. Las pruebas se hicieron con distintos conjuntos de perros y de pares, por lo que los números no son estrictamente comparables con los del modelo final.

---

# 3️⃣ Aumento del Dataset

Se amplió el conjunto experimental utilizando:

```text
400 perros → entrenamiento
100 perros → prueba

8.000 pares → entrenamiento
2.000 pares → prueba
```

El aumento de datos permitió mejorar la capacidad de generalización del modelo.

---

# 4️⃣ Modelo Final — CNN propia mejorada

Se construyó nuevamente una red desde cero, esta vez con:

- 4 bloques de convolución con BatchNormalization.
- Dropout y aumento de datos (volteo, rotación y zoom).
- Un dataset mayor (8.000 pares de entrenamiento).
- Entrenamiento con EarlyStopping y reducción automática del learning rate.
- Ajuste del umbral de decisión con datos de validación.

Resultado final en perros nunca vistos:

```text
Accuracy:  87,55 %
Precision: 89,24 %
Recall:    85,40 %
F1-score:  87,28 %
```

## Evolución del modelo desde cero

```text
56,25 %   (CNN con 16 perros)
   ↓
71,85 %   (CNN mejorada, umbral 0,5)
   ↓
87,55 %   (CNN mejorada, umbral ajustado)
```

---

# 💾 Modelos Entrenados

El proyecto contiene los siguientes modelos:

- `model/modelo_perros_bolivar_scratch.keras`  
  **Modelo final del proyecto.** Red siamesa con CNN propia, sin redes preentrenadas. Es el que utiliza la aplicación: extrae características mediante `extractor_128` y realiza la búsqueda por similitud.

- `experimentos/mobilenet_preentrenado/modelo_perros_bolivar_12000_app.keras` y `experimentos/mobilenet_preentrenado/modelo_perros_bolivar_final.keras`  
  Modelos del experimento de comparación con MobileNetV2.

Todos los modelos utilizan el formato:

```text
.keras
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
- Ajuste del umbral de decisión.
- Evaluación.
- Experimentación con diferentes modelos.
- Exportación de los modelos entrenados.

## Visual Studio Code

Visual Studio Code se utiliza para:

- Organización del proyecto.
- Desarrollo del código.
- Documentación.
- Integración del modelo.
- Desarrollo de la interfaz de búsqueda de coincidencias.
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

red-neuronal-identificacion-perros-bolivar/
│
├── 📂 .github/workflows/
│   └── 📄 ci.yml
│
├── 📂 model/
│   └── 📄 modelo_perros_bolivar_scratch.keras
│
├── 📂 experimentos/
│   └── 📂 mobilenet_preentrenado/    (versión anterior con MobileNetV2, NO es la entrega)
│
├── 📂 data/
│   ├── 📂 candidates/                (fotos candidatas de la galería)
│   ├── 📂 found/                     (fotos de perros encontrados, no se sube a Git)
│   ├── 📂 raw/
│   ├── 📂 processed/
│   └── 📄 perros.db                  (base SQLite, no se sube a Git)
│
├── 📂 notebooks/
│   └── 📄 red_desde_cero_perros.ipynb
│
├── 📂 src/
│   ├── 📄 app.py
│   ├── 📄 db.py
│   ├── 📄 generar_pares.py
│   └── 📄 migrar_json_a_sqlite.py
│
├── 📂 tests/
│   ├── 📄 test_app.py
│   └── 📄 test_db.py
│
├── 📄 README.md
├── 📄 AGENT.md
├── 📄 memoria.md
├── 📄 comandos.md
├── 📄 Skill.md
├── 📄 requirements.txt
└── 📄 .gitignore

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
Gradio
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
Ajuste del umbral
      ↓
Exportación del modelo
```

---

## Flujo de la aplicación

```text
📷 Subir fotografía del perro perdido
        ↓
🧠 Extracción de características
        ↓
🔎 Comparación con fotografías candidatas
        ↓
📊 Cálculo y ordenamiento por similitud
        ↓
┌────────────────────────────┐
│ Resultado                  │
│                            │
│ 🏆 Posibles coincidencias  │
│            o               │
│ ⚠️ Sin coincidencia alta   │
└────────────────────────────┘
```

La aplicación permite cargar una fotografía de un perro perdido y compararla con las fotografías candidatas registradas. Las imágenes se ordenan según su nivel de similitud y se muestran las principales coincidencias. Cuando la mayor similitud no alcanza el límite establecido, el sistema informa que no se encontró una coincidencia suficientemente alta.

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