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

G= nx.Graph()

#-----------------------------ARREGLOS PARA GUARDAR DATOS---------------------------------------------

T = np.array([[0,0]]) #define las posiciones ocupadas por cada particula

#pos= np.array([0, 0])
ind_part_activas= np.array([0,0]) #define el indice de la posicion de las particulas activas en T
N= 0


#----------------------------FUNCIONES A USAR-----------------------------------------------
def direction( ): 
    #retorna la dirección en que se va a mover una particula
    #esto hay que mejorarlo para que la particula no vuelva por donde vino
    
    return choice([(1,0), (-1,0), (0,1), (0,-1)] ) 
#%%
def isintrace(pos, trace):
    for i in trace:
        if np.array_equal(pos, i):
            return True
    return False
#%% 
def edge_list( G, nodes_pos, source, target):
    
    #esta funcion toma el grafo G, las posiciones de los nodos  y la direccion
    #en la que se genera la arista 'edge' ; desde source hasta target. 
    
    #recordar que np.append junta un array con un valor en un eje especificado.Por
    #lo tanto, se le debe entregar las coordenadas en arreglos, como Trace. 
    
    edges= np.append(source, target, axis=0)
    
    #nodes_pose debe ser un arrgelo unidimensional, que me diga el indice
    #o numero del nodo. En el caso en que un nodo se divida, los resultantes
    #deberían tener el mismo número, o seguiremos teniendo el problema. Quizá
    #una forma de arreglarlo sería conectar entre los nodos que tengan distancia
    #exactamente igual a 1
    
    G.add_node(target, pos= (nodes_pos[0], nodes_pos[1]))
    
    #Target tiene coordenadas x=nodes_pos[0], y=  nodes_pos[1] 
    #esto no tiene mucho sentido
    return G, edges 
# end edge_list
#%% 

def action(G, edges, pos, Trace, ind_tmp, N):
    pos += direction()
    if isintrace(pos, Trace):
        
        #    if any( Trace[:] == pos)  :  arroja un error, porque, si bien le estoy preguntando
        #a python si es que alguna fila de la traza es igual a la posicion, este compara 
        #todo el arreglo con pos, no parece comparar fila con fila. Para arreglarlo debería pregun-
        #tarle ...? tiene que revisar fila por fila, esto es, tiene que revisar TODO el arreglo
        #asi que debería ser any(blabla).all(?) y ahi no se que va xd
        pass 
    #estamos revisando una posible direccion ! 
    
        
    else : 
        #N+= 1
        #ind_tmp.append(N) #aqui agregamos el indice de la particula activa nueva 
          #y agregamos a la traza la posicion ocupada
        ind_tmp.append(pos)
        Trace= np.concatenate((Trace, [pos]), axis=0)
        N += 1
        G, edges= edge_list(G, pos, T[i-1], T[i])
        #aqui actualizamos la traza dentro el if. No deberíamos actualizarla fuera tambien? 
        
    #ind_part_activas= ind_tmp
    #print(ind_part_activas)
    
    return G, Trace, N, edges#ind_part_activas, N
        
 #%%        
  
#--------------------------------- MAIN CODE---------------------------------------------------------

#este loop se debe ejectutar mientras el contador sea menor al maximo, Y  mientras
#tengamos particulas activas. Si no hay nada activo, nada se propaga y dejamos el 
#codigo corriendo inutilmente 
pos= (0,0)
edges=np.zeros([len(pos), 2])

while t < tmax  and len(ind_part_activas) >0  :
        
    t += h # tiempo= tiempo+ h
    ind_tmp = [] #guarda una posicion temporal que debe ser verificada en la traza
    
    for i in ind_part_activas: 
        r= np.random.uniform(0,1) #retorna numeros uniformemente distribuidos entre cero y uno 
        #pos = np.array(T[i])  #Asigna la posicion a una fila de la traza. Esto es un arreglo de python
        # plt.scatter(T[:,0], T[:,1])
        # plt.savefig('paso' + str(i)+ '.png', format= 'png')
        # plt.clf() 
         
        if r< s: #si el número aleatorio escogido es menor que esa cantidad, hay ramificación
        #notese que al haber ramificacion, podemos agregar o quitar una particula, dependiendo de si
        #las posiciones han sido ocupadas. 
        
            # T, ind_part_activas, N = action(pos, T, ind_tmp, N)
            # T, ind_part_activas, N = action(pos, T, ind_tmp, N )
            G, T, N, edges = action(G, edges, i, T, ind_tmp, N)
            G, T, N, edges = action(G, edges, i, T, ind_tmp, N )
            
        else: #si el número es mayor o igual, saltamos 
            #T, ind_part_activas, N = action(pos, T, ind_tmp, N)
            G, T, N, edges = action(G, edges, i, T, ind_tmp, N)
    ind_part_activas = ind_tmp
    print(ind_tmp)
    #ind_part_activas = ind_tmp
    #aqui le estaba dando el valor de una lista vacía a ind_part_activas. Además, esto ya lo
    # hace la funcion de accion    


#para generar el grafo 



    
#ramificamos? si
#movemos tambien
# nos devolvemos 
# se desactiva todo de forma rara 

#la condicion para que una particula estpe activa es que (sin devolvernos) al menos
#una de las tres posiciones que tiene a su alrededor esté disponible 
#*revisar vecinos 
    