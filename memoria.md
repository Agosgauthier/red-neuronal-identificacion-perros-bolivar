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

# 📊 Experimento Final

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

# 🧠 Arquitectura

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

Configuración del modelo final:

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

El entrenamiento se detuvo automáticamente en la época 14. Se conservaron los pesos de la época 9 (accuracy de validación 75,94 %).

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

## Versión final — CNN propia mejorada

Se construyó nuevamente una red desde cero, con 4 bloques de convolución, BatchNormalization, Dropout, aumento de datos, 8.000 pares de entrenamiento y EarlyStopping.

Resultados sobre los 2.000 pares de prueba (perros nunca vistos):

```text
Con umbral 0,5 (por defecto):
Accuracy 71,85 % | Precision 98,23 % | Recall 44,50 % | F1-score 61,25 %

Con umbral 0,15 (elegido con validación):
Accuracy 87,55 % | Precision 88,20 % | Recall 86,70 % | F1-score 87,44 %
```

Matriz de confusión con umbral 0,15:

```text
[[884 116]
 [133 867]]
```

Resultados con similitud coseno (la que usa la aplicación), umbral 0,90:

```text
Accuracy 87,55 % | Precision 89,24 % | Recall 85,40 % | F1-score 87,28 %

[[897 103]
 [146 854]]
```

Evaluación como buscador (100 perros del test, una foto registrada y otra distinta para buscar):

```text
Perro correcto en primer lugar:     54 de 100
Perro correcto entre los 3 primeros: 77 de 100
Perro correcto entre los 5 primeros: 78 de 100
```

Resumen de la evolución de la red desde cero:

```text
56,25 %  (CNN con 16 perros)
   ↓
71,85 %  (CNN mejorada, umbral 0,5)
   ↓
87,55 %  (CNN mejorada, umbral ajustado)
```

---

# 💾 Modelos

El modelo final del proyecto, utilizado por la aplicación:

```text
model/modelo_perros_bolivar_scratch.keras
```

Tamaño aproximado: 5 MB.

Modelos del experimento de comparación (MobileNetV2), que ya no usa la aplicación:

```text
model/modelo_perros_bolivar_12000_app.keras
model/modelo_perros_bolivar_final.keras
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

# 🤖 Información para el Agente

El agente debe recordar que:

- El objetivo principal es comparar dos imágenes de perros.
- El modelo actual utiliza una arquitectura Siamese con una CNN propia creada desde cero.
- **No se deben utilizar redes preentrenadas** (como MobileNetV2) en el modelo entregado.
- El modelo final es `modelo_perros_bolivar_scratch.keras`, con 431.073 parámetros.
- La aplicación busca coincidencias con similitud coseno sobre la capa `extractor_128`, con umbral de 0,90.
- Resultado del modelo final: 87,55 % de accuracy sobre 2.000 pares de prueba; como buscador, el perro correcto queda primero en 54 de 100 y entre los 5 primeros en 78 de 100.
- Los umbrales (0,15 para la salida de la red y 0,90 para la similitud coseno) se eligieron con datos de validación, no con los de prueba.
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

✅ Modelo final exportado (modelo_perros_bolivar_scratch.keras)

✅ Aplicación Gradio conectada al modelo final

✅ Comparación y búsqueda de fotografías funcionando

✅ Registro de perros encontrados implementado

✅ Pruebas automatizadas implementadas

✅ Repositorio creado

✅ Documentación actualizada
```

El proyecto se encuentra en una etapa funcional de desarrollo, con el modelo integrado en una aplicación local.

---

# 🧠 Último Estado Conocido

Modelo final (entregado):

- `modelo_perros_bolivar_scratch.keras`: red siamesa con CNN propia, usada por la aplicación.
  Sobre 2.000 pares de prueba con similitud coseno y umbral 0,90:
  Accuracy 87,55 % | Precision 89,24 % | Recall 85,40 % | F1-score 87,28 %
  Como buscador con 100 perros: primero 54/100 | entre los 3 primeros 77/100 | entre los 5 primeros 78/100.

Modelos de comparación (MobileNetV2, no usados por la aplicación):

- `modelo_perros_bolivar_final.keras`: Accuracy 82,15 % | F1-score 82,83 %
- `modelo_perros_bolivar_12000_app.keras`: Accuracy 87,81 % | F1-score 88,30 % (1.600 pares, umbral 0,76)

Umbral de coincidencia en la aplicación: 0,90.

Limitaciones conocidas:

- A veces puntúan alto perros distintos con colores parecidos.
- Las fotos del dataset de un mismo perro se parecen mucho entre sí; con fotos reales de Bolívar el rendimiento podría ser menor.
- La aplicación recalcula las características de cada foto candidata en cada búsqueda, por lo que no escala a miles de fotos sin guardar los vectores precalculados.

La línea base actual para próximas mejoras es el modelo final desde cero (87,55 % en pares y 54 % de acierto en primer lugar).