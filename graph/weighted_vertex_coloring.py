from __future__ import division
import sys
import os
sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),os.pardir)))
import networkx as nx
import math
import random
import copy
import numpy as np
import optimization.minimum_approximate as ma
import coloring_techniques as ct


def get_weight_dictionaries(graph, choice):
	"""
	Implementation of getting weights in terms of a 
	dictionary so that it can be used in the DSATUR
	variants function.

	Args:
		graph: The networkx weighted vertex graph in question

		choice: Integer representing for which variation we want 
		the weight dictionary, will be one of the values between
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
	Main runner function for WVC, it implements the first column 
	generation phase of the paper being referred to.

	Args:
		graph: The networkx graph on which algorithm is to be
		implemented.
		
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
			coloring = ct.optimized_greedy_dsatur_coloring(graph, get_weight_dictionaries(graph, i))
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

		nodes_list = reorder_nodes(nearest_coloring)

	return upper_bound, nearest_coloring


def get_sorted_nodes(graph):
	"""
	Give a list of nodes sorted in decreasing order
	of vertex weight.

	Args:
		graph: The networkx graph for which the list
		of nodes sorted in decreasing order of vertex
		weight is required.

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


def reorder_nodes(color_classes):
	"""
	Using a reordering heuristic to order the
	nodes for next iteration on the basis of
	different heuristics.

	Args:
		color_classes: The obtained color class
		from previous iteration.

	Returns:
		An ordering of the vertices for next
		iteration.
	"""
	size_array = [color for color in color_classes]
	numpy_size_array = np.array([len(color_classes[color]) for color in size_array])
	sorted_index = np.argsort(numpy_size_array).tolist()

	nodes_list = []

	for index in sorted_index:
		nodes_list.extend(color_classes[size_array[index]])

	return nodes_list


if __name__ == '__main__':
	pass