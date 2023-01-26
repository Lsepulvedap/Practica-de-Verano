# Practica-de-Verano

Repositorio destinado a guardar codigos, imágenes y datos para análisis que se vaya utilizando durante las práticas de verano 2023, Uchile. 

Resumen del trabajo 

Usando un conjunto de reglas sencillas mediante una simulacion basada en agentes logramos obtener dos tipos de red que cubren todo el espacio disponible, hasta llegar a un borde que las absorbe sus partículas constituyentes y desactiva. 

La primera red (red con ramificación de puntas) parte con una partícula activa que en cada paso de tiempo se ramifica  en dos nuevas partículas activas, desactivando la anterior. En cada paso de tiempo, tan solo una de las particulas nuevas (escogida al azar) se ramifica. Se consideran aquí que las partículas activas son aquellas que están en el extremo de las trayectorias. 

La segunda red (red con reactivación) parte con una partícula activa que se mueve en una dirección aleatoria. En este caso, las particulas activas son aquellas que tienen espacio disponible para saltar. En cada paso de tiempo, una partícula activa elegida al azar salta. 

En ambos casos, las particulas pueden elegir moverse hasta en seis direcciones (Esto puedes cambiarlo en la función 'direction'!), y ya que en cada paso de tiempo se mueve solo una activa al azar, se genera un frente de propagación rugoso. Esto es, que el frente no crece 'todo al mismo tiempo', por lo que se ve un poco deforme mientras el tiempo avanza. Además, la condicipon de borde impuesta es una condición absorbente, es decir, una vez que las partículas llegan al borde son absorbidas por este, y mueren. 

Sobre el codigo 

En la carpeta 'CODE' podrás encontrar todos (si, todos) los códigos (intentos y fracasos) que escribí y/o use durante el transcurso de la actividad. Cada función tiene su descripción y su forma de uso. Si es que hay algo que no se entiende, porfavor, házmelo saber! 

Conclusiones y resultados
En la carpeta 'IMG' podrás encontrar todos los gráficos generados y utilizados durante la actividad.  De las figuras de distribuciones de nodos tenemos que, dado que en la red con reactivación, una misma partícula en distintos pasos de tiempo puede moverse y ocupar espacios disponibles las conexiones se pueden dar hasta con seis nodos! Por otro lado, la red con ramificación de puntas tiene a lo más conexiones con tres nodos, pues nodos intermedios se conectan con el anterior y los dos en los que se ramifica (ver árboles). 

Como consecuencia de generar conexiones a lo más con tres nodos, la red con ramificación de puntas genera menos subárboles por nivel que la red con
reactivación. Ya que ambas deben llenar el mismo espacio, la red con ramificación produce subárboles de mayor tamaño y más persistentes, mientras que la red con
reactivación produce subárboles mas pequeños y menos persistentes.
Como trabajo a futuro se propone comparar las propiedades de estas redes con las de patrones observados en sistemas no lineales teóricos y experimentales, así como
también describir matemáticamente cada modelo mediante ecuaciones de campo medio.

Para mas información, contáctame a lsepulveda2019@udec.cl
