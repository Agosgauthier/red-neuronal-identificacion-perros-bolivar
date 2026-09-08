# 🧠 Memoria del Proyecto — Identificación de Perros en Bolívar

## 📌 Información General

**Nombre del proyecto:** Identificación de Perros en Bolívar — Red Neuronal

**Materia:** Redes Neuronales

**Tipo de proyecto:** Visión por computadora / Deep Learning

**Objetivo principal:** comparar dos imágenes de perros y determinar si corresponden al mismo perro o a perros diferentes.

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

Para el primer experimento se crearon pares de imágenes.

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
100 perros → entrenamiento
20 perros  → prueba
```

Se generaron:

```text
4.000 pares → entrenamiento
800 pares   → prueba
```

Distribución:

```text
2.000 pares de mismo perro
2.000 pares de perros diferentes
```

para entrenamiento.

Y:

```text
400 pares de mismo perro
400 pares de perros diferentes
```

para prueba.

Los perros utilizados en el conjunto de prueba no fueron utilizados durante el entrenamiento.

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

Los valores de los píxeles fueron normalizados para facilitar el procesamiento de la red neuronal.

---

# 🧠 Arquitectura

La arquitectura principal utilizada es una **Siamese Network**.

La idea es procesar dos imágenes mediante la misma red y comparar las características obtenidas.

```text
Imagen 1
   ↓
MobileNetV2
   ↓
Vector de características
        \
         \
          → Comparación → Clasificación
         /
        /
Vector de características
   ↑
MobileNetV2
   ↑
Imagen 2
```

La misma red se utiliza para ambas imágenes.

---

# 🔬 Extractor de Características

Se utiliza **MobileNetV2** como extractor de características.

La red fue cargada con pesos preentrenados sobre **ImageNet**.

Después se agregaron capas propias para adaptar la representación al problema.

Flujo:

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

---

# 🔗 Comparación

Los vectores producidos por las dos imágenes son comparados mediante la diferencia absoluta:

```text
|Vector 1 - Vector 2|
```

Después se aplican:

```text
Dense(64)
   ↓
Dense(1)
   ↓
Sigmoid
```

La salida final representa:

```text
1 → mismo perro
0 → perros diferentes
```

---

# ⚙️ Entrenamiento

## Primera versión

Se construyó una CNN desde cero.

Resultado sobre el conjunto de prueba:

```text
Accuracy: 56,25 %
```

La primera versión presentó dificultades para reconocer correctamente los pares correspondientes al mismo perro.

---

# 🔄 Segunda versión

Se incorporó **MobileNetV2** mediante transfer learning.

Resultado:

```text
Accuracy: 56,25 %
F1-score: 58,82 %
```

La utilización de una red preentrenada mejoró algunas métricas, aunque el accuracy general no aumentó en esta etapa.

---

# 📈 Tercera versión

Se amplió el experimento utilizando una mayor cantidad de perros y pares.

Configuración:

```text
100 perros de entrenamiento
20 perros de prueba

4.000 pares de entrenamiento
800 pares de prueba
```

Resultado:

```text
Accuracy: 69,25 %
F1-score: 68,94 %
```

El aumento del conjunto de datos produjo una mejora importante en la capacidad de generalización.

---

# 🛠️ Fine-tuning

Posteriormente se realizó **fine-tuning** sobre las capas finales de MobileNetV2.

Se mantuvo congelada la mayor parte de la red y se habilitaron las capas finales para que pudieran adaptarse al problema específico.

Learning rate utilizado durante fine-tuning:

```text
0.00001
```

Se realizaron:

```text
5 épocas
```

Resultado final:

```text
Accuracy: 72,13 %
Precision: 72,18 %
Recall: 72,00 %
F1-score: 72,09 %
```

---

# 📊 Matriz de Confusión Final

La matriz de confusión obtenida fue:

```text
[[289 111]
 [112 288]]
```

Interpretación:

```text
289 → perros diferentes correctamente clasificados
111 → perros diferentes clasificados como mismo perro

112 → pares del mismo perro clasificados como diferentes
288 → pares del mismo perro correctamente clasificados
```

---

# 📈 Evolución de Resultados

La evolución de las principales versiones fue:

```text
CNN inicial
Accuracy: 56,25 %
       ↓
MobileNetV2
Accuracy: 56,25 %
       ↓
Más datos
Accuracy: 69,25 %
       ↓
Fine-tuning
Accuracy: 72,13 %
```

La mejor versión actual es la versión con **MobileNetV2 + fine-tuning**.

---

# 💾 Modelo Final

El modelo final exportado se llama:

```text
modelo_perros_bolivar_final.keras
```

Ubicación dentro del repositorio:

```text
model/modelo_perros_bolivar_final.keras
```

Tamaño aproximado:

```text
9,85 MB
```

---

# 🧪 Entorno de Ejecución

El entrenamiento y la evaluación de la red neuronal se realizan en:

```text
Google Colab
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

Las principales herramientas y bibliotecas utilizadas son:

```text
Python
TensorFlow
Keras
MobileNetV2
OpenCV
NumPy
Pandas
Scikit-learn
Matplotlib
```

---

# 📁 Estructura Actual del Proyecto

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

# 🤖 Información para el Agente

El agente debe recordar que:

- El objetivo principal es comparar dos imágenes de perros.
- El modelo actual utiliza una arquitectura Siamese.
- MobileNetV2 funciona como extractor de características.
- El modelo fue ajustado mediante fine-tuning.
- El resultado final actual es de 72,13 % de accuracy.
- Los datos de prueba deben mantenerse separados de los datos de entrenamiento.
- No se deben inventar resultados experimentales.
- Cada nueva mejora debe ser evaluada antes de considerarse definitiva.

---

# 🚫 Reglas Importantes

Nunca utilizar el conjunto de prueba para entrenar el modelo.

Nunca considerar una mejora sin comparar métricas.

Nunca eliminar el modelo funcional sin comprobar previamente la nueva versión.

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

# 🚧 Próximas Tareas

El proyecto debe continuar con:

```text
1. Crear la interfaz de usuario.
2. Permitir cargar dos fotografías.
3. Preprocesar ambas imágenes.
4. Ejecutar el modelo.
5. Mostrar el resultado.
6. Realizar pruebas con imágenes externas.
7. Mejorar el rendimiento.
8. Adaptar el sistema al contexto de Bolívar.
```

---

# 📌 Estado Actual

```text
✅ Dataset seleccionado
✅ Dataset descargado
✅ Dataset validado
✅ Datos preparados
✅ Pares generados
✅ CNN inicial entrenada
✅ MobileNetV2 implementada
✅ Dataset experimental ampliado
✅ Fine-tuning realizado
✅ Modelo evaluado
✅ Modelo final exportado
✅ Repositorio creado
✅ Documentación inicial creada
```

Pendiente:

```text
🚧 Integración del modelo en una aplicación
🚧 Interfaz para cargar imágenes
🚧 Predicción visual
🚧 Nuevas pruebas
🚧 Nuevas mejoras del modelo
```

---

# 🧠 Último Estado Conocido

La mejor versión disponible actualmente es:

```text
modelo_perros_bolivar_final.keras
```

Métricas:

```text
Accuracy: 72,13 %
Precision: 72,18 %
Recall: 72,00 %
F1-score: 72,09 %
```

Este modelo debe considerarse la **línea base actual** para las próximas mejoras.