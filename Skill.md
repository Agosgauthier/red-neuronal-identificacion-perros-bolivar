# 🧠 Skill.md — Habilidades del Agente

## 📌 Descripción

Este archivo define las habilidades y procedimientos que puede utilizar el agente de inteligencia artificial dentro del proyecto **Identificación de Perros en Bolívar — Red Neuronal**.

El objetivo es facilitar la ejecución de tareas relacionadas con datos, entrenamiento, evaluación, documentación y mantenimiento del proyecto.

**Consigna del trabajo:** la red neuronal entregada se construye y entrena **desde cero, sin redes preentrenadas**.

---

# 🎯 Objetivo

Las habilidades del agente están orientadas a:

- Analizar la estructura del proyecto.
- Preparar y procesar datos.
- Trabajar con imágenes.
- Construir y entrenar redes neuronales desde cero.
- Evaluar modelos.
- Ajustar umbrales de decisión.
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

Los datos de prueba no deben utilizarse durante el entrenamiento ni para elegir umbrales.

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
Normalización (dividir por 255)
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

### Configuración actual

```text
400 perros → entrenamiento
100 perros → prueba

8.000 pares → entrenamiento
2.000 pares → prueba

Total: 10.000 pares
```

Del entrenamiento, el 20 % se reserva como validación.

---

### Pares positivos

Dos imágenes pertenecientes al mismo identificador de perro.

### Pares negativos

Dos imágenes pertenecientes a identificadores de perros diferentes.

El agente debe mantener una distribución equilibrada (50 % y 50 %) cuando el experimento lo requiera.

---

# 🧠 Creación de Modelos

## Arquitectura utilizada

El proyecto utiliza una **Siamese Network** con una **CNN propia creada desde cero**.

Cada imagen pasa por el mismo extractor de características.

```text
Imagen 1 ──► Extractor ──► Vector 1
                               │
                               ├──► Comparación
                               │
Imagen 2 ──► Extractor ──► Vector 2
```

El extractor (`extractor_128`) tiene esta estructura:

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

La comparación se realiza así:

```text
|Vector 1 - Vector 2| → Dense(64, ReLU) → Dense(1, Sigmoid)
```

Parámetros totales: 431.073.

Todos los pesos se inicializan al azar y se aprenden durante el entrenamiento. **No se utilizan pesos preentrenados.**

---

# 🔬 Experimento de comparación: Transfer Learning

En una etapa anterior del proyecto se probó **MobileNetV2** con pesos preentrenados sobre ImageNet, con y sin fine-tuning, únicamente como **comparación**.

Ese experimento se conserva en:

```text
experimentos/mobilenet_preentrenado/modelo_perros_bolivar_final.keras
experimentos/mobilenet_preentrenado/modelo_perros_bolivar_12000_app.keras
```

El agente **no debe usar transfer learning ni redes preentrenadas en el modelo entregado**, porque la consigna del trabajo lo prohíbe.

Los resultados de ese experimento no son estrictamente comparables con los del modelo final, porque se midieron con conjuntos de perros y pares distintos.

---

# ⚙️ Entrenamiento

El agente debe poder ayudar a configurar y ejecutar procesos de entrenamiento, en Google Colab con GPU.

### Parámetros actuales

```text
Optimizador: Adam
Learning rate inicial: 0.001
Pérdida: binary_crossentropy
Batch size: 32
Validación: 20 % del entrenamiento
Épocas máximas: 40
EarlyStopping: val_loss, paciencia 5, restaura mejores pesos
ReduceLROnPlateau: factor 0.5, paciencia 3, mínimo 1e-6
```

En el entrenamiento final, el proceso se detuvo en la época 14 y se conservaron los pesos de la época 9.

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

# 🎚️ Ajuste de Umbrales

El agente debe poder elegir umbrales de decisión **usando datos de validación**, nunca los datos de prueba.

```text
Umbral de la salida de la red: 0,15
Umbral de similitud coseno (aplicación): 0,90
```

Procedimiento:

```text
Calcular predicciones sobre validación
        ↓
Probar distintos umbrales
        ↓
Elegir el de mayor F1-score
        ↓
Aplicarlo sobre los datos de prueba
        ↓
Registrar los resultados
```

Cuando se entrene un modelo nuevo, el umbral debe recalcularse y actualizarse en `src/app.py` (`UMBRAL_COINCIDENCIA`).

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
Conversión a clases (con el umbral elegido en validación)
       ↓
Métricas
       ↓
Análisis
```

### Evaluación como buscador

Además de evaluar pares, se mide qué tan bien funciona el sistema buscando un perro entre muchos: se registra una foto de cada perro y se busca con otra foto distinta del mismo perro.

```text
Resultado del modelo final (100 perros):
Primer lugar:          54 de 100
Entre los 3 primeros:  77 de 100
Entre los 5 primeros:  78 de 100
```

### Resultados del modelo final (2.000 pares de prueba)

```text
Similitud coseno, umbral 0,90:
Accuracy 87,55 % | Precision 89,24 % | Recall 85,40 % | F1-score 87,28 %
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
- Efecto del umbral elegido.

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

El modelo final del proyecto, usado por la aplicación, es:

```text
model/modelo_perros_bolivar_scratch.keras
```

Los modelos del experimento de comparación (MobileNetV2) son:

```text
experimentos/mobilenet_preentrenado/modelo_perros_bolivar_final.keras
experimentos/mobilenet_preentrenado/modelo_perros_bolivar_12000_app.keras
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
Recalcular el umbral de similitud
       ↓
Comparar resultados
       ↓
Conservar la mejor versión
```

El modelo no debe sobrescribirse sin comprobar la nueva versión.

Nota sobre Git: el archivo `.gitignore` ignora los archivos `.keras`. Para subir un modelo nuevo hay que agregarlo de forma forzada:

```bash
git add -f model/nombre_del_modelo.keras
```

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
- Ajuste de umbrales.
- Experimentación.
- Procesamiento de datos.

Colab borra la memoria al reiniciarse, por lo que hay que volver a ejecutar las celdas de preparación (dataset, pares y modelo).

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

# 🖥️ Aplicación y Pruebas

El agente puede trabajar con la aplicación de comparación de perros y ejecutar las pruebas automatizadas del proyecto.

## Aplicación

Archivo principal:

```text
src/app.py
```

La aplicación carga `modelo_perros_bolivar_scratch.keras`, calcula la similitud coseno sobre la capa `extractor_128` y usa el umbral 0,90.

Para ejecutarla:

```bash
python -m src.app
```

## Pruebas

Las pruebas se encuentran en:

```text
tests/test_app.py
```

Para ejecutarlas:

```bash
python -m unittest discover -s tests -v
```

El agente debe comprobar que las pruebas continúen funcionando después de realizar modificaciones relacionadas con la aplicación.

---

# 🚫 Restricciones

El agente no debe:

- Entrenar utilizando datos de prueba.
- Elegir umbrales utilizando datos de prueba.
- Incorporar redes o pesos preentrenados al modelo entregado.
- Inventar métricas.
- Inventar resultados de experimentos.
- Eliminar datos sin autorización.
- Reemplazar un modelo funcional sin verificar el nuevo.
- Ignorar errores de ejecución.
- Considerar una mejora sin realizar una evaluación.
- Modificar archivos no relacionados con la tarea.