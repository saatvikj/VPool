from __future__ import division
import networkx as nx

def create_graph_from_input(adj_matrix):
	"""
	Creates the networkx graph to be used for coloring from input.

	Iterates over the contents of the file having admissibility
	matrix in order to create the corresponding networkx graph, 
	adds information about vertex weight to each vertex
	and changes input graph to graph whose coloring would fetch
	the sharability network.

	Args:
		adj_matrix: The adjacency matrix.

	Returns:
		A networkx graph which is complement of graph corresponding
		to graph given by admissibility matrix with each vertex 
		containing extra information about the vertex weight. The
		coloring of the complement graph will give us the trips 
		which can be shared together in one color class. 
	"""

	data = nx.Graph()
	for i in range(len(adj_matrix)):
		data.add_node(i)

	for i, source in enumerate(adj_matrix):
		for j, value in enumerate(source):
			if i != j and int(value) == 1:
				data.add_edge(i,j)

	nx.set_node_attributes(data, 1, 'weight')

	data = nx.complement(data)
	return data


def add_weight_to_vertices(graph, rates):
	"""
	Take input graph and add weights to corresponding
	vertices on the basis of the properties of the 
	vertices.

	Args:
		graph: the networkx graph

		rates: the rate slab for a passenger in the
		network.

	Returns:
		A networkx weighted graph with appropriate
		weights assigned to the vertices according
		to the weighing property.

	Side note: Current weighing property is that
		w(v) = w(v) - alpha(v) where alpha(v) is
		a value which is decided by degree of the 
		vertex v.
	"""
	nx.set_node_attributes(graph,0,'weight')
	weights = nx.get_node_attributes(graph, 'weight')
	for node, rate in enumerate(rates):
		weights[node] = rate
	nx.set_node_attributes(graph, weights, 'weight')
	return graph


if __name__ == '__main__':
	pass