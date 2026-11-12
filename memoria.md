# 🧠 Memoria del Proyecto — Identificación de Perros en Bolívar

## 📌 Información General

**Nombre del proyecto:** Identificación de Perros en Bolívar — Red Neuronal

**Materia:** Redes Neuronales

**Tipo de proyecto:** Visión por computadora / Deep Learning

**Objetivo principal:** comparar dos imágenes de perros y determinar si corresponden al mismo perro o a perros diferentes.

**Consigna importante:** la red neuronal debe construirse y entrenarse **desde cero, sin utilizar redes preentrenadas** (como MobileNetV2).

---

# 🎯 Objetivo del Sistema

El sistema busca desarrollar un modelo capaz de comparar dos fotografías de perros y realizar una clasificación binaria:

```text
1 → Mismo perro
0 → Perros diferentes
```

Este sistema constituye el **MVP (Producto Mínimo Viable)** del proyecto.

La evolución futura del proyecto busca adaptar esta funcionalidad al contexto específico de **Bolívar**.

---

# 🗂️ Dataset

El proyecto utiliza el dataset **YT-BB-Dog**.

Durante la exploración del dataset se identificaron:

```text
2.723 perros
27.036 imágenes
```

Las imágenes están organizadas mediante identificadores numéricos correspondientes a diferentes perros.

La estructura principal contiene:

```text
YT-BB-Dog/
│
├── train/
│   └── identificadores de perros
│
└── test/
    └── identificadores de perros
```

---

# 🧪 Preparación de Datos

Se crearon pares de imágenes.

Cada par contiene:

```text
imagen1 + imagen2 + label
```

Donde:

```text
label = 1 → mismo perro
label = 0 → perros diferentes
```

Los pares fueron balanceados para mantener una cantidad equivalente de ejemplos positivos y negativos.

---

# 📊 Experimento de la versión anterior (red siamesa)

Para el experimento final se seleccionaron:

```text
400 perros → entrenamiento
100 perros → prueba
```

Se generaron:

```text
8.000 pares → entrenamiento
2.000 pares → prueba
```

Distribución:

```text
4.000 pares de mismo perro
4.000 pares de perros diferentes
```

para entrenamiento.

Y:

```text
1.000 pares de mismo perro
1.000 pares de perros diferentes
```

para prueba.

Los perros utilizados en el conjunto de prueba no fueron utilizados durante el entrenamiento. Además, el 20 % de los pares de entrenamiento se reservó como validación.

---

# 🖼️ Preprocesamiento

Las imágenes fueron procesadas antes de ingresar al modelo.

### Tamaño

```text
128 × 128 píxeles
```

### Canales

```text
RGB
```

### Normalización

Los valores de los píxeles se dividieron por 255, para que queden entre 0 y 1.

---

# 🧠 Arquitectura de la versión anterior (red siamesa)

> Esta sección y las dos siguientes (extractor y comparación) describen la red siamesa anterior. El modelo actual, el D, está descripto en "Versión final — Modelo D", dentro de "Evolución del Proyecto".

La arquitectura principal utilizada es una **Siamese Network** con una **CNN propia creada desde cero**.

La idea es procesar dos imágenes mediante la misma red y comparar las características obtenidas.

```text
Imagen 1
   ↓
CNN propia (extractor_128)
   ↓
Vector de características
        \
         \
          → Comparación → Clasificación
         /
        /
Vector de características
   ↑
CNN propia (extractor_128)
   ↑
Imagen 2
```

La misma red, con los mismos pesos, se utiliza para ambas imágenes.

---

# 🔬 Extractor de Características (`extractor_128`)

El extractor es una red convolucional construida desde cero. Todos sus pesos parten de valores aleatorios y se aprenden durante el entrenamiento. **No se utilizan pesos preentrenados.**

Flujo:

```text
Imagen 128 × 128 × 3
   ↓
RandomFlip · RandomRotation · RandomZoom   (solo al entrenar)
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
Vector de características (huella del perro)
```

---

# 🔗 Comparación

Los vectores producidos por las dos imágenes son comparados mediante la diferencia absoluta (capa propia `AbsDifference`):

```text
|Vector 1 - Vector 2|
```

Después se aplican:

```text
Dense(64, ReLU)
   ↓
Dense(1, Sigmoid)
```

La salida final es un número entre 0 y 1 (cerca de 1 → mismo perro).

Parámetros del modelo:

```text
extractor_128:   422.752
comparacion:       8.256
salida:               65
Total:           431.073
(entrenables 430.113 · no entrenables 960)
```

---

# ⚙️ Entrenamiento

Configuración de la versión anterior (red siamesa):

```text
Optimizador:           Adam
Learning rate inicial: 0.001
Pérdida:               binary_crossentropy
Batch size:            32
Validación:            20 % del entrenamiento
Épocas máximas:        40
EarlyStopping:         val_loss, paciencia 5, restaura mejores pesos
ReduceLROnPlateau:     factor 0.5, paciencia 3, mínimo 1e-6
```

El entrenamiento se detuvo automáticamente en la época 30. Se conservaron los pesos de la época 25 (accuracy de validación 87,75 %).

---

# 🔄 Evolución del Proyecto

## Primera versión — CNN inicial

CNN creada desde cero, entrenada con muy pocos datos (16 perros de entrenamiento y 4 de prueba).

```text
Accuracy: 56,25 %
```

Con tan pocos perros, la red no tenía suficientes datos para aprender.

## Experimento de comparación — MobileNetV2

Se probó reemplazar la CNN por **MobileNetV2** preentrenada (transfer learning) y luego fine-tuning de sus últimas capas.

```text
MobileNetV2 congelada:    Accuracy 56,25 %   F1-score 58,82 %
Con más datos:            Accuracy 69,25 %   F1-score 68,94 %
Con fine-tuning:          Accuracy 82,15 %   F1-score 82,83 %
Búsqueda por similitud:   Accuracy 87,81 %   F1-score 88,30 %  (1.600 pares)
```

Este experimento se conserva **solo como comparación**. No es la entrega, porque la consigna prohíbe redes preentrenadas. Las pruebas usaron conjuntos de perros y pares distintos, por lo que los números no son estrictamente comparables con los del modelo final.

## Versión intermedia — CNN propia siamesa mejorada (scratch)

Se construyó nuevamente una red desde cero, con 4 bloques de convolución, BatchNormalization, Dropout, aumento de datos, 8.000 pares de entrenamiento y EarlyStopping.

Resultados sobre los 2.000 pares de prueba (perros nunca vistos):

```text
Con umbral 0,5 (por defecto):
Accuracy 89,95 % | Precision 93,00 % | Recall 86,40 % | F1-score 89,58 %


Con umbral 0,25 (elegido con validación):
Accuracy 88,55 % | Precision 85,40 % | Recall 93,00 % | F1-score 89,04 %

```

Matriz de confusión con umbral 0,25:

```text
[[841 159]

 [ 70 930]]
```

Resultados con similitud coseno (la que usaba la aplicación antes del modelo D), umbral 0,90:

```text
Accuracy 90,80 % | Precision 91,21 % | Recall 90,30 % | F1-score 90,75 %


[[913  87]
 [ 97 903]]
```

Evaluación como buscador (100 perros del test, una foto registrada y otra distinta para buscar):

```text
Perro correcto en primer lugar:     60 de 100
Perro correcto entre los 3 primeros: 80 de 100
Perro correcto entre los 5 primeros: 83 de 100
```

Resumen de la evolución de la red desde cero:

```text
56,25 %  (CNN con 16 perros)
   ↓
89,95 %  (CNN mejorada, umbral 0,5)
   ↓
90,80 %  (CNN mejorada, similitud coseno)

```

## Versión final — Modelo D (extractor con pérdida de trillizos)

Archivo: `model/extractor_D_trillizos.keras`. CNN propia, creada y entrenada desde cero (sin redes preentrenadas). Es solo el extractor: convierte cada foto en un vector de 128 números y dos fotos se comparan con la similitud coseno. No tiene cabeza de comparación ni sigmoide.

```text
Entrenamiento:       pérdida de trillizos (triplet loss), margen 0,3
Tanda:               16 perros x 4 fotos = 64 imágenes
Optimizador:         Adam, learning rate 0,001
Épocas:              30 (100 pasos por época)
Aumento de datos:    RandomFlip, RandomRotation, RandomZoom, RandomBrightness
Umbral de coseno:    0,999876 (elegido en validación, F1 de validación 0,9064)
```

En la app, el coseno se reescala con una sigmoide centrada en 0,999876 (`CENTRO_COSENO` y `ESCALA_COSENO` en `src/config.py`). Por eso `UMBRAL_COINCIDENCIA = 0.5` equivale a ese coseno. El reescalado no cambia el orden de los resultados.

Resultados con perros que el modelo nunca vio:

```text
Pares de prueba:       Accuracy 87,85 % | F1-score 87,78 %
Buscador (100 perros): primero 70 de 100 | entre los 3 primeros 81 de 100 | entre los 5 primeros 85 de 100
```

Comparado con el modelo anterior, la accuracy es parecida, pero como buscador mejora de 54 a 70 de 100 en primer lugar.

Otros intentos:

- Las configuraciones A, B y C (más perros y distinto learning rate) dieron entre 78,6 % y 82,1 % en prueba y entre 32 y 37 de 100 en primer lugar, peor que el modelo anterior.
- Centrar los vectores (restarles la media) empeoró el resultado (F1 de validación 0,73; 48 de 100 en primer lugar) y se descartó.

Límite conocido: durante el entrenamiento, la pérdida de trillizos se estabilizó cerca de 0,30, que es el valor del margen, y las similitudes quedan entre 0,9988 y 0,99999.

---

# 💾 Modelos

El modelo final del proyecto, utilizado por la aplicación:

```text
model/extractor_D_trillizos.keras
```

Tamaño aproximado: 5 MB.

Versión anterior (red siamesa), conservada como comparación: `model/modelo_perros_bolivar_scratch.keras`.

Modelos del experimento de comparación (MobileNetV2), que ya no usa la aplicación:

```text
experimentos/mobilenet_preentrenado/modelo_perros_bolivar_12000_app.keras
experimentos/mobilenet_preentrenado/modelo_perros_bolivar_final.keras
```

---

# 🧪 Entorno de Ejecución

El entrenamiento y la evaluación de la red neuronal se realizan en:

```text
Google Colab (GPU T4)
```

Visual Studio Code se utiliza principalmente para:

```text
Organización del proyecto
Desarrollo
Documentación
Integración del modelo
Gestión del repositorio
```

---

# 📚 Bibliotecas Utilizadas

```text
Python
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

# 📁 Estructura Actual del Proyecto

```text
red-neuronal-identificacion-perros-bolivar/
│
├── .github/workflows/
│   └── ci.yml
│
├── model/
│   ├── extractor_D_trillizos.keras   (modelo final, el que usa la app)
│   └── modelo_perros_bolivar_scratch.keras   (versión anterior, comparación)
│
├── experimentos/
│   └── mobilenet_preentrenado/    (versión anterior con MobileNetV2, NO es la entrega)
│
├── data/
│   ├── candidates/                (fotos candidatas de la galería)
│   ├── found/                     (fotos de perros encontrados, no se sube a Git)
│   ├── raw/
│   ├── processed/
│   └── perros.db                  (base SQLite, no se sube a Git)
│
├── notebooks/
│   └── red_desde_cero_perros.ipynb
│
├── main.py                       (solo arranca la app)
│
├── src/
│   ├── config.py                 (rutas y umbral)
│   ├── models/                   (clases de datos)
│   ├── services/                 (toda la lógica, en clases)
│   │   ├── modelo_service.py
│   │   ├── buscador_service.py
│   │   ├── perros_repository.py
│   │   ├── dataset_service.py
│   │   ├── evaluacion_service.py
│   │   └── entrenamiento_service.py
│   ├── controllers/              (conecta la vista con los services)
│   └── views/                    (interfaz Gradio, HTML y CSS)
│
├── scripts/
│   └── migrar_json_a_sqlite.py
│
├── tests/
│   ├── test_modelo_service.py
│   ├── test_buscador_service.py
│   ├── test_repository.py
│   ├── test_controller.py
│   └── test_dataset_y_evaluacion.py
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

# 🤖 Información para el Agente

El agente debe recordar que:

- El objetivo principal es comparar dos imágenes de perros.
- **No se deben utilizar redes preentrenadas** (como MobileNetV2) en el modelo entregado.
- El modelo actual es una CNN propia creada desde cero, entrenada con pérdida de trillizos. La versión anterior era una red Siamese.
- El modelo final es `extractor_D_trillizos.keras` (solo extractor, entrenado con pérdida de trillizos). `modelo_perros_bolivar_scratch.keras` es la versión anterior, conservada como comparación.
- La aplicación busca coincidencias con similitud coseno entre los vectores del extractor. El coseno se reescala con una sigmoide (`CENTRO_COSENO = 0.999876`, `ESCALA_COSENO = 0.0001`) y el umbral de la app es `UMBRAL_COINCIDENCIA = 0.5`, que equivale a un coseno de 0,999876.
- Resultado del modelo final: 87,85 % de accuracy y 87,78 % de F1 sobre los pares de prueba; como buscador, el perro correcto queda primero en 70 de 100 y entre los 5 primeros en 85 de 100.
- Los umbrales se eligieron con datos de validación, no con los de prueba (versión anterior: 0,25 y 0,90; modelo D: 0,999876).
- Los datos de prueba deben mantenerse separados de los datos de entrenamiento.
- No se deben inventar resultados experimentales.
- Cada nueva mejora debe ser evaluada antes de considerarse definitiva.
- Si se cambia el modelo, hay que recalcular el umbral de similitud.

---

# 🚫 Reglas Importantes

Nunca utilizar el conjunto de prueba para entrenar el modelo.

Nunca utilizar el conjunto de prueba para elegir umbrales.

Nunca considerar una mejora sin comparar métricas.

Nunca eliminar el modelo funcional sin comprobar previamente la nueva versión.

Nunca incorporar pesos preentrenados al modelo entregado.

Nunca usar ni modificar los archivos de `experimentos/` como parte de la entrega.

Mantener documentados:

```text
Dataset
Arquitectura
Parámetros
Entrenamiento
Resultados
Cambios realizados
```

---

# 🔄 Feedback Loop

El proyecto utiliza un proceso iterativo:

```text
Entrenar
   ↓
Evaluar
   ↓
Analizar resultados
   ↓
Detectar problemas
   ↓
Modificar
   ↓
Volver a entrenar
   ↓
Evaluar nuevamente
```

Cada nueva versión debe poder compararse con la anterior.

---

# 📌 Estado Actual

El proyecto cuenta actualmente con:

```text
✅ Dataset YT-BB-Dog seleccionado y preparado

✅ Pares de imágenes generados (8.000 de entrenamiento y 2.000 de prueba)

✅ CNN inicial entrenada

✅ Experimento de comparación con MobileNetV2 realizado

✅ Red siamesa con CNN propia, creada desde cero y entrenada

✅ Umbrales ajustados con datos de validación

✅ Modelo evaluado como clasificador y como buscador

✅ Modelo final exportado (extractor_D_trillizos.keras)

✅ Aplicación Gradio conectada al modelo final

✅ Comparación y búsqueda de fotografías funcionando

✅ Registro de perros encontrados implementado

✅ Registros de perros encontrados guardados en SQLite (data/perros.db)

✅ Caché de vectores en la búsqueda de coincidencias

✅ Experimento con MobileNetV2 archivado en experimentos/mobilenet_preentrenado/ (no es la entrega)

✅ Aplicación ejecutable con python main.py

✅ Pruebas automatizadas implementadas

✅ Repositorio creado

✅ Documentación actualizada
```

El proyecto se encuentra en una etapa funcional de desarrollo, con el modelo integrado en una aplicación local.

---

# 🧠 Último Estado Conocido

Modelo final (entregado):

- `extractor_D_trillizos.keras`: CNN propia con pérdida de trillizos, usada por la aplicación.
  Umbral de coseno 0,999876 (F1 de validación 0,9064). Pares de prueba: Accuracy 87,85 % | F1-score 87,78 %.
  Como buscador con 100 perros: primero 70/100 | entre los 3 primeros 81/100 | entre los 5 primeros 85/100.

Versión anterior (comparación):

- `modelo_perros_bolivar_scratch.keras`: red siamesa con CNN propia.
  Sobre 2.000 pares de prueba con similitud coseno y umbral 0,90:
  Accuracy 90,80 % | Precision 91,21 % | Recall 90,30 % | F1-score 90,75 %

  Como buscador con 100 perros: primero 60/100 | entre los 3 primeros 80/100 | entre los 5 primeros 83/100.

Modelos de comparación (MobileNetV2, no usados por la aplicación):

- `modelo_perros_bolivar_final.keras`: Accuracy 82,15 % | F1-score 82,83 %
- `modelo_perros_bolivar_12000_app.keras`: Accuracy 87,81 % | F1-score 88,30 % (1.600 pares, umbral 0,76)

Umbral de coincidencia en la aplicación: 0.5 sobre el coseno reescalado (equivale a un coseno de 0,999876).

Limitaciones conocidas:

- A veces puntúan alto perros distintos con colores parecidos.
- Las fotos del dataset de un mismo perro se parecen mucho entre sí; con fotos reales de Bolívar el rendimiento podría ser menor.
- Los vectores de las fotos candidatas se guardan en caché mientras la aplicación está abierta, pero no hay un índice persistente: con miles de fotos la primera búsqueda tardaría mucho.
- Con pocas fotos en la galería, los puntajes de perros distintos quedan muy juntos (en pruebas manuales, entre 92 % y 99 %) y el perro correcto no siempre queda primero.

La línea base actual para próximas mejoras es el modelo D (87,85 % en pares y 70 % de acierto en primer lugar).