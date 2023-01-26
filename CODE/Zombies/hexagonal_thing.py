# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 18:50:35 2023

@author: sepul
"""


import numpy as np
import networkx as nx

import functions 

from datetime import datetime

# import copy, cProfile, pstats, io
# from pstats import SortKey
# pr = cProfile.Profile() # Descomentar lineas para utilizar.
start_time = datetime.now()

#%%
#---------------------------------DATOS DEL PROBLEMA--------------------------------------------------

tmax= 100#tiempo maximo de simulacion
t= 0.0 #tiempo inicial 
h= 0.1 #paso de tiempo
s= 0.0



  
  
#--------------------------------- MAIN CODE---------------------------------------------------------


#pr.enable() # Activas el profiler

# for n in range(1): 
#     #-----------------------------ARREGLOS PARA GUARDAR DATOS---------------------------------------------

edges =np.empty([0, 2])

origen= np.array( [0,0])

T = np.array([[0,0]]) 
pos= np.array([ 0, 0]) # posicion de las particulas que se van añadiendo/ [Indice, (par ordenado)] 

ind_part_activas= np.array([0]) #define el indice de la posicion de las particulas activas en T

N= 0


G= nx.Graph()
G.add_node(0, pos= (0,0))
t = 0

while t < tmax  and len(ind_part_activas) >0  :
    
    
    t += h # tiempo= tiempo+ h
    ind_tmp = [] #guarda una posicion temporal que debe ser verificada en la traza
    
    randperms = np.random.permutation(ind_part_activas)
    
    #for i in randperms:
        
    ind_mover= np.random.choice(randperms) 
    r= np.random.uniform(0,1) 
    
    
    pos= T[ind_mover]
    N_activas= len(ind_part_activas)
    
    probabilidad= 1- np.exp(-s* N_activas* h)
    
    if probabilidad < 0.5: 
        if r < probabilidad :
            
            #def action(G, edges, pos, Trace, ind_tmp, i, N):
        
            G, T, N, edges, ind_tmp = functions.action(G, edges, pos, T, ind_tmp,ind_mover, N)
            G, T, N, edges, ind_tmp = functions.action(G, edges, pos, T, ind_tmp,ind_mover, N)
        else:
        
            G, T, N, edges, ind_tmp =  functions.action(G, edges, pos, T, ind_tmp,ind_mover, N)
            
    else: 
        print(r'Revisa $\Delta t$!')
        break 
        
    ind_tmp= functions.revivir(T, ind_part_activas, ind_tmp)
       
    ind_part_activas = ind_tmp
    
    G.add_edges_from(edges)
    
    nx.write_gpickle(G, 'grafo_prueba.gpickle')   
    #np.savetxt('traza_grafo_prueba',T )
    #nx.write_gpickle(G, 'Graph'+str(n)+'.gpickle')
    
   # nx.write_gpickle(G,'Grafos_prueba.gpickle'%n)
    #nx.write_gpickle(G, 'Graph_prueba1.gpickle')
        
            # pr.disable() # Desactivas el profiler
            # s = io.StringIO()
            # sortby = SortKey.CUMULATIVE
            # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            # ps.print_stats()
            
            # with open('test.txt', 'w+') as f: # Guardas los resultados en un .txt
            #     f.write(s.getvalue())
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))






