from __future__ import division
import networkx as nx
from ortools.sat.python import cp_model


def or_naive_model(graph):
	"""
	Function that implements ILP Model M1 as presented by 
	Malaguti, Enrico, Michele Monaci, and Paolo Toth. 
	"Models and heuristic algorithms for a weighted vertex coloring 
	problem." Journal of Heuristics 15.5 (2009): 503-526 using google
	or tools.

	Args:
		graph: The input graph on which model is to be implemented

	Returns:
		The coloring of the graph.
	"""
	model = cp_model.CpModel()
	matrix_dimension = graph.number_of_nodes()
	weights = nx.get_node_attributes(graph, 'weight')
	x = {}
	for i in range(matrix_dimension):
		for j in range(matrix_dimension):
			x[(i,j)] = model.NewBoolVar('x_%i%i' %(i, j))
	
	z = {}
	for i in range(matrix_dimension):
		z[i] = model.NewIntVar(0, 9999999999999, 'z_%i' %i)

	for h in range(matrix_dimension):
		for i in range(matrix_dimension):
			model.Add(z[h] >= x[(i,h)]*weights[i])

	for i in range(matrix_dimension):
		only_one_color_expression = sum(x[(i,h)] for h in range(matrix_dimension))
		model.Add(only_one_color_expression == 1)

	for h in range(matrix_dimension):
		for i in graph.edges():
			model.Add(x[(i[0],h)]+x[(i[1],h)] <= 1)

	model.Minimize(sum(z[h] for h in range(matrix_dimension)))
	solver = cp_model.CpSolver()
	solver.Solve(model)