# Detector de flujo urbano

## Uso del contador automático
El contador automático recibe como entrada un video y genera un archivo csv con el número de vehículos ligeros y pesados, taxis, motocicletas y personas. El contador actual obtiene buenos resultados con vehículos y taxis; para contar personas y motocicletas se requiere de mejorar los [parámetros](./parametros/README.md).

Este ejemplo utiliza videos tomados por un dron en una zona de interés de la ciudad de Quito. 

Se debe ejecutar el archivo [main.py](./main.py) de la siguiente forma:

python main.py --input "ruta del video" --config "id_configuración"

Cada video de ejemplo tiene un id de configuración para que funcione.
Estas son todas las posibles formas de usar el programa:

* python .\main.py --input ".\sur_oriente.mp4"--config "sur_or_ab"
* python .\main.py --input ".\sur_oriente.mp4"--config "sur_or_ai"
* python .\main.py --input ".\sur_oriente.mp4"--config "sur_or_id"
* python .\main.py --input ".\nor_occidente.mp4" --config "nor_oc_ab"
* python .\main.py --input ".\nor_occidente.mp4" --config "nor_oc_d"
* python .\main.py --input ".\nor_oriente.mp4" --config "nor_or_id"
* python .\main.py --input ".\nor_oriente.mp4" --config "nor_or_ab"
* python .\main.py --input ".\sur_occidente.mp4" --config "sur_oc_ab"
* python .\main.py --input ".\Puente_guambra2.mp4" --config "p_g_i"
* python .\main.py --input ".\Puente_guambra2.mp4" --config "p_g_d"
* python .\main.py --input ".\Puente_guambra2.mp4" --config "p_g_ab"

## Descargar los videos de ejemplo
Si quieres acceder a los videos de ejemplo puedes hacerlo a través del [siguiente link](https://cutt.ly/HnRDmNE).

## Aprendizaje
Si quieres conocer cómo funciona este módulo de conteo automático, la carpeta [notebooks](./notebooks/README.md) contiene las explicaciones esenciales sobre el funcionamiento de main.py.

## Personalización 
Si quieres usar el contador automático en tus propios videos sólo debes modificar los [parámetros](./parametros/README.md) para ajustarlos a tu contenido.