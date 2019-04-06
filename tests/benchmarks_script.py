from __future__ import division
import sys
sys.path.insert(0, 'D:/College/VPool/')
import networkx as nx
import csv
import random
from graph import weighted_vertex_coloring as wvc

def run_test(nodes, density, weights, iterations):
	"""
	Function to create an arbitrary graph with given number
	of nodes, edge density and given weight function and run
	the weighted vertex coloring on it.

	Args:
		nodes: Number of nodes of the graph
		density: Edge density (Between 0 and 1)
		weights: Node weights
		iterations: Number of iterations of wvc

	Returns:
		A list of statistics obtained for the run.
	"""
	test_graph = nx.complete_graph(nodes)
	number_of_removed_edges = int((1-density)*(len(test_graph.edges)))
	removal = random.sample(list(test_graph.edges),number_of_removed_edges)
	test_graph.remove_edges_from(removal)
	test_graph = nx.complement(test_graph)
	nx.set_node_attributes(test_graph, weights, 'weight')
	weight, coloring = wvc.give_best_coloring(test_graph, iterations)
	print(coloring)
	print(weight)
	num_classes = len(coloring)
	avg_people_per_class = float(nodes/num_classes)

	results_list = [nodes, density, iterations, num_classes, avg_people_per_class]

	return results_list

if __name__ == '__main__':

	nodes = [100]
	densities = [0.8]
	iterations = 100

	for i in nodes:
		for j in densities:
			run_test(i, j, 1, 100)