# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 16:34:15 2023

@author: sepul
"""

import numpy as np
import matplotlib.pyplot as plt
from random import choice

#comenzamos definiendo el numero de partículas, tiempo máximo de simulación y paso de tiempo

N= 1 #basta que tengamos una sola partícula que comience a ramificarse y moverse
h= 0.1 #paso de tiempo
tmax= 500 #define el tiempo durante el que se corre la simulación. Notar que la misma no depende del tiempo. Este
          #solo es un contador. Aqui el tiempo simplemente define cuando ocurrirá una nueva acción. 
t=1 
#Podemos definir la traza como una matriz de Nx2, y luego quitar los espacios en blanco. Ya que no se conoce el 
#número de partículas N, estimamos que el tamaño máximo de la matriz a inicializar será dim(tmáx). Entonces, la 
#matriz a inicializar debería ser de 100^2 x2.


T= np.array([0,0]) #define la traza/camino de la(s) partícula(s). 

ind_part_activas = np.array([ ]) # guarda el indice de la posición de las particulas activas

direction = [(1,0), (-1,0), (0,1), (0,-1)] 


    
#Ahora definimos cuando van a ocurrir los movimientos. Para esto, primero definimos la tasa de movimiento
# y ramificación,h y s, respectivamente:  

s= 0.9 #tasa de ramificacion


x, y= 75,75 #posicion de la partícula inicial
while t < tmax:
        
    t += h # tiempo= tiempo+ h
    ind_tmp = [] #guarda una posicion temporal que debe ser verificada en la traza
    
    for i in ind_part_activas: 
        r= np.random.uniform(0,1) #retorna numeros uniformemente distribuidos entre cero y uno 
        pos = T[i]    #guarda una posicion en la traza
        
        if r< s*h: #si el número aleatorio escogido es menor que esa cantidad, hay ramificación
        #notese que al haber ramificacion, podemos agregar o quitar una particula, dependiendo de si
        #las posiciones han sido ocupadas. 
        
            p1 = pos + choice(direction)
            p2 = pos + choice(direction)
            
        
            # revisar si p1 está en la traza, si no esta, entonces actualizar ind_tmp
            # y la traza, y N +=1. Si está, entonces no hacer nada
            
            if p1.all in T == True: 
                pass 
            else : 
                N+= 1
                ind_tmp.append(N) #aqui agregamos el indice de la particula activa nueva 
                T= np.append(T, p1, axis= 0 )   #p1 #aqui agregamos a T la posicion de la particula activa
            
            # hacer lo mismo para p2
            if p2.all in T == True: 
                pass 
            else : 
                N+=1
                ind_tmp.append(N)
                T= np.append(T, p2, axis= 0)
        
            
        else:  # si está, entonces eliminar la partícula activa
            p = pos + choice(direction)
                # revisar si p1 está en la traza, si no esta, entonces actualizar ind_tmp
                # y la traza, y N +=1. Si está, entonces no hacer nada
            if p.all in T == True: 
                pass 
            else : 
                N+=1
                ind_tmp.append(N)
                T=  np.append(T, p2, axis= 0 ) 
          
    ind_part_activas = ind_tmp        
     
plt.scatter(T.T[0], T.T[1]) #filas vs columnas

    
    
    
    
    
    
    
