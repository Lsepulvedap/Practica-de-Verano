# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 18:50:35 2023

@author: sepul
"""


import numpy as np
import networkx as nx

import functions 

#from datetime import datetime
# import copy, cProfile, pstats, io
# from pstats import SortKey
# pr = cProfile.Profile() # Descomentar lineas para utilizar.
#start_time = datetime.now()

#%%
#---------------------------------DATOS DEL PROBLEMA--------------------------------------------------

tmax= 300 #tiempo maximo de simulacion
t= 0 #tiempo inicial 
h= 1 #paso de tiempo
s= 0.0



  
  
#--------------------------------- MAIN CODE---------------------------------------------------------


#pr.enable() # Activas el profiler

for n in range(2): 
    #-----------------------------ARREGLOS PARA GUARDAR DATOS---------------------------------------------

    edges =np.empty([0, 2])
    
    origen= np.array( [0,0])
    
    T = np.array([[0,0]]) 
    pos= np.array([ 0, 0]) # posicion de las particulas que se van añadiendo/ [Indice, (par ordenado)] 
    
    ind_part_activas= np.array([0]) #define el indice de la posicion de las particulas activas en T
    N= 0
    
    
    G= nx.Graph()
    G.add_node(0, pos= (0,0))
    
    while t < tmax  and len(ind_part_activas) >0  :
        
        
        t += h # tiempo= tiempo+ h
        ind_tmp = [] #guarda una posicion temporal que debe ser verificada en la traza
        
        randperms = np.random.permutation(ind_part_activas)
        
        for i in randperms:
            
             
            r= np.random.uniform(0,1) 
            
            pos= T[i]
            
            #voy a cambiar nodes_position por i
            if r < s:
                
                #def action(G, edges, pos, Trace, ind_tmp, i, N):
            
                G, T, N, edges, ind_tmp = functions.action(G, edges, pos, T, ind_tmp,i, N)
                G, T, N, edges, ind_tmp = functions.action(G, edges, pos, T, ind_tmp,i, N)
            else:
            
                G, T, N, edges, ind_tmp =  functions.action(G, edges, pos, T, ind_tmp,i, N)
                
        ind_tmp= functions.revivir(T ,ind_part_activas,ind_tmp)
           
        ind_part_activas = ind_tmp
        G.add_edges_from(edges)
        
    #nx.write_gpickle(G, 'Graph'+str(n)+'.gpickle')
    
    nx.write_gpickle(G,'Graph%i.gpickle'%n)
    #nx.write_gpickle(G, 'Graph_prueba1.gpickle')
    
        # pr.disable() # Desactivas el profiler
        # s = io.StringIO()
        # sortby = SortKey.CUMULATIVE
        # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        # ps.print_stats()
        
        # with open('test.txt', 'w+') as f: # Guardas los resultados en un .txt
        #     f.write(s.getvalue())
    #end_time = datetime.now()
#print('Duration: {}'.format(end_time - start_time))

#%%        


