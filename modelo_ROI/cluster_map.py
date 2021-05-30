import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

data_point = pd.read_csv('centros_googleApi')
centros = list(data_point['cluster_point'])

pos_graph = []
lab_dict = {}
for i,centro in enumerate(centros):
    lab_dict[i] = str(i)
    pos = centro.replace('(','').replace(')','').split(',')
    pos_graph.append((float(pos[0]),float(pos[1])))
    
time_data = pd.read_csv('time_matrix.csv')
time_matrix = time_data.iloc[:,1:].values
time_graph = nx.DiGraph(time_matrix)

nx.draw(time_graph,pos_graph,
            node_size=500,
            labels=lab_dict, 
            with_labels = True)
plt.show()
