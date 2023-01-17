# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 18:50:35 2023

@author: sepul
"""


import numpy as np
import matplotlib.pyplot as plt
from random import choice
import networkx as nx
from math import dist

from tree_thingy  import * 

#%%
#---------------------------------DATOS DEL PROBLEMA--------------------------------------------------

tmax= 10#tiempo maximo de simulacion
t= 0 #tiempo inicial 
h= 1 #paso de tiempo
s= 1.0


#-----------------------------ARREGLOS PARA GUARDAR DATOS---------------------------------------------

edges =np.empty([0, 2])

T = np.array([[0,0]]) 

pos= np.array([ 0, 0]) # posicion de las particulas que se van añadiendo/ [Indice, (par ordenado)] 

ind_part_activas= np.array([0]) #define el indice de la posicion de las particulas activas en T
N= 0


G= nx.Graph()
G.add_node(0, pos= (0,0))
#%% 
#----------------------------FUNCIONES A USAR-----------------------------------------------

def isintrace(pos, trace):
    
    ''' Chequea si el elemento pos, correspondiente al par ordenado que denota la posicion de una particula
    nueva se ecuentra ya en la traza. '''
    
    for i in trace:
        if np.allclose(pos, i, rtol= 1e-3):
            return True
    return False
#%% 
def direction(pos, Trace): 
    
    ''' Le da una dirección de movimiento a las partículas a partir de la posicion de la particula
    que va a moverse pos, revisando los vecinos mas cercanos de la partícula en ese momento, cuyas posiciones
    son dadas por pos_tmp. Luego, anexa en una matriz las posiciones que no están ocupadas revisando la
    traza Trace. Finalmente elige al azar una posicion de la matriz.'''
    
    opciones = np.array([[1,0] , [-1,0], [1/2, np.sqrt(3)/2], [-1/2, np.sqrt(3)/2], [-1/2, -np.sqrt(3)/2],
                          [1/2, -np.sqrt(3)/2]] ) #genera un hexagono 
    #opciones = np.array([[1,0] , [-1,0], [0,1], [0,-1] ] )
                         
                       
    pos_tmp = pos + opciones 
    posibles = []
    
  
    for neighbor in pos_tmp:
        
        if isintrace(neighbor, Trace):
            pass

        else: 
            posibles.append(neighbor)
            #print('y las que podriamos ocupar son' ,posibles)
    if np.any(posibles):
        
        posicion = choice(posibles)
        #print('elegimos', posicion)
        return posicion
    else:
        return []
#end_direction

#%% 
def boundary(origen, position, max_time, h): 
    ''' Calcula el radio máximo del movimiento como la máxima distancia que puede
    moverse la partícula en línea recta durante el tiempo de la simulación. Luego,
   calcula la distancia desde el origen a la posicion de la partícula que
    se va a mover. Si dicha distancia es mayor o igual al radio maxímo, se elimina
    la posicion nueva a la que se iba a mover. '''
    r_max= max_time/h 
    if dist(origen, position) >= r_max :
        np.delete(position)
        
        

#%%
def revivir(Trace,ind_part_activas,ind_tmp): 
    ''' Revisa la posición de la partícula que quedó activa y ve si tiene espacio dis-
    ponible'''
    
    for i in ind_part_activas: 
        revisar= Trace[i]
        r= direction(revisar, Trace)
        if len(r) > 0: 
            ind_tmp.append(i)
    return ind_tmp
        
 
#%% 
def edge_list(edges, T, source, target):
    
    ''' Esta funcion toma las posiciones de los nodos (que corresponde simplemente 
    a la traza) y la direccion  en la que se genera la arista 'edge' ; desde source hasta target. 
    
    Recordar que np.append junta un array con un valor en un eje especificado.Por
    lo tanto, se le debe entregar las coordenadas en arreglos, como Trace.
    Edges tiene que ser un arreglo al que le vamos anexando conexiones e indica las conexiones que se hacen 
    de acuerdo a los indices de traza.  
    
    Source y target son indices de los nodos en Traza. Serán la i-esima particula moviendose
     y N, respectivamente.'''
    
    edges= np.append (edges, np.array([ [source, target] ]) , axis=0)
   

    #print(target)
    #el arreglo (source, target) debe ser (indice en traza(source), N)

    return  edges 
# end edge_list
#%% 

def action(G, edges, pos, Trace, ind_tmp, i, N):
    
    ''' Toma un grafo G y un arreglo edges que indica las conexiones que se van dando entre los nodos 
    indexados. Pos corresponde a la posicion de la particula que decide moverse(que debe entregar direction)
    por lo que corresponde
    a un par odenado (x,y), y Trace el arreglo de todas las posiciones que se han ocupado. 
    Además,  ind_tmp son los indices de las particulas temporalmente activas. 
    
    Por ultimo i, N son los índices de las partículas fuente y objetivo en las que se generan
    las conexiones, respectivamente. ''' 
    
    pos_tmp = np.copy(pos)
    pos_tmp= direction(pos, Trace)# direction revisa las posiciones posibles y elige una que no está en la traza
    
    #print('la posicion nueva es', pos_tmp)
    if np.any(pos_tmp):
        Trace= np.concatenate( (Trace, [pos_tmp]) , axis=0)
        N += 1
        #print(N)
        ind_tmp.append(N) #anexamos el indice activo a la enésima partícula
        
        edges= edge_list(edges, T, i, N ) #source es un indice de la traza, y target tambien
        G.add_node(N, pos= (pos_tmp[0], pos_tmp[1]))
        
  #nodes_pos es un indice 
            
         
    return G, Trace, N, edges, ind_tmp #ind_part_activas 

#end_action
        
 #%%        
  
#--------------------------------- MAIN CODE---------------------------------------------------------



while t < tmax  and len(ind_part_activas) >0  :
    
    
    t += h # tiempo= tiempo+ h
    ind_tmp = [] #guarda una posicion temporal que debe ser verificada en la traza
    
    randperms = np.random.permutation(ind_part_activas)
    
    for i in randperms:
        
         
        r= np.random.uniform(0,1) 
        
       # nodes_pos= T[i][0] #aqui esto no es un indice , y debería serlo
       
        #pos= np.array(T[i])
        pos= T[i]
        
        #voy a cambiar nodes_position por i
        if r < s:
            
            #def action(G, edges, pos, Trace, ind_tmp, i, N):
        
            G, T, N, edges, ind_tmp = action(G, edges, pos, T, ind_tmp,i, N)
            G, T, N, edges, ind_tmp = action(G, edges, pos, T, ind_tmp,i, N)
        else:
        
            G, T, N, edges, ind_tmp =  action(G, edges, pos, T, ind_tmp,i, N)
            
    ind_tmp= revivir(T ,ind_part_activas,ind_tmp)
       
    ind_part_activas = ind_tmp
         
plt.figure(figsize=(9,9))
plt.axis('equal')   
   
plt.scatter(T[:,0], T[:,1], c= 'grey', alpha= 0.0)
plt.scatter(T[ind_part_activas][:,0], T[ind_part_activas][:,1], c= 'red', alpha= 0.8)

x= nx.get_node_attributes(G, 'pos')

G.add_edges_from(edges)

nx.draw_networkx_nodes(G,x, node_shape='.', node_size=0.0, alpha= 0 )
nx.draw_networkx_edges(G,x)

     
plt.show()

#%% 
nx.write_gpickle(G,'myGraph.gpickle')


nodos, copia = clean(G)


tree= hierarchy_pos(G, 0)
nx.draw(G, tree, node_color= 'red', node_size= 10)

