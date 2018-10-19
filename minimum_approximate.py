from gurobipy import *
import networkx as nx

def give_model_approximate(graph)
	matrix_dimension = graph.number_of_nodes()
	model = Model("approximate")
	all_vertex_color_exprs = []
	
	y = model.addVars(matrix_dimension,matrix_dimension,vtype=GRB.BINARY)
	
	for i in range(matrix_dimension):
		vertex_color_expr = LinExpr()		
		for j in range(i+1):
			vertex_color_expr += y[i,j]
		all_vertex_color_expr.append(vertex_color_expr)
 

if __name__ == '__main__':
