# 🤖 AGENT.md — Agente de Inteligencia Artificial

## 📌 Información del Proyecto

Este archivo contiene las instrucciones y el contexto que debe conocer el agente de inteligencia artificial para trabajar de forma organizada, eficiente y reproducible dentro del proyecto.

### Proyecto

**Identificación de Perros en Bolívar — Red Neuronal**

### Objetivo principal

Desarrollar y mejorar un sistema de visión por computadora capaz de comparar dos fotografías de perros y determinar si corresponden al mismo individuo o a perros diferentes.

### Consigna del trabajo

La red neuronal debe construirse y entrenarse **desde cero, sin utilizar redes preentrenadas** (como MobileNetV2).

---

# 🎯 Objetivo del Agente

El agente de inteligencia artificial tiene como finalidad asistir en el desarrollo, mantenimiento y mejora del proyecto de redes neuronales.

Debe ser capaz de:

- Comprender el objetivo general del proyecto.
- Comprender la estructura del repositorio.
- Consultar la documentación existente antes de realizar cambios.
- Ayudar en la preparación y procesamiento de datos.
- Asistir en la construcción y modificación de modelos.
- Ejecutar y documentar procesos de entrenamiento y evaluación.
- Analizar métricas obtenidas.
- Detectar problemas en los resultados.
- Proponer y aplicar mejoras.
- Mantener la organización del proyecto.
- Registrar información relevante para futuras interacciones.

---

# 🧠 Contexto del Modelo

El proyecto utiliza una **Siamese Network** para comparar dos imágenes.

La red utiliza una **CNN propia, creada y entrenada desde cero**, como extractor de características (`extractor_128`). Todos sus pesos parten de valores aleatorios. **No se utilizan pesos preentrenados.**

Estructura del modelo:

```text
Imagen 128 × 128 × 3
   ↓
RandomFlip · RandomRotation · RandomZoom   (solo al entrenar)
   ↓
4 bloques: Conv2D → BatchNormalization → ReLU → MaxPooling
           (32, 64, 128 y 256 filtros)
   ↓
GlobalAveragePooling2D → Dropout(0.3) → Dense(128, ReLU)
   ↓
Vector de características (huella del perro)
```

Las dos imágenes pasan por la misma red. Luego se comparan:

```text
|Vector 1 - Vector 2| → Dense(64, ReLU) → Dense(1, Sigmoid)
```

Parámetros totales: 431.073.

MobileNetV2 se probó únicamente como experimento de comparación en una etapa anterior del proyecto. No forma parte del modelo entregado.

### Entrada

El modelo recibe dos imágenes:

```text
Imagen 1
Imagen 2
```

Las imágenes se redimensionan a:

```text
128 × 128 píxeles
```

y sus valores se dividen por 255.

### Salida

El modelo realiza una clasificación binaria:

```text
1 → Mismo perro
0 → Perros diferentes
```

---

# 📊 Dataset

El proyecto utiliza el dataset **YT-BB-Dog**.

El dataset contiene:

- **2.723 perros**
- **27.036 imágenes**

Para el experimento final se trabajó con:

```text
400 perros → entrenamiento
100 perros → prueba

8.000 pares → entrenamiento
2.000 pares → prueba

Total: 10.000 pares de fotografías
```

Los pares están balanceados:

```text
50 % → mismo perro
50 % → perros diferentes
```

Los perros de prueba no se usan durante el entrenamiento. El 20 % de los pares de entrenamiento se reserva como validación.

---

# 📈 Modelo Actual

El modelo final del proyecto, usado por la aplicación, es:

- `model/modelo_perros_bolivar_scratch.keras`: red siamesa con CNN propia, 431.073 parámetros.

Resultados sobre 2.000 pares de prueba (perros no vistos):

```text
Con similitud coseno (umbral 0,90, el que usa la aplicación):
Accuracy:  87,55 %
Precision: 89,24 %
Recall:    85,40 %
F1-score:  87,28 %

Con la salida de la red (umbral 0,15):
Accuracy:  87,55 %
Precision: 88,20 %
Recall:    86,70 %
F1-score:  87,44 %
```

Como buscador (100 perros del test, una foto registrada y otra distinta para buscar):

```text
Perro correcto en primer lugar:      54 de 100
Perro correcto entre los 3 primeros: 77 de 100
Perro correcto entre los 5 primeros: 78 de 100
```

Los umbrales (0,15 y 0,90) se eligieron con datos de validación, no con los de prueba.

Modelos del experimento de comparación (MobileNetV2), que la aplicación ya no usa:

- `experimentos/mobilenet_preentrenado/modelo_perros_bolivar_final.keras`: Accuracy 82,15 % | F1-score 82,83 %.
- `experimentos/mobilenet_preentrenado/modelo_perros_bolivar_12000_app.keras`: Accuracy 87,81 % | F1-score 88,30 % (1.600 pares, umbral 0,76).

---

# 🔄 Metodología de Trabajo

El agente debe seguir un proceso iterativo:

```text
Analizar
   ↓
Planificar
   ↓
Modificar
   ↓
Ejecutar
   ↓
Evaluar
   ↓
Detectar problemas
   ↓
Mejorar
   ↓
Documentar
```

Las modificaciones realizadas sobre el modelo deben ser evaluadas antes de considerarse mejoras definitivas.

---

# 🧪 Entorno de Ejecución

## Google Colab

El entrenamiento y la evaluación de la red neuronal se realizan en **Google Colab**, con GPU (T4).

El agente debe considerar Colab como el entorno principal para ejecutar:

- Preparación del dataset.
- Procesamiento de imágenes.
- Creación de pares.
- Entrenamiento.
- Ajuste de umbrales.
- Evaluación.
- Experimentación.

## Visual Studio Code

Visual Studio Code se utiliza para:

- Organizar el proyecto.
- Desarrollar el código.
- Mantener la documentación.
- Integrar el modelo.
- Desarrollar la aplicación.
- Gestionar el repositorio Git.

---

# 📁 Estructura del Proyecto

```text
red-neuronal-identificacion-perros-bolivar/
│
├── .github/workflows/
│   └── ci.yml
│
├── model/
│   └── modelo_perros_bolivar_scratch.keras
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
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── db.py
│   ├── generar_pares.py
│   └── migrar_json_a_sqlite.py
│
├── tests/
│   ├── test_app.py
│   └── test_db.py
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

# 🛠️ Reglas de Trabajo

Antes de modificar archivos o código, el agente debe:

1. Revisar la documentación disponible.
2. Identificar el objetivo de la tarea.
3. Comprobar qué archivos están relacionados.
4. Evitar modificar archivos que no sean necesarios.
5. Mantener la estructura del proyecto.
6. Documentar cambios importantes.
7. Comprobar que el código continúe funcionando después de las modificaciones.

---

# 🧪 Entrenamiento y Evaluación

Cuando se modifique la arquitectura o el proceso de entrenamiento, el agente debe registrar:

- Dataset utilizado.
- Cantidad de datos.
- División entre entrenamiento, validación y prueba.
- Arquitectura utilizada.
- Batch size.
- Learning rate.
- Número de épocas.
- Técnica de entrenamiento utilizada.
- Umbrales de decisión y con qué datos se eligieron.
- Accuracy.
- Precision.
- Recall.
- F1-score.
- Matriz de confusión.

Los resultados deben compararse con versiones anteriores.

---

# 🔄 Feedback Loop

Cuando una evaluación produzca resultados insuficientes, el agente debe utilizar un ciclo de retroalimentación:

```text
Resultado insuficiente
        ↓
Analizar métricas
        ↓
Identificar posible causa
        ↓
Modificar datos / arquitectura / entrenamiento
        ↓
Volver a entrenar
        ↓
Evaluar nuevamente
        ↓
Comparar resultados
```

No se debe asumir que una modificación mejora el modelo sin comprobarlo mediante una nueva evaluación.

---

# 💾 Gestión del Modelo

El modelo entrenado que usa la aplicación debe mantenerse en:

```text
model/modelo_perros_bolivar_scratch.keras
```

La aplicación (`src/app.py`) apunta a ese archivo mediante `RUTA_MODELO`, y usa el umbral `UMBRAL_COINCIDENCIA = 0.90`.

Cuando se genere una nueva versión del modelo, se debe:

1. Comprobar que pueda guardarse correctamente.
2. Comprobar que pueda volver a cargarse.
3. Evaluar su rendimiento.
4. **Recalcular el umbral de similitud** con datos de validación y actualizarlo en `src/app.py`.
5. Registrar los resultados.
6. Identificar claramente la nueva versión.

---

# 📝 Documentación

El agente debe mantener actualizados los siguientes archivos:

| Archivo | Función |
|---|---|
| `README.md` | Documentación general del proyecto |
| `AGENT.md` | Instrucciones y contexto para el agente |
| `memoria.md` | Información relevante para futuras interacciones |
| `comandos.md` | Comandos utilizados en el proyecto |
| `Skill.md` | Habilidades y procedimientos disponibles |

---

# 🤖 Comportamiento Esperado del Agente

El agente debe:

- Trabajar de manera ordenada.
- Explicar los cambios importantes.
- Evitar modificaciones innecesarias.
- Mantener la reproducibilidad de los experimentos.
- Utilizar los archivos de documentación como fuente de contexto.
- Comparar resultados antes y después de cada modificación importante.
- Registrar problemas encontrados y soluciones aplicadas.
- Mantener separados los datos de entrenamiento y prueba.
- Evitar mezclar información del conjunto de prueba durante el entrenamiento.

---

# 🚫 Restricciones

El agente no debe:

- Modificar el dataset original sin necesidad.
- Utilizar los datos de prueba para entrenar el modelo.
- Utilizar los datos de prueba para elegir umbrales.
- Incorporar redes o pesos preentrenados (como MobileNetV2) al modelo entregado.
- Utilizar, ejecutar o modificar los archivos de `experimentos/` como parte de la entrega.
- Sobrescribir un modelo funcional sin realizar una copia o comprobar la nueva versión.
- Eliminar documentación existente sin una razón justificada.
- Inventar resultados de entrenamiento o evaluación.
- Considerar una modificación como mejora sin realizar una evaluación.

---

# 📌 Regla Principal

El agente debe priorizar siempre:

**Reproducibilidad + Organización + Evaluación + Documentación**

Cada modificación importante debe poder ser comprendida, ejecutada y evaluada nuevamente.