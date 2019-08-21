from __future__ import division
import networkx as nx


def create_graph_from_input(adj_matrix):
	"""
	Creates the networkx graph to be used for coloring from input.

	Iterates over the contents of the list having admissibility
	matrix in order to create the corresponding networkx graph, 
	adds information about vertex weight to each vertex
	and changes input graph to graph whose coloring would fetch
	the sharability network.

	Args:
		adj_matrix: The adjacency matrix of the graph created
		from the input data.

	Returns:
		A networkx graph which is complement of graph corresponding
		to graph given by admissibility matrix with each vertex 
		containing extra information about the vertex weight.
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


def create_dynamic_graph(adj_matrix, types):
	data = nx.Graph()
	for i in range(len(adj_matrix)):
		data.add_node(i)


	for i, source in enumerate(adj_matrix):
		for j, value in enumerate(source):
			if i != j and int(value) == 1:
				data.add_edge(i,j)

	nx.set_node_attributes(data, 1, 'weight')

	data = nx.complement(data)
	nx.set_node_attributes(data, 'rider', 'type')
	rider_type_dictionary = nx.get_node_attributes(data,'type')

	for i in range(len(adj_matrix)):
		rider_type_dictionary[i] = types[i]

	nx.set_node_attributes(data, rider_type_dictionary, 'type')

	return data


def add_weight_to_vertices(graph, rates):
	"""
	Take input graph and add weights to corresponding
	vertices on the basis of the properties of the 
	vertices.

	Args:
		graph: The networkx graph on which the weights
		need to be added.

		rates: The weights that correspond to each rider
		in the network.

	Returns:
		A networkx weighted graph with appropriate
		weights assigned to the vertices according
		to the weighing property.

	Side note: Current weighing property is that
		w(v) = d(v) where d(v) is the average 
		distance between sources of other vertices
		from v's source.
	"""
	nx.set_node_attributes(graph,0,'weight')
	weights = nx.get_node_attributes(graph, 'weight')

	for node, rate in enumerate(rates):
		weights[node] = rate
	nx.set_node_attributes(graph, weights, 'weight')

	return graph


if __name__ == '__main__':
	pass