# 🧠 Skill.md — Habilidades del Agente

## 📌 Descripción

Este archivo define las habilidades y procedimientos que puede utilizar el agente de inteligencia artificial dentro del proyecto **Identificación de Perros en Bolívar — Red Neuronal**.

El objetivo es facilitar la ejecución de tareas relacionadas con datos, entrenamiento, evaluación, documentación y mantenimiento del proyecto.

---

# 🎯 Objetivo

Las habilidades del agente están orientadas a:

- Analizar la estructura del proyecto.
- Preparar y procesar datos.
- Trabajar con imágenes.
- Entrenar modelos de redes neuronales.
- Evaluar modelos.
- Analizar resultados.
- Realizar mejoras iterativas.
- Gestionar modelos entrenados.
- Mantener la documentación.
- Utilizar Git y GitHub.

---

# 🗂️ Gestión de Datos

## Descripción

El agente debe poder trabajar con datasets de imágenes y mantener separados los conjuntos de entrenamiento y prueba.

### Tareas

- Verificar la estructura del dataset.
- Contar imágenes y clases.
- Detectar carpetas inválidas.
- Preparar imágenes.
- Redimensionar imágenes.
- Normalizar valores.
- Crear conjuntos de entrenamiento y prueba.
- Generar pares positivos y negativos.

### Regla

Los datos de prueba no deben utilizarse durante el entrenamiento.

---

# 🖼️ Procesamiento de Imágenes

## Descripción

El agente debe poder preparar imágenes para ser utilizadas por la red neuronal.

### Procedimientos

```text
Imagen original
      ↓
Lectura
      ↓
Conversión RGB
      ↓
Redimensionamiento
      ↓
Normalización
      ↓
Entrada del modelo
```

### Configuración actual

```text
Tamaño: 128 × 128
Canales: RGB
```

---

# 🔗 Creación de Pares

El sistema utiliza pares de imágenes para entrenar la red.

Formato:

```text
imagen1 + imagen2 + label
```

Labels:

```text
1 → mismo perro
0 → perros diferentes
```

### Pares positivos

Dos imágenes pertenecientes al mismo identificador de perro.

### Pares negativos

Dos imágenes pertenecientes a identificadores de perros diferentes.

El agente debe mantener una distribución equilibrada cuando el experimento lo requiera.

---

# 🧠 Creación de Modelos

## Arquitectura utilizada

El proyecto utiliza una **Siamese Network**.

Cada imagen pasa por el mismo extractor de características.

```text
Imagen 1 ──► Extractor ──► Vector 1
                               │
                               ├──► Comparación
                               │
Imagen 2 ──► Extractor ──► Vector 2
```

El extractor utilizado actualmente es:

```text
MobileNetV2
```

con pesos preentrenados sobre ImageNet.

---

# 🔬 Transfer Learning

El agente puede utilizar modelos preentrenados para aprovechar características aprendidas previamente.

En este proyecto se utiliza:

```text
MobileNetV2
```

como extractor de características.

La red puede mantenerse congelada durante una primera etapa y posteriormente utilizarse fine-tuning.

---

# 🛠️ Fine-tuning

## Descripción

El fine-tuning permite adaptar parte de un modelo preentrenado al problema específico.

### Configuración utilizada

```text
Capas finales entrenables
Learning rate: 0.00001
Épocas: 5
```

### Procedimiento

```text
Modelo preentrenado
        ↓
Congelar la mayor parte
        ↓
Descongelar capas finales
        ↓
Learning rate pequeño
        ↓
Reentrenamiento
        ↓
Evaluación
```

---

# ⚙️ Entrenamiento

El agente debe poder ayudar a configurar y ejecutar procesos de entrenamiento.

### Parámetros actuales

```text
Batch size: 32
Learning rate inicial: 0.0001
Learning rate fine-tuning: 0.00001
Épocas iniciales: 10
Épocas fine-tuning: 5
```

### Métrica principal

```text
Accuracy
```

También deben registrarse:

```text
Precision
Recall
F1-score
```

---

# 📈 Evaluación

El agente debe evaluar cada versión del modelo antes de considerarla una mejora.

### Métricas

```text
Accuracy
Precision
Recall
F1-score
Matriz de confusión
```

### Procedimiento

```text
Modelo entrenado
       ↓
Datos de prueba
       ↓
Predicciones
       ↓
Conversión a clases
       ↓
Métricas
       ↓
Análisis
```

---

# 🔄 Feedback Loop

El agente debe utilizar un ciclo iterativo cuando los resultados sean insuficientes.

```text
Entrenar
   ↓
Evaluar
   ↓
Analizar errores
   ↓
Identificar causa
   ↓
Modificar
   ↓
Volver a entrenar
   ↓
Comparar resultados
```

Una modificación solo debe considerarse una mejora si las métricas obtenidas lo justifican.

---

# 🧪 Análisis de Resultados

El agente debe analizar:

- Diferencia entre entrenamiento y validación.
- Rendimiento en datos de prueba.
- Errores de clasificación.
- Matriz de confusión.
- Posible sobreajuste.
- Efecto de cambios en los datos.
- Efecto de cambios en la arquitectura.

Debe distinguir entre:

```text
Mejora real
```

y

```text
Mejora aparente
```

---

# 💾 Gestión de Modelos

El modelo actual se encuentra en:

```text
modelo/modelo_perros_bolivar_final.keras
```

### Procedimiento recomendado

Antes de reemplazar un modelo:

```text
Guardar versión actual
       ↓
Entrenar nueva versión
       ↓
Evaluar
       ↓
Comparar resultados
       ↓
Conservar la mejor versión
```

El modelo no debe sobrescribirse sin comprobar la nueva versión.

---

# 🧪 Verificación del Modelo

Después de guardar un modelo, el agente debe comprobar:

```text
✓ El archivo existe
✓ El modelo puede cargarse
✓ La arquitectura es correcta
✓ Las predicciones funcionan
✓ Las métricas pueden reproducirse
```

---

# 💻 Entorno de Ejecución

## Google Colab

Es el entorno principal para:

- Entrenamiento.
- Evaluación.
- Experimentación.
- Procesamiento de datos.

## Visual Studio Code

Se utiliza para:

- Desarrollo.
- Organización.
- Documentación.
- Integración del modelo.
- Desarrollo de la aplicación.

---

# 🌿 Git y GitHub

El agente debe conocer y utilizar los comandos básicos de Git.

### Estado

```bash
git status
```

### Agregar cambios

```bash
git add .
```

### Crear commit

```bash
git commit -m "descripcion del cambio"
```

### Subir cambios

```bash
git push
```

### Descargar cambios

```bash
git pull
```

### Historial

```bash
git log --oneline
```

---

# 📝 Documentación

El agente debe mantener actualizados:

```text
README.md
AGENT.md
memoria.md
comandos.md
Skill.md
```

Cuando se realice un cambio importante en el modelo o en el flujo de trabajo, debe documentarse.

---

# 🚫 Restricciones

El agente no debe:

- Entrenar utilizando datos de prueba.
- Inventar métricas.
- Inventar resultados de experimentos.
- Eliminar datos sin autorización.
- Reemplazar un modelo funcional sin verificar el nuevo.
- Ignorar errores de ejecución.
- Considerar una mejora sin realizar una evaluación.
- Modificar archivos no relacionados con la tarea.

---

# 🎯 Habilidades Futuras

El agente podrá ampliar sus capacidades para:

- Automatizar experimentos.
- Generar nuevos conjuntos de pares.
- Comparar diferentes arquitecturas.
- Ajustar hiperparámetros.
- Analizar errores específicos.
- Automatizar evaluaciones.
- Integrar el modelo en la aplicación.
- Proponer mejoras basadas en los resultados.

---

# 📌 Estado Actual

Actualmente el proyecto dispone de:

```text
✅ Dataset YT-BB-Dog
✅ Preparación de imágenes
✅ Generación de pares
✅ Siamese Network
✅ MobileNetV2
✅ Transfer Learning
✅ Fine-tuning
✅ Evaluación
✅ Modelo entrenado
✅ Modelo exportado
```

Modelo actual:

```text
modelo/modelo_perros_bolivar_final.keras
```

Resultado:

```text
Accuracy: 72,13 %
Precision: 72,18 %
Recall: 72,00 %
F1-score: 72,09 %
```

---

# 🚀 Próxima Habilidad a Implementar

La próxima etapa consiste en integrar el modelo en una aplicación que permita:

```text
📷 Imagen 1
      +
📷 Imagen 2
      ↓
🧠 Modelo
      ↓
Comparación
      ↓
✅ Mismo perro
      o
❌ Perros diferentes
```

El agente deberá asistir en la implementación, pruebas y documentación de esta funcionalidad.