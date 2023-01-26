# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 13:12:28 2023

@author: sepul
"""

import numpy as np
import matplotlib.pyplot as plt
from random import choice


#---------------------------------DATOS DEL PROBLEMA--------------------------------------------------

tmax= 100 #tiempo maximo de simulacion
t= 1  #tiempo inicial 


#-----------------------------ARREGLOS PARA GUARDAR DATOS---------------------------------------------

T = np.array([0,0]) #define las posiciones ocupadas por cada particula
ind_part_activas= np.array([]) #define el indice de la posicion de las particulas activas en T

#ind_tmpt= mp.array([])


#----------------------------FUNCIONES A USAR-----------------------------------------------
def direction( ): 
    #retorna la dirección en que se va a mover una particula
    return choice([(1,0), (-1,0), (0,1), (0,-1)] ) 


def check_trace(pos, s, h, T, ind_tmp, N ):
    #revisa si una cierta posicion ha sido ocupada. Si no, se la agrega a la traza usando
    #np.append()
    
    r= np.random.uniform(0,1) 
   
    if r< s*h: 
    #Si el número aleatorio escogido es menor que esa cantidad, hay ramificación
    #como nos ramificamos, podemos ocupar 2 espacios, por lo que definimos dos nuevas POSIBLES
    #ubicaciones. 
    
        pos_1 = pos +  direction( )  
        pos_2 = pos + direction()
        
        #Debemos ver ahora si estas posiciones han sido ya ocupadas. Si lo están, no hacemos
        #nada. Y si no está, agregamos una partícula, actualizamos el índice de particulas
        #activas y la traza, que nos indicará cuales espacios se han ocupado. 
        
        #Debemos hacer esto para cada nueva posicion
        
        if pos_1.all in T == True: 
            pass 
        
        else : 
            N+= 1
            ind_tmp.append(N) #aqui agregamos el indice de la particula activa nueva 
            T = np.append(T, pos_1, axis= 0 )  #y agregamos a la traza la posicion ocupada
        
        if pos_2.all in T == True: 
            pass 
        
        else : 
            N+= 1
            ind_tmp.append(N) #aqui agregamos el indice de la particula activa nueva 
            T = np.append(T, pos_2, axis= 0 )  #y agregamos a la traza la posicion ocupada
            
        #Ahora, si no nos ramificamos, tenemos que saltar (movernos). Hacemos entonces
        #el mismo procedimiento anterior.
        
    else :       
        pos +=  direction( )
        
        if pos.all in T == True: 
            pass 
        
        else : 
            N+= 1
            ind_tmp.append(N) #aqui agregamos el indice de la particula activa nueva 
            T = np.append(T, pos, axis= 0 )
    ind_part_activas = ind_tmp 
    
    
    #Después de haber revisado para todas las posiciones, la función nos entrega la nueva
    #traza y una lista con los indices de la tarza que están activos. 
    
    return [ind_part_activas, T]


#----------------------------VEAMOS SI FUNCIONAAAAAAAAAA T-T -------------------------------


while t< tmax: 
    t += 0.1
    
    for i in ind_part_activas: 
        check_trace(pos= T[i], s= 0.8, h= 0.1, T= T, ind_tmp= [], N= 1)
        
        print()


plt.scatter(T.T[0], T.T[1])

#no funciona T-T. Grafica un puro punto aaaaaaaaa
