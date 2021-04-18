def main(args):
    """
    Use: 
    python color_graph.py num_clusters
    Parametros:
    num_clusters: numero de clusters para el coloreado
    Ejemplo:
    python color_graph.py 45
    """ 

    if(len(args)==1):

        import osmnx as ox
        import networkx as nx 
        import geopandas as gpd
        import matplotlib.pyplot as plt
        import pandas as pd
        from sklearn.cluster import AgglomerativeClustering
        from sklearn.preprocessing import MinMaxScaler
        import numpy as np

        num_clusters = int(args[0])
        point = (-0.206412, -78.499363)
        filtro = '["highway"~"primary|secondary|tertiary"]'
        graph = ox.graph_from_point(point, dist=1000, simplify=True, custom_filter=filtro)
        g_nodes = list(graph.nodes)
        positions = {}
        for node_name in g_nodes:
            positions[node_name] = (graph.nodes[node_name]['x'],graph.nodes[node_name]['y'])
        positions_x = nx.get_node_attributes(graph,'x')
        positions_y = nx.get_node_attributes(graph,'y')
        positions_for_data={'nodos':g_nodes,
            'position_x':positions_x.values(),
            'position_y':positions_y.values()}
        data = pd.DataFrame.from_dict(positions_for_data)
        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(data[['position_x','position_y']])
        data_scaled = pd.DataFrame(data_scaled, columns=data.columns[1:])
        cluster = AgglomerativeClustering(n_clusters=num_clusters, affinity='euclidean', linkage='ward')  
        colors_num = cluster.fit_predict(data_scaled)
        print(colors_num)
        labeldict = {}
        for i,node_name in enumerate(g_nodes):
            labeldict[node_name] = colors_num[i]

        data['cluster']=colors_num
        data['centro_x'] = 0
        data['centro_y'] = 0

        centros = []
        for cluster in range(max(colors_num)+1):
            indices = np.where(data['cluster']==cluster)
            grupo = data.iloc[indices]
            centro_x = grupo['position_x'].mean()
            centro_y = grupo['position_y'].mean()
            for indice in indices:
                data.at[indice,'centro_x']=centro_x
                data.at[indice,'centro_y']=centro_y
                
            centros.append((centro_x,centro_y))        

        inicio_nodos = max(g_nodes)+1
        idx = inicio_nodos
        colores_centros = []
        for centro in centros:
            graph.add_node(idx)
            graph.nodes[idx]['x']=centro[0]
            graph.nodes[idx]['y']=centro[1]
            colores_centros.append(40)
            idx+=1

        colors_num_2 = np.append(colors_num,colores_centros)
        
        fig, ax = ox.plot_graph(graph,
            node_color=colors_num_2,    
            node_size=50)

        positions = {}
        g_nodes = list(graph.nodes)
        for node_name in g_nodes:
            positions[node_name] = (graph.nodes[node_name]['x'],graph.nodes[node_name]['y'])
        
        nx.draw(graph,positions,
            node_size=500,
            node_color=colors_num_2)
        plt.show()
        
    else:
        print(main.__doc__)
    return 0

if __name__ == '__main__' :
    import sys
    main(sys.argv[1:])
    
""" 
nx.draw(graph,positions,
            node_size=500,
            node_color=colors_num,
            labels=labeldict, 
            with_labels = True)
        plt.show() """