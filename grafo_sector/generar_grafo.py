import osmnx as ox
import networkx as nx 
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Fetch the Osmx data from an addres
#place_name = "Puente El Guambra, Desvio Puente Moran Valverde, La Argelia, Quito, Pichincha, 16258, Ecuador"
#graph = ox.graph_from_address(place_name)

# from a point
point = (-0.206412, -78.499363)
filtro = '["highway"~"primary|secondary"]'
graph = ox.graph_from_point(point, dist=1000, simplify=True, custom_filter=filtro)
# Project the graph
graph_proj = ox.project_graph(graph)
# plot the graph
fig, ax = ox.plot_graph(graph_proj)

""" # cálculo basico de las estadisticas de la red
stats = ox.basic_stats(graph_proj)
print(stats)

# cálculo del área de cobertura de la calle 
nodes, edges = ox.graph_to_gdfs(graph_proj, nodes=True, edges= True)
area = edges.unary_union.convex_hull.area
print(area)



# Análisis de red
# =================
from shapely.geometry import box
bbox = box(*edges.unary_union.bounds)

# Cálcula el centro de la red 
centroid = bbox.centroid

# Convert coordenada x a tipo flotante 
nodes['x'] = nodes['x'].astype(float)

# Obtiene la coordenada mas alejada y extrae la fila
maxx = nodes['x'].max()

target_loc = nodes.loc[nodes['x']==maxx, :]

# Extract the geometry
target_point = target_loc.geometry.values[0]

# Extract the coordinates 
origen_xy = (centroid.y, centroid.x)
target_xy = (target_point.y, target_point.x)

# encuentra los nodos mas cercanos de la red
origen_node = ox.get_nearest_node(graph_proj, origen_xy, method='euclidean')
target_node = ox.get_nearest_node(graph_proj, target_xy, method='euclidean')

# encuentra el camino mas corto
route = nx.shortest_path(G=graph_proj, source=origen_node, target=target_node) """