# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 12:00:47 2023

@author: sepul
"""

#i'll try to do the random walk. Then, the non-backtracking random walk

import numpy as np
import matplotlib.pyplot as plt
from random import choice


def direction( ): 
    #retorna la dirección en que se va a mover una particula
    #esto hay que mejorarlo para que la particula no vuelva por donde vino
    
    return choice([(1,0), (-1,0), (0,1), (0,-1)] ) 

def action(pos, Trace, N):
    
    pos += direction()
    
    N+= 1   
    Trace= np.concatenate((Trace, [pos]), axis=0)
      
    return Trace, N

T= np.array([[0,0]])
N=0 

for i in range(10000): 
    
    pos = np.array(T[i])  
    T, N = action(pos, T, N )
print(T, N)

plt.plot(T[:,0], T[:,1])

            
