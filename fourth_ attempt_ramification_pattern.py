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

tmax= 10 #tiempo maximo de simulacion
t= 0 #tiempo inicial 
h= 1 #paso de tiempo
s= 1


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
def direction(): 
    
    '''retorna la dirección en que se va a mover una particula''' 
    #Esto hay que mejorarlo para que la particula no vuelva por donde vino. Para esto hay que 
    #hacer que se revisen los vecinos mas cercanos. Cuando encuentra posiciones desocupadas
    #elige una (o dos, dependiendo si se ramifica o se mueve) al azar. 
 
    
    
    return choice([(1,0), (-1,0), (0,1), (0,-1)] ) 
#end_directionbt.........................................................................................................................


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
    
    ''' Esta funcion toma el grafo G, las posiciones de los nodos (que corresponde simplemente 
    a la traza) y la direccion  en la que se genera la arista 'edge' ; desde source hasta target. 
    
    Recordar que np.append junta un array con un valor en un eje especificado.Por
    lo tanto, se le debe entregar las coordenadas en arreglos, como Trace.
    Edges tiene que ser un arreglo al que le vamos anexando conexiones e indica las conexiones que se hacen 
    de acuerdo a los indices de traza.  
    
    Source y target son indices de los nodos en Traza. Serán la i-esima particula moviendose
     y N, respectivamente.'''
    
    edges= np.append (edges, np.array([ [source, target] ]) , axis=0)
    print(target)
    #el arreglo (source, target) debe ser (indice en traza(source), N)

    return G, edges 
# end edge_list
#%% 

def action(G, edges, pos, Trace, ind_tmp, i, N):
    
    ''' Toma un grafo G y un arreglo edges que indica las conexiones que se van dando entre los nodos 
    indexados. Pos corresponde a la nueva posicion de la particula que decide moverse, por lo que corresponde
    a un par odenado (x,y), y Trace el arreglo de todas las posiciones que se han ocupado. 
    Además,  ind_tmp son los indices de las particulas temporalmente activas. 
    
    Por ultimo i, N son los índices de las partículas fuente y objetivo en las que se generan
    las conexiones, respectivamente. ''' 
    pos_tmp = np.copy(pos)
    pos_tmp += direction()
    
    if isintrace(pos_tmp, Trace):
        pass 
    else : 
        
        Trace= np.concatenate((Trace, [pos_tmp]), axis=0)
        N += 1
        print(N)
        ind_tmp.append(N) #anexamos el indice activo a la enésima partícula
        G, edges= edge_list(G, edges, T, i, N ) #source es un indice de la traza, y target tambien
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
       
        pos= np.array(T[i])
        
        #voy a cambiar nodes_position por i
        if r < s:
            
            #def action(G, edges, pos, Trace, ind_tmp, i, N):
        
            G, T, N, edges, ind_tmp = action(G, edges, pos, T, ind_tmp,i, N)
            G, T, N, edges, ind_tmp = action(G, edges, pos, T, ind_tmp,i, N)
            
        else:
        
            G, T, N, edges, ind_tmp =  action(G, edges, pos, T, ind_tmp,i, N)
            
    ind_part_activas = ind_tmp
    #%% 
for i in range(len(T[:,0])): 
    plt.scatter(T[:,0], T[:,1], label= i)
# #%%
# for i in range(len( T[:,0] ) ) : 
#     G.add_node(i, pos= (T[i,0], T[i,1]))

#%%
x= nx.get_node_attributes(G, 'pos')
G.add_edges_from(edges)
nx.draw(G, x, with_labels= True)
plt.axis('equal')
#ya que la i-esima particula es la que salta, le puedo entregar como source a i. Luego, target es N
