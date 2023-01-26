# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 14:52:49 2023

@author: sepul
"""

import numpy as np
import matplotlib.pyplot as plt
from random import choice


#---------------------------------DATOS DEL PROBLEMA--------------------------------------------------

nmax= 10 #tiempo maximo de simulacion
s= 0.8


#-----------------------------ARREGLOS PARA GUARDAR DATOS---------------------------------------------

T = np.array([[0,0]]) #define las posiciones ocupadas por cada particula
 
pos= [np.array([0,0])]


#ind_part_activas= np.array([0]) #define el indice de la posicion de las particulas activas en T7
#si defino el indice vacio, hace algo

# ind_tmpt= mp.array([])


#----------------------------FUNCIONES A USAR-----------------------------------------------
def direction(pos, Trace ): 
    #retorna la dirección en que se va a mover una particula 
    # final_position= [ pos + i for i in [(1,0), (-1,0), (0,1), (0,-1)]  ] 
    # final_position= [f for f in final_position if not f in Trace ]
    
    eleccion= []
    for d in [(1,0), (-1,0), (0,1), (0,-1)]:
        
        nuevo = pos + d
        print(nuevo in Trace, Trace, nuevo.dtype)
        if   any(np.equal(Trace, pos).all(1)) : 
            eleccion += nuevo
    #print(eleccion)
           
    if  len(eleccion)== 0: 
        return pos 
    else: 
        return choice(eleccion)  #si eleccion esta vacio, no me puedo mover y me muero
    

#hay que mejorar esto para que la particula nunca vuelva de donde vino 


def action(pos, Trace ):
    pos = direction(pos, Trace) 
    
    #if not (pos in Trace) : 
      
       # N+= 1
        #ind_tmp.append(N) #aqui agregamos el indice de la particula activa nueva 
          #y agregamos a la traza la posicion ocupada
        
    Trace= np.concatenate((Trace, [pos]), axis=0)
      
        #aqui actualizamos la traza dentro el if. No deberíamos actualizarla fuera tambien? 
        
    #ind_part_activas= ind_tmp
    
    
    return Trace
        
    #pos es la posicion actual     
  # if (pos in Trace) == True: dice que si 
      
#--------------------------------- MAIN CODE---------------------------------------------------------


for n in range(10):
    T= action(pos[0], T)
    #ind_tmp = [] #guarda una posicion temporal que debe ser verificada en la traza
    
    # for i in ind_part_activas: 
    #     r= np.random.uniform(0,1) #retorna numeros uniformemente distribuidos entre cero y uno 
    #     pos = np.array(T[i])  #Asigna la posicion a una fila de la traza. Esto es un arreglo de python
       
        
    #     if r< s : #si el número aleatorio escogido es menor que esa cantidad, hay ramificación
    #     #notese que al haber ramificacion, podemos agregar o quitar una particula, dependiendo de si
    #     #las posiciones han sido ocupadas. 
        
    #         T = action(pos, T)
    #         T= action(pos, T)
            
            
    #     else: #si el número es mayor o igual, saltamos 
    #         T= action(pos, T, ind_tmp, N)
               
    # ind_part_activas = ind_tmp     
    
     
plt.scatter(T.T[0], T.T[1]) #filas vs columnas

    
