# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 17:07:55 2023

@author: sepul
"""
import matplotlib.pyplot as plt 
import networkx as nx
import functions
import numpy as np
from collections import Counter

#%%

#-----------------------------------------GRAPH NETWORK-----------------------------------------------------------
G = nx.read_gpickle('Graph_s1_t_300.gpickle')

plt.figure(figsize=(9,9))
plt.axis('equal')   
plt.style.use('bmh')
plt.grid(False)
   
# plt.scatter(T[:,0], T[:,1], c= 'grey', alpha= 0.0)
# plt.scatter(T[ind_part_activas][:,0], T[ind_part_activas][:,1], c= 'red', alpha= 0.8)

angle = np.linspace( 0 , 2 *np.pi) 
 
radius = 25
x = radius * np.cos( angle ) 
y = radius * np.sin( angle ) 

plt.plot( x, y, color='crimson', alpha=0.1) 


x= nx.get_node_attributes(G, 'pos')

G.add_edges_from(G.edges)

nx.draw_networkx_nodes(G,x, node_shape='.', node_size=0.0, alpha= 0 )
nx.draw_networkx_edges(G,x)

     
plt.show()


#%% 
#------------------------------------------------DIRECTED TREE----------------------------------------------
#generacion de arboles dirigidos

nodos, copia = functions.clean(G) #limpia la red quitando los nodos de grado 2
arbol= nx.dfs_tree(copia, 0) #genera un arbol genealogico DIRIGIDO

tree_2= functions.hierarchy_pos(arbol,0) #Toma el arbol no dirigido y lo ordena 
nx.draw(G, tree_2 ,node_color= 'red', node_size= 10) #dibuja el arbol dirigido 
plt.show()

#%%--------------------------------------------DISTRIBUCION DE NODOS------------------------------------------
functions.degree_distribution(300)



#%% 

arbolitos= functions.generar_arboles(300)
tamaño= []
persistencia= []
for tree in arbolitos: 
    
    subarbol= functions.subarboles(tree)
    tamaño += subarbol[2]
    persistencia += subarbol[1]
    
 #%%--------------------------------------------DESIGN DETAILS-------------------------------------
 
# import matplotlib.font_manager
# from IPython.core.display import HTML

# def make_html(fontname):
#     return "<p>{font}: <span style='font-family:{font}; font-size: 24px;'>{font}</p>".format(font=fontname)

# code = "\n".join([make_html(font) for font in sorted(set([f.name for f in matplotlib.font_manager.fontManager.ttflist]))])

# HTML("<div style='column-count: 2;'>{}</div>".format(code))
csfont = {'fontname':'Comic Sans MS'}
hfont = {'fontname':'Helvetica'}
awfont= {'fontname' :  'FontAwesome'}

 
 #%% 


plt.style.use('bmh')
plt.hist(tamaño, color='crimson', align= 'mid',bins=np.arange(0,1200,200) , rwidth=0.9, histtype='bar')
#plt.hist(tamaño, color='crimson', align= 'mid',bins=np.arange(0,1200,200) , rwidth=0.8, histtype='bar', cumulative= True)
#plt.title('Distribución acumulada de tamaños de subárboles', fontsize= 18, fontname= 'Helvetica')
plt.title('Distribución de tamaños de subárboles', fontsize= 18, **csfont)
plt.xlabel('Tamaño del subárbol', fontsize= 15) 
plt.ylabel('Número de subárboles', fontsize=15)
plt.yscale('log')
plt.grid(False)
plt.show()
#me gustaria poner barras por intervalo: por ejemplo, que en el intervalo 0-200 hay 2000 arboles
#
#%%
plt.hist(persistencia, color= 'crimson', align= 'mid', bins= np.arange(0,40, 5), rwidth= 0.9, histtype= 'bar')
plt.title('Distribución de persistencia de subárboles', fontsize= 18)
#plt.hist(tamaño, color='crimson', align= 'mid',bins=np.arange(0,1200,200) , rwidth=0.8, histtype='bar', cumulative= True)
#plt.title('Distribución acumulada de tamaños de subárboles', fontsize= 18, fontname= 'Helvetica')
plt.xlabel('Persistencia del subárbol', fontsize=15) 
plt.ylabel('Número de subárboles', fontsize=15)
plt.yscale('log')
plt.grid(False)

plt.show()







