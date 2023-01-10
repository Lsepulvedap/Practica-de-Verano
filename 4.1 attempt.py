# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 17:04:30 2023

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

T = np.array([[0,0]]) #define las posiciones ocupadas por cada particula

pos= np.array([0, 0]) #posicion de las particulas activas

ind_part_activas= np.array([0]) #define el indice de la posicion de las particulas activas en T
N= 0


#----------------------------FUNCIONES A USAR-----------------------------------------------
def direction( ): 
    #retorna la dirección en que se va a mover una particula
    #esto hay que mejorarlo para que la particula no vuelva por donde vino 
    return choice([(1,0), (-1,0), (0,1), (0,-1)] ) 



def action(pos, Trace, ind_tmp, N):
    
    pos += direction()
    
    if any(np.equal(Trace, pos).all(1)):
        
        #    if any( Trace[:] == pos)  :  arroja un error, porque, si bien le estoy preguntando
        #a python si es que alguna fila de la traza es igual a la posicion, este compara 
        #todo el arreglo con pos, no parece comparar fila con fila. Para arreglarlo debería pregun-
        #tarle ...? tiene que revisar fila por fila, esto es, tiene que revisar TODO el arreglo
        #asi que debería ser any(blabla).all(?) y ahi no se que va xd
        pass 
    #estamos revisando una posible direccion ! 
      
    else : 
        N+= 1
        ind_tmp.append(N) #aqui agregamos el indice de la particula activa nueva 
          #y agregamos a la traza la posicion ocupada
       
        Trace= np.concatenate((Trace, [pos]), axis=0)
        #aqui actualizamos la traza dentro el if. No deberíamos actualizarla fuera tambien? 
        
    # ind_part_activas= ind_tmp
    # print(ind_part_activas)
    
    return Trace, N 
 #%%        
  
#--------------------------------- MAIN CODE---------------------------------------------------------

#este loop se debe ejectutar mientras el contador sea menor al maximo, Y  mientras
#tengamos particulas activas. Si no hay nada activo, nada se propaga y dejamos el 
#codigo corriendo inutilmente 

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
             T, N = action( pos, T, ind_tmp, N)
             T, N = action( pos, T, ind_tmp, N )
            
        else: #si el número es mayor o igual, saltamos 
            #T, ind_part_activas, N = action(pos, T, ind_tmp, N)
             T, N = action( pos, T, ind_tmp, N )
    ind_part_activas = ind_tmp
    
    print(ind_tmp)
    #ind_part_activas = ind_tmp
    #aqui le estaba dando el valor de una lista vacía a ind_part_activas. Además, esto ya lo
    # hace la funcion de accion    
#%%

for i in range(len(T[:,0])): 
    
    plt.scatter(T[i,0], T[i,1]) #grafica todas las posiciones ocupadas
    plt.text(x=T[i,0],  y= T[i,1], s=i)

    #%%

G= nx.Graph()
nodes_labels= len(T[:,0])
edges= np.zeros( (nodes_labels-1, 2)) 

edges[:, 0] = np.arange(0, nodes_labels-1)
edges[:, 1] = np.arange(1, nodes_labels)

for i in range(nodes_labels): 
    G.add_node(i, pos= (T[i,0], T[i,1]))

G.add_edges_from(edges)
pos= nx.get_node_attributes(G, 'pos')


fig, ax = plt.subplots()
nx.draw_networkx(G, pos, with_labels=True, arrows=True )

ax.set_axis_on()
ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)



#la idea es que se conecten los nodos que están a distancia 1 exactamente entre ellos 
