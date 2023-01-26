# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 22:08:16 2023

@author: sepul
"""

import numpy as np
from random import choice


Trace= np.array([[0,1], [0,-1], [5,6]])
pos= np.array([[0,0]])
 
def direction(pos, Trace): 
    
    opciones = np.array([ [1,0] , [-1,0], [0,1], [0,-1] ] )

    a= pos+ opciones[0] 
    b=  pos+ opciones[1]
    c=  pos+ opciones[2]
    d =  pos+ opciones[3] 

    pos_tmp= np.concatenate((a,b,c,d) , axis=0)
   
    
    print('las posiciones temporales son', pos_tmp) #esto no está entregando un array
    print(pos_tmp.dtype) 
    
    empty= np.empty([0,2])
    
    for i in range(4):
        if not (pos_tmp[i] in Trace[:]) :
            
            #print(pos_tmp[i] )
            
            posible= np.concatenate( (empty, pos_tmp[i]), axis=0)
            
            print('mientras que las posibles son', posible)
          
            empty= posible 
            
            posicion= choice(empty)
            
        else: 
            pass
        print('aqui se acaba el' , i, '-esimo loop')
    return posicion
            
#%% 


posicion= direction(pos, Trace)
print(posicion)
