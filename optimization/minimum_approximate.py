try:
	from gurobipy import *
	import networkx as nx


	def give_model_approximate(graph):
		"""
		Function that implements ILP Model M2 as presented by 
		Malaguti, Enrico, Michele Monaci, and Paolo Toth. 
		"Models and heuristic algorithms for a weighted vertex coloring 
		problem." Journal of Heuristics 15.5 (2009): 503-526.

		Args:
			graph: The input graph on which model is to be implemented

		Returns:
			The value of the objective function (lower bound on weight of
			weighted coloring of the graph.)
		"""
		matrix_dimension = graph.number_of_nodes()
		model = Model("approximate")
		all_vertex_color_exprs = []
		
		y = model.addVars(matrix_dimension,matrix_dimension,vtype=GRB.BINARY)
		
		for i in range(matrix_dimension):
			vertex_color_expr = LinExpr()		
			for j in range(i+1):
				vertex_color_expr += y[i,j]
			model.addConstr(vertex_color_expr,GRB.EQUAL,1)

		for i in range(matrix_dimension):
			for j in range(matrix_dimension-1,i,-1):
				model.addConstr(y[j,i],GRB.LESS_EQUAL,y[i,i])
		
		for i in graph.edges():
			min_val = i[0] if i[0] <= i[1] else i[1]
			model.addConstr(y[i[0], min_val]+y[i[0],min_val], GRB.LESS_EQUAL, y[min_val, min_val])

		obj_function = LinExpr()
		weights = nx.get_node_attributes(graph, 'weight')

		for node in weights:
			obj_function += y[node,node]*weights[node]

		model.setObjective(obj_function, GRB.MINIMIZE)
		model.optimize()

		return model.getObjective().getValue()

except ImportError:
	pass


if __name__ == '__main__':
	pass