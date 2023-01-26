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
import matplotlib.pyplot as plt
from collections import Counter
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
    pos_tmp= direction(pos_tmp, Trace)# direction revisa las posiciones posibles y elige una que no está en la traza
   
    if np.any(pos_tmp):
        #si es que hay algun elemento elegido, lo agregamos a traza. Después hay que ver si ese punto
        #cumple con la condicion de borde 
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
        
        if copia.degree(i)== 2 and i != 0: 
            neighbours = [n for n in copia[i]]
            copia.add_edge(neighbours[0], neighbours[1])
            copia.remove_node(i)

        else: 
            pass 
            
    return  nodos , copia  

#%%

    
def degree_distribution(nfiles): 
    
    degrees = np.zeros((nfiles,6))
    for n in range(nfiles):
        filename= 'Graph%i_not_zombie.gpickle' % n
        
        G = nx.read_gpickle(filename)
        
        #_,G = clean(G)
        degree_sequence= sorted([d for n,d in G.degree()], reverse=True)
        
        ndegree= Counter(degree_sequence)
        deg, cnt = zip(*ndegree.items())
        
        for i in range(len(deg)):
            degrees[n, deg[i]-1] = cnt[i]
            
    total_histogram = np.sum(degrees, axis=0)
    
    normalized= total_histogram/np.sum(total_histogram)
    #cum_total_histogram = np.cumsum(total_histogram)
    x= np.arange(1,7)
    
    plt.style.use('bmh')
    plt.grid(False) 
    #plt.title('Distribución de grados', fontsize=18,fontname= "Arial")
    plt.xlabel(r'$k$ ', fontsize=15,fontname= "Arial")
    plt.ylabel(r' $\mathcal{P}(k)$', fontsize=15,fontname= "Arial")
    #plt.yscale('log')
    

    plot_1= plt.bar(x,normalized, color= 'crimson')

    
    return plot_1

#end degree_distribution



#%% 


def topological_generations(G):
    """Stratifies a DAG into generations.

    A topological generation is node collection in which ancestors of a node in each
    generation are guaranteed to be in a previous generation, and any descendants of
    a node are guaranteed to be in a following generation. Nodes are guaranteed to
    be in the earliest possible generation that they can belong to.

    Parameters
    ----------
    G : NetworkX digraph
        A directed acyclic graph (DAG)

    Yields
    ------
    sets of nodes
        Yields sets of nodes representing each generation.

    Raises
    ------
    NetworkXError
        Generations are defined for directed graphs only. If the graph
        `G` is undirected, a :exc:`NetworkXError` is raised.

    NetworkXUnfeasible
        If `G` is not a directed acyclic graph (DAG) no topological generations
        exist and a :exc:`NetworkXUnfeasible` exception is raised.  This can also
        be raised if `G` is changed while the returned iterator is being processed

    RuntimeError
        If `G` is changed while the returned iterator is being processed.

    Examples
    --------
    >>> DG = nx.DiGraph([(2, 1), (3, 1)])
    >>> [sorted(generation) for generation in nx.topological_generations(DG)]
    [[2, 3], [1]]

    Notes
    -----
    The generation in which a node resides can also be determined by taking the
    max-path-distance from the node to the farthest leaf node. That value can
    be obtained with this function using `enumerate(topological_generations(G))`.

    See also
    --------
    topological_sort
    """
    if not G.is_directed():
        raise nx.NetworkXError("Topological sort not defined on undirected graphs.")

    multigraph = G.is_multigraph()
    indegree_map = {v: d for v, d in G.in_degree() if d > 0}
    zero_indegree = [v for v, d in G.in_degree() if d == 0]

    while zero_indegree:
        this_generation = zero_indegree
        zero_indegree = []
        for node in this_generation:
            if node not in G:
                raise RuntimeError("Graph changed during iteration")
            for child in G.neighbors(node):
                try:
                    indegree_map[child] -= len(G[node][child]) if multigraph else 1
                except KeyError as err:
                    raise RuntimeError("Graph changed during iteration") from err
                if indegree_map[child] == 0:
                    zero_indegree.append(child)
                    del indegree_map[child]
        yield this_generation

    if indegree_map:
        raise nx.NetworkXUnfeasible(
            "Graph contains a cycle or graph changed during iteration"
        )
        
#%% 

def generar_arboles(nfiles):
    ''' Genera una lista de subarboles dirigidos a partir de cada grafo.'''
  
    arboles= []
    
    for n in range(nfiles): 
        #esta primera parte genera una lista de los arboles de todos los grafos, partiendo desde el nodo 0
        
        filename= 'Graph%i_not_zombie.gpickle' % n #elige un archivo y lo nombra como corresponde
        #filename= 'Grafo_not_zombie_prueba.gpickle'
        G= nx.read_gpickle(filename) #lee el archivo
        _,copia= clean(G) #limpia cada grafo 
        arbol= nx.dfs_tree(copia,0) #genera un arbol dirigido para cada grafo 
        arboles.append(arbol) #y cada uno se guarda en una lista de arboles. 
        
    return arboles

#%%
def subarboles(arbol):   
    #   ''' Toma un arbol dirigido y sin nodos de grado 2 y calcula los nodos
    #   que hay  en la cuarta generacion.
    # Luego, para un arreglo de subarboles (grafos dirigidos) calcula la persistencia y el tamaño.
    # Para el calculo de la persistencia genera una lista de listas con los nodos de cada generación. De esta
    # forma, el largo de esa lista es la cantidad de generaciones que tiene el arbol(contando al nodo madre). 
    # Por otro lado, el tamaño del subarbol viene dado por la cantidad de conexiones que existe, que se calcula
    # como el largo de la lista contenedora de edges. '''
        #ordena la lista de generaciones en orden creciente; va de la gen 1 a la gen(len(G))
    
    generaciones= [sorted(generation) for generation in topological_generations(arbol)] 
    
    #entrega los nodos de la cuarta generacion. Esta bien :3
    
    nodos= generaciones[3] 
    
    subarb=[]
    
    for i in range(len(nodos)):
        subarb +=  [nx.dfs_tree(arbol, nodos[i])] 
      
        persistencia= []
        tamaño= []
        for j in range(len(subarb)): 
            subgenerations= [sorted(generation) for generation in topological_generations(subarb[j] ) ]
            persistencia.append(len(subgenerations)-1) #no se cuenta la generacion del nodo 0
        
            tamaño.append(len( subarb[j].edges()))
            
            cantidad_subarboles= len(subarb)
                
            # cantidades= cantidad_subarboles.append
            # tamaños.append(tamaño)
            # persistencia.append(persistencia) #REVISAAAAAAAAAAAAR
        
    return cantidad_subarboles, persistencia, tamaño
    
 
#end subarboles



