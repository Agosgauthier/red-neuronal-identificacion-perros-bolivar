# 🤖 AGENT.md — Agente de Inteligencia Artificial

## 📌 Información del Proyecto

Este archivo contiene las instrucciones y el contexto que debe conocer el agente de inteligencia artificial para trabajar de forma organizada, eficiente y reproducible dentro del proyecto.

### Proyecto

**Identificación de Perros en Bolívar — Red Neuronal**

### Objetivo principal

Desarrollar y mejorar un sistema de visión por computadora capaz de comparar dos fotografías de perros y determinar si corresponden al mismo individuo o a perros diferentes.

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

La red utiliza **MobileNetV2** como extractor de características, con pesos preentrenados sobre ImageNet.

Posteriormente se realizó **fine-tuning** para adaptar parte de la red al problema específico.

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
100 perros → entrenamiento
20 perros  → prueba

4.000 pares → entrenamiento
800 pares   → prueba
```

Los pares están balanceados:

```text
50 % → mismo perro
50 % → perros diferentes
```

---

# 📈 Modelo Actual

El modelo final obtenido durante la experimentación alcanzó:

```text
Accuracy: 72,13 %
Precision: 72,18 %
Recall: 72,00 %
F1-score: 72,09 %
```

El modelo se encuentra en:

```text
model/modelo_perros_bolivar_final.keras
```

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

El entrenamiento y la evaluación de la red neuronal se realizan en **Google Colab**.

El agente debe considerar Colab como el entorno principal para ejecutar:

- Preparación del dataset.
- Procesamiento de imágenes.
- Creación de pares.
- Entrenamiento.
- Fine-tuning.
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
- División entre entrenamiento y prueba.
- Arquitectura utilizada.
- Batch size.
- Learning rate.
- Número de épocas.
- Técnica de entrenamiento utilizada.
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

El modelo entrenado debe mantenerse en:

```text
model/modelo_perros_bolivar_final.keras
```

Cuando se genere una nueva versión del modelo, se debe:

1. Comprobar que pueda guardarse correctamente.
2. Comprobar que pueda volver a cargarse.
3. Evaluar su rendimiento.
4. Registrar los resultados.
5. Identificar claramente la nueva versión.

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
- Sobrescribir un modelo funcional sin realizar una copia o comprobar la nueva versión.
- Eliminar documentación existente sin una razón justificada.
- Inventar resultados de entrenamiento o evaluación.
- Considerar una modificación como mejora sin realizar una evaluación.

---

# 📌 Regla Principal

El agente debe priorizar siempre:

**Reproducibilidad + Organización + Evaluación + Documentación**

Cada modificación importante debe poder ser comprendida, ejecutada y evaluada nuevamente.