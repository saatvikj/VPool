from gurobipy import *
import networkx as nx


def naive_wvc_model(graph):
	"""
	Function that implements ILP Model M1 as presented by 
	Malaguti, Enrico, Michele Monaci, and Paolo Toth. 
	"Models and heuristic algorithms for a weighted vertex coloring 
	problem." Journal of Heuristics 15.5 (2009): 503-526.

	Args:
		graph: The input graph on which model is to be implemented

	Returns:
		The coloring of the graph.
	"""
	matrix_dimension = graph.number_of_nodes()
	weights = nx.get_node_attributes(graph, 'weight')
	model = Model("approximate")
	model.setParam(GRB.Param.OutputFlag, 0)

	x = model.addVars(matrix_dimension,matrix_dimension,vtype=GRB.BINARY, name="allotment")
	z = model.addVars(matrix_dimension)

	for h in range(matrix_dimension):
		for i in range(matrix_dimension):
			model.addConstr(z[h],GRB.GREATER_EQUAL,weights[i]*x[i,h])

	for i in range(matrix_dimension):
		only_one_class_constraint = LinExpr()
		for h in range(matrix_dimension):
			only_one_class_constraint += x[i,h]
		model.addConstr(only_one_class_constraint, GRB.EQUAL, 1)

	for h in range(matrix_dimension):
		for i in graph.edges():
			model.addConstr(x[i[0],h] + x[i[1],h], GRB.LESS_EQUAL, 1)

	obj_function = LinExpr()
	for i in range(matrix_dimension):
		obj_function += z[i]

	model.setObjective(obj_function, GRB.MINIMIZE)
	model.optimize()


	color_class_distribution = []
	for i in range(matrix_dimension):
		i_class = []
		for j in range(matrix_dimension):
			i_class.append(model.getVarByName("allotment")[i,j])
		color_class_distribution.append(i_class)

	return color_class_distribution 