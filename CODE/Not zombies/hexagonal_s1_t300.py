# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 18:50:35 2023

@author: sepul
"""


import numpy as np
import networkx as nx
from tqdm import trange
import functions_s1 as functions

from datetime import datetime

# import copy, cProfile, pstats, io
# from pstats import SortKey
# pr = cProfile.Profile() # Descomentar lineas para utilizar.


tmax= 30#tiempo maximo de simulacion
t= 0.0 #tiempo inicial 
h= 1 #paso de tiempo
s= 1.0
    

#%%
start_time = datetime.now()
#---------------------------------DATOS DEL PROBLEMA--------------------------------------------------

#for n in range(1): 

    
    #--------------------------------- MAIN CODE---------------------------------------------------------
    
edges =np.empty([0, 2])

origen= np.array( [0,0])

T = np.array([[0,0]]) 
pos= np.array([ 0, 0]) # posicion de las particulas que se van añadiendo/ [Indice, (par ordenado)] 

ind_part_activas= np.array([0]) #define el indice de la posicion de las particulas activas en T

N= 0


G= nx.Graph()
G.add_node(0, pos= (0,0))
t = 0


# for q in trange(int(tmax/h)):
    
while t < tmax  and len(ind_part_activas) >0  :
    # if not len(ind_part_activas) >0:
    #     break
    ind_tmp = []
    # t = q*h

    #t += h # tiempo= tiempo+ h
   
    
    randperms = np.random.permutation(ind_part_activas)
    

    
    ind_mover= np.random.choice(ind_part_activas) 

    r= np.random.uniform(0,1) 

    pos= T[ind_mover]
    N_activas= len(ind_part_activas)

    
    if r < 1 :
        
    
        G, T, N, edges, ind_tmp = functions.action(G, edges, pos, T, ind_tmp,ind_mover, N)
        G, T, N, edges, ind_tmp = functions.action(G, edges, pos, T, ind_tmp,ind_mover, N)
    else:
    
        G, T, N, edges, ind_tmp =  functions.action(G, edges, pos, T, ind_tmp,ind_mover, N)

    
    #print('el indice temporal es ',ind_tmp)
    
    ind_part_activas=np.append(ind_part_activas,ind_tmp).astype(int)

    ind_part_activas=np.delete(ind_part_activas, np.where(ind_part_activas == ind_mover)) 
        
    #print('el indice de activas es', ind_part_activas)
    
    G.add_edges_from(edges)
    
    np.savetxt('indactivas_red_not_zombie_prueba.txt', ind_part_activas, delimiter= ' ')
    np.savetxt('Traza_red_not_zombie_prueba.txt', T, delimiter= ' ')
    
    nx.write_gpickle(G,'Grafo_not_zombie_prueba.gpickle')

end_time = datetime.now()
    
print('Duration: {}'.format(end_time - start_time))







