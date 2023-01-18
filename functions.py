# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 10:34:01 2023

@author: sepul
"""

import networkx as nx
import random
import numpy as np
from random import choice
from numba import njit
#----------------------------FUNCIONES A USAR-----------------------------------------------

def isintrace(pos, trace):
    
    ''' Chequea si el elemento pos, correspondiente al par ordenado que denota la posicion de una particula
    nueva se ecuentra ya en la traza. '''
    
    # for i in trace:
    #     if np.allclose(pos, i, rtol= 1e-3):
    #         return True
    # return False
    #print(pos-trace)
    bools = np.sum(np.abs(pos-trace), axis=1) <= 1e-3
    return np.sum(bools) > 0


#%% 
def boundary(origen, position, r_max): 
    
    ''' Calcula el radio máximo del movimiento como la máxima distancia que puede
    moverse la partícula en línea recta durante el tiempo de la simulación . Luego,
    calcula la distancia desde el origen a la posicion de la partícula que
    se movió (la entregada por direction). Si dicha distancia es menor al radio máximo, retorna True. '''
    
    #print('la posicion elegida por direction es', position)
    origen= np.array([0,0])
    distancia= np.hypot( position[0]- origen[0], position[1]- origen[1])
    
    #np.hypot caclula la hipotenusa entre dos puntos; en el espacio euclideo es igual a la norma uwu
    #print('y la distancia del origen a la posicion es', distancia)
    
    #distancia= dist(origen, position)
    # if bc==0: 
    #     bc_flag= 0
    # elif bc== 1: 
    #     bc_flag= 
    if distancia <= r_max :
        return True 
    
    return False
#%%
def direction(pos, Trace): 
    
    ''' Le da una dirección de movimiento a las partículas a partir de la posicion de la particula
    que va a moverse pos, revisando los vecinos mas cercanos de la partícula en ese momento, cuyas posiciones
    son dadas por pos_tmp. Luego, anexa en una matriz las posiciones que no están ocupadas revisando la
    traza Trace. Finalmente elige al azar una posicion de la matriz.'''
    
    origen= np.array([0,0])
    opciones = np.array([[1,0] , [-1,0], [1/2, np.sqrt(3)/2], [-1/2, np.sqrt(3)/2], [-1/2, -np.sqrt(3)/2],
                          [1/2, -np.sqrt(3)/2]] ) #genera un hexagono 
    #opciones = np.array([[1,0] , [-1,0], [0,1], [0,-1] ] )
                         
                       
    pos_tmp = pos + opciones 
    posibles = []
    
  
    for neighbor in pos_tmp:
        
        if isintrace(neighbor, Trace): #or boundary(origen, pos_tmp, tmax, h):
            pass

        else: 
            posibles.append(neighbor)
            #print('y las que podriamos ocupar son' ,posibles)
    if np.any(posibles):
        
        posicion = choice(posibles)
        #print('elegimos', posicion)
        
        if boundary(origen , posicion , 25):
            return posicion
    
    return []
#end_direction


        
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
    #print('la posicion arrojada es',pos_tmp)
    
    #print('la posicion nueva es', pos_tmp)
    
    if np.any(pos_tmp):
        #si es que hay algun elemento elegido, lo agregamos a traza. Después hay que ver si ese punto
        #cunple con la condicion de borde 
        Trace= np.concatenate( (Trace, [pos_tmp]) , axis=0)
        N += 1
        #print(N)
        ind_tmp.append(N) #anexamos el indice activo a la enésima partícula
        
        edges= edge_list(edges, Trace, i, N ) #source es un indice de la traza, y target tambien
        G.add_node(N, pos= (pos_tmp[0], pos_tmp[1]))
        
  #nodes_pos es un indice 
            
         
    return G, Trace, N, edges, ind_tmp #ind_part_activas 

#end_action
    
#%% 
def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.  
    Licensed under Creative Commons Attribution-Share Alike 
    
    If the graph is a tree this will return the positions to plot this in a 
    hierarchical layout.
    
    G: the graph (must be a tree)
    
    root: the root node of current branch 
    - if the tree is directed and this is not given, 
      the root will be found and used
    - if the tree is directed and this is given, then 
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given, 
      then a random choice will be used.
    
    width: horizontal space allocated for this branch - avoids overlap with other branches
    
    vert_gap: gap between levels of hierarchy
    
    vert_loc: vertical location of root
    
    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))
            
    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''
    
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos

            
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

#G= nx.read_gpickle('myGraph.gpickle')

#nx.draw(G, tree, node_color= 'red', node_size= 10)

#%% 
def clean(G): 
    '''  Toma un grafo G y saca los nodos que tienen grado dos, quitando también las
    conexiones entre esos nodos'''
    import copy 
    copia= copy.copy(G)
    nodos= G.nodes
   
    
    for i in range(len(copia.nodes)): 
        
        if copia.degree(i)== 2: 
            neighbours = [n for n in copia[i]]
            copia.add_edge(neighbours[0], neighbours[1])
            copia.remove_node(i)

        else: 
            pass 
            
    return  nodos , copia  

#%%
#necesitamos hacer una funcion que junte todos los diccionarios con nodos, y despues haga el histograma
#con eso 



# def analisis(G):
#     from collections import Counter 
#     for g in range(1000): 
#         degrees= dict(Counter(Gi.degrees)+ Counter(degrees_2))

# def histogram(G): 
    
    
#    degree_sequence= sorted([d for n,d in G.degree()], reverse=True)
   
#    from collections import Counter
#    import matplotlib.pyplot as plt

#    ndegree= Counter(degree_sequence)
#    deg, cnt = zip(*ndegree.items())
#    plt.title('Node degree distribution')
#    plt.xlabel(r'Node degree $k$ ')
#    plt.ylabel(r'Distribution $\mathcal{P(k)}$')
#    plot= plt.bar(deg, cnt, width=0.80, color='b')
   
#    return plot 

