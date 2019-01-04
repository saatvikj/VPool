import networkx as nx
import sys
import copy
import math
import random
import coloring_techniques as ct
import minimum_approximate as ma


def create_graph_from_input(filename):
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
		adj_matrix.append(row.split(' '))

	data = nx.Graph()
	for i in range(len(adj_matrix)):
		data.add_node(i)

	for i, source in enumerate(adj_matrix):
		for j, value in enumerate(source):
			if value != '' and (i != j) and (int(value) == 1):
				data.add_edge(i,j)

	nx.set_node_attributes(data, 1, 'weight')

	data = nx.complement(data)
	return data


def create_rates_for_slabs(distances, slab):
	"""
	Create rate matrix according to given slabs
	by reading distance matrix from the input
	file.

	Args:
		distances: The distance list corresponding
		to distance of each node from destination.

		slab: A dictionary with all but last keys
		as starting distance of slab and value as
		list of two elements with first value as
		base price and second as extra rate per km
		for that slab.

	Returns:
		A list of rates for each node in the vertex.
	"""
	rates = []
	for distance in distances:
		for base in slab:
			if distance != '' and int(distance) >= base[0] and int(distance) < base[1]:
				rates.append(slab[base][0] + int(distance)*slab[base][1])

	return rates


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


def get_distance_to_travel(filename):
	"""
	Create a list of distances that every passenger
	has to travel stored in the file.

	Args:
		filename: The file containing the data

	Returns:
		List of distances each person has to travel
		to reach the destination.
	"""
	distance_matrix = []
	rows = open(filename).read().split('\n');
	for row in rows:
		distance_matrix.append(row.split(' '))

	number_of_people = len(distance_matrix)

	return distance_matrix[number_of_people-1]


def get_sorted_nodes(graph):
	"""
	Give a list of nodes sorted in decreasing order
	of vertex weight.

	Args:
		graph: the networkx graph

	Returns:
		A list in which the nodes of the graph are
		sorted in decreasing order of their weights.
	"""
	weights = nx.get_node_attributes(graph, 'weight')
	weight_sorted_tuple_list = sorted(weights.items(), key=lambda item: item[1], reverse=True)

	sorted_nodes = []

	for i in weight_sorted_tuple_list:
		sorted_nodes.append(i[0])

	return sorted_nodes


def get_weight_dictionaries(graph, choice):
	"""
	Implementation of getting weights in terms of a 
	dictionary so that it can be used in the DSATUR
	variants function.

	Args:
		graph: The networkx weighted vertex graph in question
		choice: Integer representing for which variation we want 
		the weight dictionary., will be one of the values between
		0 and 4 (inclusive).
			0: Weight = 1
			1: Weight = ln(1+w(vertex))
			2: Weight = sqrt (w(vertex))
			3: Weight = w(vertex)
			4: Weight = w(vertex)^2

	Returns:
		A dictionary representing the weights to be needed for
		sending into the DSATUR variant function of coloring_techniques
		module. Dictionary maps vertex to corresponding weight.
	"""
	weight_dictionary = {}

	for i in range(graph.number_of_nodes()):
		if choice == 0:
			weight_dictionary[i] = 1
		elif choice == 1:
			weight_dictionary[i] = math.log(nx.get_node_attributes(graph, 'weight')[i]+1)
		elif choice == 2:
			weight_dictionary[i] = math.sqrt(nx.get_node_attributes(graph, 'weight')[i])
		elif choice == 3:
			weight_dictionary[i] = nx.get_node_attributes(graph, 'weight')[i]
		elif choice == 4:
			weight_dictionary[i] = nx.get_node_attributes(graph, 'weight')[i]**2

	return weight_dictionary


def give_best_coloring(graph, iterations):
	"""
	Main runner function, it implements the first column 
	generation phase of the paper being referred to.

	Args:
		graph: The networkx graph on which algorithm is implemented
		iterations: The maximum number of iterations till which 
		algorithm is repeated.

	Returns:
		A tuple of weight of best coloring and a dictionary 
		representing the best possible coloring that will be a 
		good heuristic for the weighted coloring problem,
		dictionary maps color index to list of vertices having that
		color.	
	"""
	# lower_bound = ma.give_model_approximate(graph)
	nearest_coloring = ct.dsatur_coloring(graph) 
	upper_bound = ct.calculate_coloring_weight(graph, nearest_coloring)
	iteration = 0

	nodes_list = get_sorted_nodes(graph)
	while (iteration < iterations):

		for i in range(1,5):
			coloring = ct.dsatur_based_weighted_coloring(graph, get_weight_dictionaries(graph, i), copy.deepcopy(nodes_list), greedy_allotment=False)		
			coloring_weight = ct.calculate_coloring_weight(graph, coloring)

			if coloring_weight < upper_bound:
				upper_bound = coloring_weight
				nearest_coloring = coloring
		
		weight_sorted_sequential_coloring = ct.weight_sorted_sequential(graph, copy.deepcopy(nodes_list))
		weight = ct.calculate_coloring_weight(graph, weight_sorted_sequential_coloring)

		greedy_dsatur_coloring = ct.dsatur_based_weighted_coloring(graph, get_weight_dictionaries(graph, 0), copy.deepcopy(nodes_list), greedy_allotment=True)
		greedy_dsatur_weight = ct.calculate_coloring_weight(graph, greedy_dsatur_coloring)

		if weight < upper_bound:
			upper_bound = weight
			nearest_coloring = weight_sorted_sequential_coloring

		if greedy_dsatur_weight < upper_bound:
			upper_bound = greedy_dsatur_weight
			nearest_coloring = greedy_dsatur_coloring

		iteration += 1

		random.shuffle(nodes_list)

	return upper_bound, nearest_coloring

if __name__ == '__main__':
	pass