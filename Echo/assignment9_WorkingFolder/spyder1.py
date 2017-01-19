# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 20:36:13 2017

@author: Hanadi
"""
import pandas as pd
store = pd.HDFStore('store.h5')
df2 = store['df2']

import networkx as nx

#create tuples of edges
def maketuple(x, y):
    r = []
    for i in range(len(y)):
        r.append((x, y[i]))
    return r
    
#add edges to the graph
def makeGraph(df):
    Graph = nx.Graph()
    for row in df.itertuples():
        Graph.add_edges_from(maketuple(row[1], row[2]))
    print 'Graph is made..'
    return Graph
    
G = makeGraph(df2)

#find the diameter of each sub graph
def findDiameter(G):
    for index, graph in enumerate(G):
        diameter = set()
        for node in graph:
            lenght = nx.single_source_dijkstra_path_length(graph, node)
            diameter.add(lenght[max(lenght, key=lenght.get)])
        print 'Diameter in subgraph',index, max(diameter)
        
#if the graph is not connected make subgraphs
if(nx.is_connected(G)):
    print 'Graph is connected'
    findDiameter(G)
else:
    print 'Graph is not connected'
    subgraphs = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)
    findDiameter(subgraphs)
    