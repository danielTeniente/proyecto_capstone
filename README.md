# Proyecto Capstone: Modelado del flujo urbano

## Introducción
Consiste en la construcción de un modelo de las calles de una zona de interés. El modelo se construyó utilizando OSMNX. 
Para la obtención de datos también se implementó un contador automático de vehículos en base a videos realizados por un dron.

## Contador de vehículos
La carpeta [detector_flujo_urbano](./detector_flujo_urbano) cuenta con un módulo para contar diferentes tipos de vehículos automáticamente a partir de un video. 

## Modelado de la zona de interés
La carpeta [modelo_ROI](./modelo_ROI) explica cómo generar un modelo simplificado a partir de la biblioteca OSMNX, junto con una serie de algoritmos aplciados sobre el modelo.

## Mapeo de flujo urbano
Consiste en colocar la información extraída de los videos en un modelo de OSMNX.