from __future__ import division
import networkx as nx 
import sys
import operator
import itertools


def weight_sorted_sequential(graph, vertex_order):
	"""
	A sequential vertex coloring algorithm in which each vertex
	in vertex ordering is given lowest indexed color it can get.
	
	It is a greedy algorithm, in this application the order is 
	set to decreasing order of weights and hence vertices with
	similar weights are preferred to be given the same color.

	Args:
		graph: The networkx graph on which the sequential coloring
		algorithm is to be applied.

		vertex_order: The order in which vertices are to be colored,
		earlier defined to be decreasing order of weights.

	Returns:
		A dictionary containing the color classes of the graph based
		on the sequential coloring greedy algorithm, dictionary maps
		color index to list of vertices with that color.
	"""
	assigned_colors = {}
	last_new_assigned_color = -1

	for vertex in vertex_order:
		color_assigned = False
		for color in assigned_colors:
			if len(list(set(graph[vertex]) & set(assigned_colors[color]))) == 0:
				assigned_colors[color].append(vertex)
				color_assigned = True
				break
		if not color_assigned:
			assigned_colors[last_new_assigned_color+1] = []
			assigned_colors[last_new_assigned_color+1].append(vertex)
			last_new_assigned_color += 1
			color_assigned = True

	return assigned_colors		


def dsatur_coloring(graph):
	"""
	Direct DSATUR coloring of given input graph. Uses the networkx
	implementation of DSATUR algorithm to give a vertex coloring.

	DSATUR Coloring Algorithm: http://cs.indstate.edu/tdu/mine1.pdf

	Args:
		graph: The networkx graph on which the DSATUR coloring
		algoirithm is to be applied.

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


def dsatur_based_weighted_coloring(graph, weight, vertex_order, greedy_allotment=False):
	"""
	Implementation of DSATUR coloring with change in comparison
	function while selecting next vertex to color from saturation 
	degree to saturation degree multiplied with some weight. 

	DSATUR Coloring Algorithm: http://cs.indstate.edu/tdu/mine1.pdf
	
	It also implements the greedy allocation of DSATUR coloring if required
	where instead of using the lowest indexed color class, it finds the best
	fit color class according to the following two rules-
		1) If no color class has weight greater than weight of vertex, select
		the one which minimizes w(vertex)=w(class)
		2) Else select the one which minimizes w(class)-w(vertex)
		
	Args:
		graph: The networkx graph on which the DSATUR based coloring
		algoirithm is to be applied.

		weight: A dictionary representing the weight to be multiplied
		with each vertex. Key is vertex id, value is weight.

		vertex_order: The order in which vertices are put to handle any
		conflicts, i.e if saturation degree*weight is same, vertex that
		comes first in ordering is chosen.

		greedy_allotment (optional): Specifies whether allotment needs 
		to be done in standard way or by following greedy heuristics
		that were mentioned above.

	Returns:
		A dictionary containing the color classes of the graph based
		off the DSATUR based coloring, dictionary maps color index to
		list of vertices with that color.
	"""
	assigned_colors = {}
	color_class_weights = {}
	saturation_degree = {}
	colored = {}
	last_new_assigned_color = -1


	#Initialize saturation degree of each vertex
	for vertex in vertex_order:
		saturation_degree[vertex] = 0
		colored[vertex] = False

	#Iterate till each vertex isn't colored
	while len(vertex_order) > 0:

		#Find vertex with maximum value of saturation degree*weight
		max_value = saturation_degree[vertex_order[0]]*weight[vertex_order[0]]
		max_vertex = vertex_order[0]
		for vertex in saturation_degree:
			if saturation_degree[vertex]*weight[vertex] > max_value and colored[vertex] is not True:
				max_value = saturation_degree[vertex]*weight[vertex]
				max_vertex = vertex


		neighbors = graph[max_vertex]
		color_assigned = False

		#If greedy allotment is not needed to be done, for each already existing color class, 
		#check if any has no neighbor of max value vertex in it, if that happens, give the 
		#max value vertex that color.
		
		#If greedy allotment is needed to be done then find color class which satisfies the
		#heuristic constraints and then allot the vertex that color and update weights accordingly.

		#After selection of color class, update saturation degree of all vertices by checking if 
		#the newly colored vertex was the first of that color for all neighbors of neighbors of 
		#newly colored vertex 

		greedy_allotted_class_candidates = []

		for color in assigned_colors:
			if not greedy_allotment:
				if len(list(set(assigned_colors[color]) & set(neighbors))) == 0:
					assigned_colors[color].append(max_vertex)
					if nx.get_node_attributes(graph, 'weight')[max_vertex] > color_class_weights[color]:
						color_class_weights[color] = nx.get_node_attributes(graph, 'weight')[max_vertex]
					color_assigned = True
					for neighbor in neighbors:
						if list(set(graph[neighbor]) & set(assigned_colors[color])) == [max_vertex]:
							saturation_degree[neighbor] += 1
					break
			else:
				if len(list(set(assigned_colors[color]) & set(neighbors))) == 0:
					greedy_allotted_class_candidates.append(color)


		if greedy_allotment:
			if len(greedy_allotted_class_candidates) != 0:
				differences = {}
				selected_candidate = -1
				larger_weight_available = False
				for candidate in greedy_allotted_class_candidates:
					differences[candidate] = color_class_weights[candidate]-nx.get_node_attributes(graph, 'weight')[max_vertex]
					if differences[candidate] >= 0:
						larger_weight_available = True

				if larger_weight_available:
					lowest_difference = sys.maxsize
					for candidate in differences:
						if differences[candidate] >= 0 and differences[candidate] <= lowest_difference:
							lowest_difference = differences[candidate]
							selected_candidate = candidate
				else:
					selected_candidate = max(differences.iteritems(), key=operator.itemgetter(1))[0]

				assigned_colors[selected_candidate].append(max_vertex)
				color_assigned = True
				for neighbor in neighbors:
					if list(set(graph[neighbor]) & set(assigned_colors[selected_candidate])) == [max_vertex]:
						saturation_degree[neighbor] += 1	

		#If max value vertex can not be put in existing color classes, make a new color class
		#and update saturation degree of all neighbors of colored vertex.

		if not color_assigned:
			assigned_colors[last_new_assigned_color+1] = []
			assigned_colors[last_new_assigned_color+1].append(max_vertex)
			color_class_weights[last_new_assigned_color+1] = nx.get_node_attributes(graph, 'weight')[max_vertex]
			last_new_assigned_color += 1 
			color_assigned = True
			for neighbor in neighbors:
				saturation_degree[neighbor] += 1

		#Update non colored vertex list by removing the colored vertex
		vertex_order.remove(max_vertex)
		colored[max_vertex] = True

	return assigned_colors


def calculate_coloring_weight(graph, coloring):
	"""
	Given a vertex coloring, calculate the weight of that coloring
	based on the vertex weights. 

	Weight of a vertex coloring is given by sum of weights of maximum
	weighted vertices for each color class.

	Args:
		graph: The networkx graph on which the coloring algoirithm 
		has been applied.

		coloring: A dictionary containing the color classes of the graph, 
		dictionary maps color index to list of vertices with that color.

	Returns:
		The weight of the vertex coloring.
	"""
	weights = nx.get_node_attributes(graph, 'weight')
	coloring_weight = 0
	for color in coloring:
		max_value = -sys.maxsize-1		
		for vertex in coloring[color]:
			if weights[vertex] >= max_value:
				max_value = weights[vertex]
		coloring_weight += max_value 

	return coloring_weight


def seq_coloring(graph):
	"""
	Direct SEQ coloring of given input graph. Uses the networkx
	implementation of SEQ algorithm to give a vertex coloring.

	Args:
		graph: The networkx graph on which the DSATUR coloring
		algoirithm is to be applied.

	Returns:
		A dictionary containing the color classes of the graph based
		off the SEQ coloring, dictionary maps color index to
		list of vertices with that color.
	"""	
	colors = nx.coloring.greedy_color(graph,strategy='largest_first')
	color_classes = {}
	for k,v in colors.iteritems():
		keys = color_classes.setdefault(v,[])
		keys.append(k)

	return color_classes


def optimized_greedy_dsatur_coloring(graph, weight_dictionary):
	"""
	An optimized alternative for the function that implements
	DSATUR based weighted coloring. Optimization being adapted from
	the networkx implementation of the DSATUR coloring algorithm.

	Args:
		graph: The networkx graph on which the algorithm is to
		be applied.

		weight_dictionary: A dictionary representing the weight
		to be multiplied with each vertex. Key is vertex id, 
		value is weight.

	Returns:
		A dictionary containing the color classes of the graph based
		off the DSATUR based coloring, dictionary maps color index to
		list of vertices with that color.
	"""
	colors = {}
	nodes = saturation_degree_first(graph, weight_dictionary, colors)

	for u in nodes:
		# Set to keep track of colors of neighbours
		neighbour_colors = {colors[v] for v in graph[u] if v in colors}
		# Find the first unused color.
		for color in itertools.count():
			if color not in neighbour_colors:
				break
		# Assign the new color to the current node.
		colors[u] = color

	color_classes = {}
	for k,v in colors.iteritems():
		keys = color_classes.setdefault(v,[])
		keys.append(k)
	return color_classes


def saturation_degree_first(graph, weight_dictionary, colors):
	"""
	
	"""
	distinct_colors = {v: set() for v in graph}
	for i in range(len(graph)):
		# On the first time through, simply choose the node of highest degree.
		if i == 0:
			node = max(graph, key=graph.degree)
			yield node
			# Add the color 0 to the distinct colors set for each
			# neighbors of that node.
			for v in graph[node]:
				distinct_colors[v].add(0)
		else:
			# Compute the maximum saturation and the set of nodes that
			# achieve that saturation.
			saturation = {v: len(c)*weight_dictionary[v] for v, c in distinct_colors.items()
						  if v not in colors}
			# Yield the node with the highest saturation, and break ties by
			# degree.
			node = max(saturation, key=lambda v: (saturation[v], graph.degree(v)))
			yield node
			# Update the distinct color sets for the neighbors.
			color = colors[node]
			for v in graph[node]:
				distinct_colors[v].add(color)
if __name__ == '__main__':
	pass