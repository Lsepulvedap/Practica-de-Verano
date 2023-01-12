# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 21:49:01 2023

@author: sepul
"""

import numpy as np
from random import choice

T= np.array([[1,2], [3,4], [5,6]])
xi= np.array([[1,1]])


def direction(pos, Trace): 
    
    opciones = np.array([[1,0] , [-1,0], [0,1], [0,-1] ] )
    pos_tmp =  np.array([ pos+ opciones[0] , pos+ opciones[1], pos+ opciones[2], pos+ opciones[3] ])
    print('las posiciones temporales son ',pos_tmp)
  
    for i in range(4):
        
        if np.array_equal(Trace[:], pos_tmp[i]):
            
            np.delete(pos_tmp[i])
            
            posibles = pos_tmp 
            print('y las posibles son' ,posibles) #deberia siempre darme algo de 3 o menos filas
            
            posicion= choice(posibles)
            print('elegimos', posicion)
        else: 
            posicion= choice(pos_tmp) #solo pasará para la primera particula 
    
    return posicion
            
#%% 

x= direction(xi, T)
print(x)
            
            
    
    