# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 14:52:49 2023

@author: sepul
"""

import numpy as np
import matplotlib.pyplot as plt
from random import choice
import networkx as nx


#---------------------------------DATOS DEL PROBLEMA--------------------------------------------------

tmax= 5 #tiempo maximo de simulacion
t= 0 #tiempo inicial 
h= 1 #paso de tiempo
s= 0.9


#-----------------------------ARREGLOS PARA GUARDAR DATOS---------------------------------------------

edges=np.empty([0, 2])

T = np.array([[0,0]]) #define las posiciones ocupadas por cada particula

pos= np.array([0, 0]) # posicion de las particulas que se van añadiendo 

ind_part_activas= np.array([0]) #define el indice de la posicion de las particulas activas en T
N= 0
G= nx.Graph()
#%% 
#----------------------------FUNCIONES A USAR-----------------------------------------------
def direction( ): 
    
    '''retorna la dirección en que se va a mover una particula''' 
    #esto hay que mejorarlo para que la particula no vuelva por donde vino
    
    return choice([(1,0), (-1,0), (0,1), (0,-1)] ) 
#end_directionbt

#%%
def isintrace(pos, trace):
    
    ''' Chequea si el elemento pos, correspondiente al par ordenado que denota la posicion de una particula
    nueva se ecuentra ya en la traza. '''
    
    for i in trace:
        if np.array_equal(pos, i):
            return True
    return False

#%% 
def edge_list( G, edges, T, source, target):
    
    ''' Esta funcion toma el grafo G, las posiciones de los nodos (que corresponde simplemente a la traza)
    y la direccion  en la que se genera la arista 'edge' ; desde source hasta target. 
    
    Recordar que np.append junta un array con un valor en un eje especificado.Por
    lo tanto, se le debe entregar las coordenadas en arreglos, como Trace.
    Edges tiene que ser un arreglo al que le vamos anexando conexiones e indica las conexiones que se hacen 
    de acuerdo a los indices de traza.  
    
    Source y target son indices de los nodos en Traza'''
    
    nodes_pos= T[source] #?? <==> T[source, :] entregará un par ordenado con las coordenadas de source
    #así, iremos desde source hasta target
    
    edges= np.append (edges, np.array([ [source, target] ]) , axis=0)
    
    G.add_node(target, pos= (nodes_pos[0], nodes_pos[1])) #añade un nodo con coordenadas x, y de source
    #revisar linea 72
    return G, edges 
# end edge_list
#%% 

def action(G, edges, nodes_pos, pos, Trace, ind_tmp, N):
    
    ''' Toma un grafo G y un arreglo edges que indica las conexiones que se van dando entre los nodos 
    indexados. Pos corresponde a la nueva posicion de la particula que decide moverse, por lo que corresponde
    a un par odenado (x,y), y Trace el arreglo de todas las posiciones que se han ocupado. Además
    nodes_pos es el índice que indica la ubicacion del nodo en la traza.
    
    Por ultimo, ind_tmp y N son los indices de las particulas temporalmente activas y el numero de particulas, 
    respectivamente. ''' 
    

    pos += direction()
    if isintrace(pos, Trace):
        pass 
   
    else : 

        ind_tmp.append(N) #anexamos el indice activo a la enésima partícula 
        
        Trace= np.concatenate((Trace, [pos]), axis=0)
        N += 1
        

            
    G, edges= edge_list(G, edges, T, nodes_pos, N ) #source es un indice de la traza, y target tambien
    
  #nodes_pos es un indice 
            
         
    return G, Trace, N, edges #ind_part_activas 

#end_action
        
 #%%        
  
#--------------------------------- MAIN CODE---------------------------------------------------------
while t < tmax  and len(ind_part_activas) >0  :
    
    
    t += h # tiempo= tiempo+ h
    ind_tmp = [] #guarda una posicion temporal que debe ser verificada en la traza
    

    for i in np.random.permutation(ind_part_activas) : 
        
         
        r= np.random.uniform(0,1) 
        
        nodes_pos= T[i] #aqui esto no es un indice , y debería serlo

        if r< s:
        
            G, T, N, edges = action(G, edges, nodes_pos, pos, T, ind_tmp, N)
            G, T, N, edges = action(G, edges, nodes_pos, pos, T, ind_tmp, N)
            
        else:
        
            G, T, N, edges =  action(G, edges, nodes_pos, pos, T, ind_tmp, N)
            
    ind_part_activas = ind_tmp
    
#%%
for i in range(len( T[:,0] ) ) : 
    G.add_node(i, pos= (T[i,0], T[i,1]))

#%%
x= nx.get_node_attributes(G, 'pos')

nx.draw(G, x)
