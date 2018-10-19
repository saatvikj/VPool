import networkx as nx
import sys

def create_graph_from_input(filename, weights):
"""
	Creates the networkx graph to be used for coloring from input file.

	Iterates over the contents of the file having admissibility
	matrix in order to create the corresponding networkx graph, 
	adds information about vertex weight to each vertex
	and changes input graph to graph whose coloring would fetch
	the sharability network.

	Args:
		filename: Name of file which has admissibility matrix, i.e
		the matrix corresponding to graph in which two nodes are
		connected if their trips can be shared.

		weights: A list of integers corresponding to vertex weight
		of each vertex of the graph, weight of vertex n (0 indexed)
		will be stored at list index n.

	Returns:
		A networkx graph which is complement of graph corresponding
		to graph given by admissibility matrix with each vertex 
		containing extra information about the vertex weight. The
		coloring of the complement graph will give us the trips 
		which can be shared together in one color class. 

"""

	adj_matrix = []
	input_rows = open(filename).read().split('\n')

	for row in input_rows:
		adj_matrix.append(row.split(','))

	data = nx.Graph()
	for i in range(len(adj_matrix)):
		data.add_node(i,weight=weights[i])

	for i,source in adj_matrix:
		for j,destination in adj_matrix:
			if not (i == j):
				data.add_edge(source, destination)

	data = nx.complement(data)
	return data

	



if __name__ == '__main__':
	pass