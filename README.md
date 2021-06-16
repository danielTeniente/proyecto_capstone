# Proyecto Capstone: Modelado del flujo urbano

## Introducción
Consiste en la construcción de un modelo de las calles de una zona de interés. El modelo se construyó utilizando OSMNX. 
Para la obtención de datos también se implementó un contador automático de vehículos en base a videos realizados por un dron.

## Contador de vehículos
La carpeta [detector_flujo_urbano](./detector_flujo_urbano/Readme.md) cuenta con un módulo para contar diferentes tipos de vehículos automáticamente a partir de un video. 

## Modelado de la zona de interés
La carpeta [modelo_ROI](./modelo_ROI/README.md) explica cómo generar un modelo simplificado a partir de la biblioteca OSMNX, junto con una serie de algoritmos aplicados sobre el modelo.

## Mapeo de flujo urbano
La carpeta [analisis](./analisis/README.md) consiste en colocar la información extraída de los videos en un modelo de OSMNX. Es el resultado de combinar los dos temas anteriores.
