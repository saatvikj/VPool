import networkx as nx 
import sys

def dsatur_coloring(graph):
"""
	Direct DSATUR coloring of given input graph. Uses the networkx
	implementation of DSATUR algorithm to give a vertex coloring.

	DSATUR Coloring Algorithm: http://cs.indstate.edu/tdu/mine1.pdf

	Args:
		graph: The networkx graph to be colored.

	Returns:
		A dictionary containing the color classes of the graph based
		off the DSATUR coloring, dictionary maps color index to
		list of vertices with that color.

"""
	
	colors = nx.coloring.greedy_color(graph,strategy='DSATUR')
	color_classes = {}
	for k,v in colors.iteritems():
		keys = color_classes.setdefault(v,[])
		keys.append(k)
	return color_classes


def dsatur_based_weighted_coloring(graph, weight, vertex_order):
"""
	Implementation of DSATUR coloring with change in comparison
	function while selecting next vertex to color from saturation 
	degree to saturation degree multiplied with some weight. 

	DSATUR Coloring Algorithm: http://cs.indstate.edu/tdu/mine1.pdf
	
	Args:
		graph: The networkx graph to be colored
		weight: A dictionary representing the weight to be multiplied
		with each vertex. Key is vertex id, value is weight.
		vertex_order: The order in which vertices are put to handle any
		conflicts, i.e if saturation degree*weight is same, vertex that
		comes first in ordering is chosen..

	Returns:
		A dictionary containing the color classes of the graph based
		off the DSATUR based coloring, dictionary maps color index to
		list of vertices with that color.

"""

	assigned_colors = {}
	saturation_degree = {}
	last_new_assigned_color = -1


	#Initialize saturation degree of each vertex
	for vertex in vertex_order:
		saturation_degree[vertex] = 0

	#Iterate till each vertex isn't colored
	while len(vertex_order) != 0:

		#Find vertex with maximum value of saturation degree*weight
		max_value = -1
		max_vertex = vertex_order[0]
		for vertex in saturation_degree:
			if saturation_degree[vertex]*weight[vertex] > max_value:
				max_value = saturation_degree[vertex]*weight[vertex]
				max_vertex = vertex


		neighbors = graph[max_vertex]
		color_assigned = False

		#For each already existing color class, check if any has no neighbor of max value
		#vertex in it, if that happens, give the max value vertex that color and update
		#saturation degree of all vertices by checking if the newly colored vertex 
		#was the first of that color for all neighbors of neighbors of newly colored vertex 
		
		for color in assigned_colors:
			if len(list(set(assigned_colors[color]) & set(neighbors))) == 0:
				assigned_colors[color].append(max_vertex)
				color_assigned = True
				for neighbor in neighbors:
					if list(set(graph[neighbor]) & set(assigned_colors[color])) == [max_vertex]:
						saturation_degree[neighbor] += 1
				break

		#If max value vertex can not be put in existing color classes, make a new color class
		#and update saturation degree of all neighbors of colored vertex.
		if not color_assigned:
			assigned_colors[last_new_assigned_color+1] = []
			assigned_colors[last_new_assigned_color+1].append(max_vertex)
			last_new_assigned_color += 1 
			color_assigned = True
			for neighbor in neighbors:
				saturation_degree[neighbor] += 1

		#Update non colored vertex list by removing the colored vertex
		vertex_order.remove(max_vertex)

				
def calculate_coloring_weight(graph, coloring):
"""
	Given a vertex coloring, calculate the weight of that coloring
	based on the vertex weights. 

	Weight of a vertex coloring is given by sum of weights of maximum
	weighted vertices for each color class.

	Args:
		graph: The networkx graph to be colored
		coloring: A dictionary containing the color classes of the graph, 
		dictionary maps color index to list of vertices with that color.

	Returns:
		The weight of the vertex coloring.

"""

	weights = nx.get_node_attributes(graph, 'weight')
	coloring_weight = 0
	for color in coloring:
		max_value = -sys.maxint-1		
		for vertex in coloring[color]:
			if weights[vertex] >= max_value:
				max_value = weights[vertex]
		coloring_weight += max_value 

	return coloring_weight



if __name__ == '__main__':
	pass