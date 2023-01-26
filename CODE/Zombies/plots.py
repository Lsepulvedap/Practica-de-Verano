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
G = nx.read_gpickle('Grafo_prueba.gpickle')

plt.figure(figsize=(9,9))
plt.axis('equal')   
plt.style.use('bmh')
plt.grid(False)
   

x= nx.get_node_attributes(G, 'pos')

G.add_edges_from(G.edges)

nx.draw_networkx_nodes(G,x, node_shape='.', node_size=0.0, alpha= 0 )
nx.draw_networkx_edges(G,x)

plt.savefig('red_revive.pdf')
     



#%% 
#------------------------------------------------DIRECTED TREE----------------------------------------------
#generacion de arboles dirigidos

nodos, copia = functions.clean(G) #limpia la red quitando los nodos de grado 2
arbol= nx.dfs_tree(copia, 0) #genera un arbol genealogico DIRIGIDO



import pydot
from networkx.drawing.nx_pydot import graphviz_layout


pos = graphviz_layout(arbol, prog="dot", root=(0))

plt.figure(figsize=(9,9))
   
plt.style.use('bmh')
plt.grid(False)
nx.draw_networkx(arbol, pos,arrows= False, with_labels=False, node_size=1, node_color='mediumblue')
plt.savefig('arbol_revive.pdf')

#%%--------------------------------------------DISTRIBUCION DE NODOS------------------------------------------
functions.degree_distribution(300)
plt.savefig('node_degree_revive.svg')



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

#tamaño normal 
plt.style.use('bmh')
plt.hist(tamaño, color='#669BBC', align= 'mid',bins=50 , rwidth=0.9, histtype='bar')
#plt.hist(tamaño, color='crimson', align= 'mid',bins=np.arange(0,1200,200) , rwidth=0.8, histtype='bar', cumulative= True)
#plt.title('Distribución acumulada de tamaños de subárboles', fontsize= 18, fontname= 'Helvetica')
#plt.title('Distribución de tamaños de subárboles', fontsize= 18, fontname="Arial")

plt.xlabel('Tamaño del subárbol', fontsize= 15, fontname="Arial")
plt.ylabel('Número de subárboles', fontsize=15, fontname="Arial")
plt.yscale('log')
plt.grid(False)
plt.savefig('tamaño_revive.pdf')

#%%
#tamaño acumulada y normalizada 

plt.style.use('bmh')

plt.hist(tamaño, color='#669BBC', align= 'mid',bins=50 , rwidth=0.8, histtype='bar',density= True ,cumulative= True)


plt.xlabel('Tamaño de subarboles', fontsize= 15, fontname="Arial")
plt.ylabel('Probabilidad acumulada', fontsize=15, fontname="Arial")

plt.grid(False)
plt.savefig('tamaño_acumulado_revive.pdf')

#me gustaria poner barras por intervalo: por ejemplo, que en el intervalo 0-200 hay 2000 arboles
#
#%%
#persistencia normal 
plt.hist(persistencia, color='#669BBC', bins=32,align= 'mid', rwidth= 0.9, histtype= 'bar')


plt.xlabel('Persistencia de subárboles', fontsize=15) 
plt.ylabel('Número de subárboles', fontsize=15)
plt.yscale('log')
plt.grid(False)

plt.savefig('persistencia_revive.svg')

#%% 
#persistencia acumulada

plt.hist(persistencia, color='#669BBC', align= 'mid',bins=50 , rwidth=0.8, histtype='bar',density= True, cumulative= True)

plt.xlabel('Persistencia de subárboles', fontsize=15) 
plt.ylabel('Probabilidad acumulada', fontsize=15)

plt.grid(False)

plt.savefig('persistencia_acumulada_revive.pdf')





