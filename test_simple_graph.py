# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 11:56:09 2023

@author: sepul
"""

import numpy as np
import networkx as nx

G= nx.Graph()
nodes_pos= np.array([[1,2], [2,3], [0,1], [1,8]])
 
edges= np.zeros( (3, 2 ))

edges[:,0]= np.arange(0,3)
edges[:,0]= np.arange(1,4)

for i in range(4): 
    G.add_node(i, pos= (nodes_pos[i,0], nodes_pos[i,1]))

G.add_edges_from(edges)
pos= nx.get_node_attributes(G, 'pos')

nx.draw(G, pos)