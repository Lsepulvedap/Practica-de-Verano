# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 17:07:55 2023

@author: sepul
"""
import matplotlib.pyplot as plt 
import networkx as nx
import tree_thingy as tt
import numpy as np


G = nx.read_gpickle('Graph1.gpickle')

plt.figure(figsize=(9,9))
plt.axis('equal')   
   
# plt.scatter(T[:,0], T[:,1], c= 'grey', alpha= 0.0)
# plt.scatter(T[ind_part_activas][:,0], T[ind_part_activas][:,1], c= 'red', alpha= 0.8)

angle = np.linspace( 0 , 2 *np.pi) 
 
radius = 10
x = radius * np.cos( angle ) 
y = radius * np.sin( angle ) 

plt.plot( x, y ) 

x= nx.get_node_attributes(G, 'pos')

G.add_edges_from(G.edges)

nx.draw_networkx_nodes(G,x, node_shape='.', node_size=0.0, alpha= 0 )
nx.draw_networkx_edges(G,x)

     
plt.show()

#%% 

nodos, copia = tt.clean(G)

# plt.figure(figsize=(9,5))
plt.axis('equal')  
tree= tt.hierarchy_pos(G, 0)

nx.draw(G, tree, node_color= 'red', node_size= 10)
plt.show()
#%%
plt.figure(figsize= (9,9))
P_k= tt.histogram(G)
plt.show()