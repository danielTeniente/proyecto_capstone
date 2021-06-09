# Parámetros
Este módulo de conteo está pensado para generalizar el conteo automático de vehículos, lo único que se necesita hacer para adecuarlo a tus videos es modificar el archivo de configuración: roi_config.py.

El archivo consiste en una serie de parámetros que se implementarán a la hora de ejecutar el programa. Estos parámetros se encuentran en una función que retorna los valores configurados:

* points_roi: consiste en los puntos que marcarán la zona de interés dentro del video. Esto se explica con más detalle en los [notebooks](../notebooks).
* size_roi: consiste en el tamaño que tendrá la imagen cuando se ejecute el programa, esto servirá para la correcta visualización del video.
* get_exit_points: Se refiere a los puntos que marcarán la zona de salida. Nuevamente, este concepto se encuentra mejor explicado en los [notebooks](../notebooks).
* get_measurements: este es uno de los más importantes, pues definen el tamaño de los vehículos. Esta configuración permite distinguir entre un vehículo ligero y uno pesado. Se tratan de medidas de largo y ancho que deben ser ajustadas para clasificar los vehículos correctamente.
