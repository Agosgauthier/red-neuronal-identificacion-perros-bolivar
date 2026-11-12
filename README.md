# 🐕 Identificación de Perros en Bolívar — Red Neuronal

## Proyecto de Redes Neuronales
**Sistema de comparación de imágenes basado en una red siamesa con CNN propia (sin redes preentrenadas): la misma CNN convierte cada foto en un vector y una capa de comparación calcula la probabilidad de que las dos fotos sean del mismo perro. La aplicación usa un umbral elegido con datos de validación para identificar posibles coincidencias de un perro perdido entre fotografías candidatas. El modelo D, entrenado con pérdida de trillizos, se conserva como un experimento posterior y no es el modelo final.**

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

El proyecto utiliza una **Siamese Network** con una **CNN propia, creada y entrenada desde cero**. Cada foto pasa por la misma CNN, con los mismos pesos, y se obtiene un vector de 128 números. Después se calcula la diferencia absoluta entre los dos vectores y dos capas Dense (una de 64 neuronas con ReLU y otra de 1 neurona con sigmoide) devuelven la probabilidad de que las dos fotos sean del mismo perro. La aplicación considera que hay coincidencia cuando esa probabilidad supera el umbral de 0,25, elegido con datos de validación. El modelo D, que se entrena con pérdida de trillizos y compara por similitud coseno, se probó después como experimento y no es el modelo final.

El diagrama de abajo muestra el funcionamiento general: las dos imágenes pasan por la misma red y se comparan.

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

# 🏆 Modelo Final — Red siamesa con CNN propia (scratch)

> Es el modelo que usa la aplicación (`model/modelo_perros_bolivar_scratch.keras`). Las secciones siguientes, hasta "Feedback Loop", lo describen: arquitectura, entrenamiento, umbral y resultados.

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

## Dataset utilizado

```text
400 perros → entrenamiento
100 perros → validación
100 perros → prueba

8.000 pares → entrenamiento
2.000 pares → validación
2.000 pares → prueba

Total: 12.000 pares de fotografías
```
Los perros de validación y de prueba **no se usan durante el entrenamiento**.

## Parámetros principales

```text
Tamaño de imagen:        128 × 128
Optimizador:             Adam
Learning rate inicial:   0.001
Función de pérdida:      binary_crossentropy
Batch size:              32
Validación:              100 perros distintos (2.000 pares)
Épocas máximas:          40
EarlyStopping:           monitorea val_loss, paciencia 5, restaura los mejores pesos
ReduceLROnPlateau:       factor 0.5, paciencia 3, mínimo 1e-6
```

## Resultado del entrenamiento

El entrenamiento se detuvo automáticamente en la época 30 (EarlyStopping). Se conservaron los pesos de la época 25, con 87,75 % de accuracy de validación.

---

# 🔎 Búsqueda de Coincidencias

Para buscar un perro, la aplicación pasa la fotografía cargada y cada fotografía candidata por la red siamesa, que devuelve la probabilidad (de 0 a 1) de que sean el mismo perro.

Las fotografías se ordenan de mayor a menor probabilidad y se muestran las 5 principales que superan el umbral.

## Umbral de decisión

```text
0,25 → 25 %
```

Este valor se eligió buscando el mayor F1-score sobre datos de validación (F1 de validación: 0,8915; 2.000 pares de otros 100 perros), no sobre los datos de prueba. Con este umbral sube el recall (93 %): se pierden menos perros correctos, a costa de mostrar algunos candidatos de más.

Si la mayor probabilidad encontrada es inferior al umbral, la aplicación informa que no se encontró una coincidencia suficientemente alta.

## Alternativa evaluada: similitud coseno (umbral 0,90)

Además de la salida de la red, se probó comparar los vectores de la CNN con similitud coseno. Esta alternativa dio los resultados siguientes, pero no es la que usa la aplicación.

Se evaluaron los **2.000 pares de prueba** (perros que el modelo nunca vio), con el límite de 0,90:

```text
1.000 pares → mismo perro
1.000 pares → perros diferentes
```

| Métrica | Resultado |
|---|---:|
| **Accuracy** | **90,80 %** |
| **Precision** | **91,21 %** |
| **Recall** | **90,30 %** |
| **F1-score** | **90,75 %** |


```text
[[913  87]
 [ 97 903]]
```

## Evaluación como buscador

(Medido con similitud coseno entre los vectores de la CNN.)

Además de comparar pares, se midió qué tan bien funciona el sistema como buscador. Se tomaron **100 perros del conjunto de prueba**, se registró una fotografía de cada uno y se buscó con **otra fotografía distinta del mismo perro**:

| Posición del perro correcto | Resultado | Al azar sería |
|---|---:|---:|
| Primer lugar | 60 de 100 | 1 |
| Entre los 3 primeros | 80 de 100 | 3 |
| Entre los 5 primeros | 83 de 100 | 5 |

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

La aplicación usa la salida de la red con el umbral de 0,25, elegido con datos de validación (el que da el mayor F1 en validación). Comparado con el umbral por defecto (0,5), sube el recall pero la accuracy en prueba baja un poco.

| Métrica | Umbral 0,5 | Umbral 0,25 |
|---|---:|---:|
| **Accuracy** | **89,95 %** | 88,55 % |
| **Precision** | **93,00 %** | 85,40 % |
| **Recall** | 86,40 % | **93,00 %** |
| **F1-score** | **89,58 %** | 89,04 % |

## Matriz de Confusión (umbral 0,25)

```text
[[841 159]

 [ 70 930]]
```

### Interpretación

```text
841 → perros diferentes correctamente clasificados
159 → perros diferentes clasificados como mismo perro

70 → pares del mismo perro clasificados como diferentes
930 → pares del mismo perro correctamente clasificados
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
100 perros → validación
100 perros → prueba

8.000 pares → entrenamiento
2.000 pares → validación
2.000 pares → prueba
```

El aumento de datos permitió mejorar la capacidad de generalización del modelo.

---

# 4️⃣ CNN propia siamesa mejorada (modelo final)

Se construyó nuevamente una red desde cero, esta vez con:

- 4 bloques de convolución con BatchNormalization.
- Dropout y aumento de datos (volteo, rotación y zoom).
- Un dataset mayor (8.000 pares de entrenamiento).
- Entrenamiento con EarlyStopping y reducción automática del learning rate.
- Ajuste del umbral de decisión con datos de validación.

Resultados en perros nunca vistos (2.000 pares de prueba), según cómo se decida:

```text
Salida de la red, umbral 0,25 (la que usa la app):  Accuracy 88,55 % | Precision 85,40 % | Recall 93,00 % | F1 89,04 %
Similitud coseno, umbral 0,90 (alternativa):        Accuracy 90,80 % | Precision 91,21 % | Recall 90,30 % | F1 90,75 %
```

## Evolución del modelo desde cero

Después de este modelo se probaron las configuraciones A, B y C (más perros y distinto learning rate), que no mejoraron de forma confiable. Luego, en la configuración D, se entrenó el extractor directamente con pérdida de trillizos, para que las fotos del mismo perro queden cerca y las de perros distintos queden lejos.

Un intento de centrar los vectores (restarles la media) empeoró el resultado (F1 de validación 0,73 y 48 de 100 como buscador), por lo que se descartó.

```text
56,25 %   (CNN con 16 perros)
   ↓
89,95 %   (CNN mejorada, umbral 0,5)
   ↓
90,80 %   (CNN mejorada, similitud coseno)
   ↓
88,55 %   (CNN mejorada, umbral 0,25 elegido en validación: modelo final de la app)
   ↓
87,85 %   (experimento D con trillizos; no es el modelo final)
```
---

# 🔬 Experimento posterior: Modelo D — Extractor con pérdida de trillizos

Es un experimento que se hizo después de la red siamesa (`model/extractor_D_trillizos.keras`). **No es el modelo final ni el que usa la aplicación.** Es una CNN propia, creada y entrenada desde cero, sin redes preentrenadas. Es solo el extractor: convierte cada foto en un vector de 128 números y dos fotos se comparan con la similitud coseno.

## Entrenamiento

```text
Pérdida:            trillizos (triplet loss), margen 0,3
Tanda:              16 perros x 4 fotos = 64 imágenes
Optimizador:        Adam, learning rate 0,001
Épocas:             30 (100 pasos por época)
Aumento de datos:   RandomFlip, RandomRotation, RandomZoom, RandomBrightness
```

## Umbral

```text
Umbral de coseno:   0,999876 (elegido en validación)
F1 en validación:   0,9064
```
Si este modelo se configura en `RUTA_MODELO`, la aplicación reescala el coseno con una sigmoide (`CENTRO_COSENO` y `ESCALA_COSENO` en `src/config.py`). Esas constantes solo se usan con este tipo de modelo y no afectan a la red siamesa.

## Resultados con perros que el modelo nunca vio

```text
Pares de prueba:       Accuracy 87,85 % | F1-score 87,78 %
Buscador (100 perros): primero 70 | entre los 3 primeros 81 | entre los 5 primeros 85
```
---

# 💾 Modelos Entrenados

El proyecto contiene los siguientes modelos:

- `model/modelo_perros_bolivar_scratch.keras`  
  **Modelo final del proyecto.** Red siamesa con CNN propia, creada y entrenada desde cero, sin redes preentrenadas. Es el que utiliza la aplicación: devuelve la probabilidad de que dos fotos sean del mismo perro y se aplica el umbral de 0,25.

- `model/extractor_D_trillizos.keras`  
  Experimento posterior: extractor entrenado con pérdida de trillizos, que compara por similitud coseno. Se conserva como comparación.

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

# 🗄️ Base de Datos

Los perros encontrados se registran en una base de datos **SQLite** local (`data/perros.db`), en la tabla `perros_encontrados`:

| Campo | Contenido |
|---|---|
| `id` | Identificador del registro (automático) |
| `imagen` | Nombre del archivo de la fotografía guardada en `data/found/` |
| `zona` | Lugar donde se encontró el perro |
| `fecha` | Fecha en la que se encontró |
| `descripcion` | Descripción opcional |
| `contacto` | Medio de contacto de quien lo encontró |
| `fecha_registro` | Fecha y hora del registro en la aplicación |

La clase `PerrosRepository` (`src/services/perros_repository.py`) ofrece `registrar()`, `obtener_por_imagen()` y `listar()`. La aplicación crea la base automáticamente la primera vez que se registra un perro.

La base de datos y las fotografías de `data/found/` **no se suben a GitHub** (están en el `.gitignore`), porque contienen datos de contacto de personas. Si existiera un archivo `data/found/datos.json` de una versión anterior, sus registros se pasan a SQLite con:

```bash
python -m scripts.migrar_json_a_sqlite
```

---

# 🧪 Experimentos Previos (MobileNetV2)

La carpeta `experimentos/mobilenet_preentrenado/` guarda una versión anterior del proyecto basada en **MobileNetV2 preentrenada** (transfer learning), con sus scripts, su notebook y sus modelos.

Se conserva únicamente como comparación. **No forma parte de la entrega**: el modelo entregado es una CNN propia, creada y entrenada desde cero, sin redes preentrenadas (`model/modelo_perros_bolivar_scratch.keras`, notebook `notebooks/red_desde_cero_perros.ipynb`).

---

# ▶️ Cómo Ejecutar la Aplicación

Desde la raíz del proyecto, con el entorno virtual activado:

```bash
pip install -r requirements.txt
python main.py
```

La aplicación se abre en `http://127.0.0.1:7860`. 

Para correr las pruebas:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

---

# 📁 Estructura del Proyecto

```text
red-neuronal-identificacion-perros-bolivar/
│
├── 📂 .github/workflows/
│   └── 📄 ci.yml
│
├── 📂 model/
│   ├── 📄 modelo_perros_bolivar_scratch.keras  (modelo final, el que usa la app)
│   └── 📄 extractor_D_trillizos.keras   (experimento con trillizos, comparación)
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
├── 📄 main.py                    (solo arranca la app)
│
├── 📂 src/
│   ├── 📄 config.py              (rutas y umbral)
│   ├── 📂 models/                (clases de datos)
│   ├── 📂 services/              (toda la lógica, en clases)
│   │   ├── 📄 modelo_service.py
│   │   ├── 📄 buscador_service.py
│   │   ├── 📄 perros_repository.py
│   │   ├── 📄 dataset_service.py
│   │   ├── 📄 evaluacion_service.py
│   │   └── 📄 entrenamiento_service.py
│   ├── 📂 controllers/           (conecta la vista con los services)
│   └── 📂 views/                 (interfaz Gradio, HTML y CSS)
│
├── 📂 scripts/
│   └── 📄 migrar_json_a_sqlite.py
│
├── 📂 tests/
│   ├── 📄 test_modelo_service.py
│   ├── 📄 test_buscador_service.py
│   ├── 📄 test_repository.py
│   ├── 📄 test_controller.py
│   └── 📄 test_dataset_y_evaluacion.py
│
├── 📄 README.md
├── 📄 AGENT.md
├── 📄 memoria.md
├── 📄 comandos.md
├── 📄 Skill.md
├── 📄 requirements.txt
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
🧠 Red siamesa: probabilidad de "mismo perro"
        ↓
🔎 Se repite con cada fotografía candidata
        ↓
📊 Orden por probabilidad y umbral de 0,25
        ↓
┌────────────────────────────┐
│ Resultado                  │
│                            │
│ 🏆 Posibles coincidencias  │
│            o               │
│ ⚠️ Sin coincidencia alta   │
└────────────────────────────┘
```

La aplicación permite cargar una fotografía de un perro perdido y compararla con las fotografías candidatas registradas. Las imágenes se ordenan según la probabilidad que devuelve la red y se muestran las principales que superan el umbral de 0,25. Cuando la mayor probabilidad no alcanza ese umbral, el sistema informa que no se encontró una coincidencia suficientemente alta.

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

## Resultados del modelo

El modelo final es `modelo_perros_bolivar_scratch.keras`: una red siamesa con CNN propia, creada y entrenada desde cero (sin redes preentrenadas). Devuelve la probabilidad de que dos fotos sean del mismo perro, y la aplicación usa un umbral de 0,25 elegido con datos de validación.

### Métricas

| Medida | Resultado |
|---|---|
| F1 en validación (donde se eligió el umbral) | 0,8915 |
| Accuracy en prueba | 88,55 % |
| Precision en prueba | 85,40 % |
| Recall en prueba | 93,00 % |
| F1 en prueba | 89,04 % |

El umbral se eligió en validación y recién después se midió en prueba, así que los números de prueba son honestos.

### Comparación de modelos: ¿cuál es mejor y cuál conviene?

| Modelo | ¿Desde cero? | Accuracy en prueba | F1 en prueba | Buscador: correcto primero (de 100) |
|---|:---:|---:|---:|---:|
| CNN inicial (16 perros) | Sí | 56,25 % | — | — |
| MobileNetV2 con fine-tuning | **No** (preentrenada) | 82,15 % | 82,83 % | — |
| **Siamesa propia, salida de la red, umbral 0,25 (final)** | **Sí** | **88,55 %** | **89,04 %** | 60 (con coseno) |
| Siamesa propia, similitud coseno (alternativa) | Sí | 90,80 % | 90,75 % | 60 |
| Configuraciones A, B y C (más perros, otro learning rate) | Sí | 78,6 % – 82,1 % | — | 32 – 37 |
| D: extractor con pérdida de trillizos (experimento) | Sí | 87,85 % | 87,78 % | 70 |

Las pruebas usaron distintos conjuntos de perros y de pares, así que los números no son estrictamente comparables.

**Conclusión:** el modelo que más conviene es la **red siamesa scratch**, usada con la salida de la red y un umbral de 0,25 elegido en validación. Tiene mejor accuracy y F1 que el modelo D (88,55 % y 89,04 % contra 87,85 % y 87,78 %), y su entrenamiento es estable: EarlyStopping, reducción del learning rate y curva de validación. El modelo D fue mejor como buscador en una prueba de 100 consultas (70 de 100 primeros contra 60), pero esa diferencia no es enorme y su pérdida quedó estancada en el valor del margen (0,30), lo que indica que separa poco a los perros distintos. Ambos modelos cumplen la consigna de ser redes creadas y entrenadas desde cero. MobileNetV2 se probó solo como comparación y no forma parte de la entrega. Las configuraciones A, B y C no mejoraron de forma confiable, porque cada entrenamiento arranca con pesos aleatorios distintos.

### Límites conocidos

- La probabilidad de la red es una estimación y no confirma por sí sola la identidad del perro.
- Con el umbral de 0,25 se prioriza el recall: pueden aparecer como posible coincidencia perros distintos con puntajes bajos.
- Con fotos difíciles (el perro ocupa poco espacio o aparecen personas en la imagen), la búsqueda es menos precisa.
- En el dataset, las fotos de un mismo perro se parecen mucho entre sí; con fotos reales de Bolívar el resultado podría ser menor.
- El resultado de buscador (60 de 100) se midió con similitud coseno entre vectores, no con la salida de la red que usa la aplicación.
- En el experimento D, la pérdida de trillizos se estabilizó cerca de 0,30, que es el valor del margen. Mejorarlo es un posible próximo paso.