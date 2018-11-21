import weighted_vertex_coloring as wvc
import utilities as utils
import networkx
import sys

def runner(filename):

	slab = {}
	slab[(0,5)] = [50,0]
	slab[(5,10)] = [70,0]
	slab[(10,sys.maxsize)] = [70,2]

	utils.unpickle_to_file(filename, 'adjacency_matrix.txt', 'distance_matrix.txt')
	graph = wvc.create_graph_from_input('adjacency_matrix.txt')
	distance_from_destination = wvc.get_distance_to_travel('distance_matrix.txt')
	rates = wvc.create_rates_for_slabs('distance_matrix.txt', slab)
	graph = wvc.add_weight_to_vertices(graph, rates)
	weight, coloring = wvc.give_best_coloring(graph, 100)
	print(weight)
	print(coloring)

if __name__ == '__main__':
	runner('saatvik_data_len_129_152540.pkl')