# Experimentos previos con MobileNetV2

## Propósito

Esta carpeta contiene archivos de una versión anterior del proyecto de identificación de perros de Bolívar, desarrollada utilizando MobileNetV2 preentrenada y técnicas de transferencia de aprendizaje (*transfer learning*).

Se conservan únicamente como referencia histórica y para comparar el enfoque anterior con la solución actual.

## Importante: no forman parte de la entrega principal

La entrega principal utiliza una red neuronal convolucional (CNN) construida y entrenada desde cero, sin utilizar MobileNetV2 ni pesos preentrenados de ImageNet.

Los archivos de esta carpeta no deben utilizarse como modelo principal de la aplicación ni como procedimiento de entrenamiento de la entrega.

## Contenido

- `entrenar_modelo_grande.py`: script de entrenamiento de la versión anterior.
- `evaluar_modelo.py`: evaluación del modelo anterior.
- `evaluar_similitud.py`: experimento de comparación de similitud.
- `arreglar_modelo.py`: script auxiliar de la versión anterior.
- `identificacion_perros_bolivar.ipynb`: notebook del experimento anterior.
- `modelo_perros_bolivar_final.keras`: modelo guardado de la versión anterior.
- `modelo_perros_bolivar_12000_app.keras`: otro modelo guardado de la versión anterior.

## Ejecución

Estos archivos son históricos. Sus rutas originales pueden haber cambiado y no se garantiza que puedan ejecutarse directamente desde esta carpeta.

Para trabajar con la entrega principal, deben utilizarse el código, el notebook y el modelo entrenados desde cero que estén documentados como parte de la solución vigente.
