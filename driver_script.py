import weighted_vertex_coloring as wvc
import utilities as utils
import infinite_vehicle_allocator as iva
import networkx
import color_splitter as cs
import sys
import coloring_techniques as ct
from Vehicle import Vehicle, comparator

def vehicles_manifest():
	vehicle_1 = Vehicle(1,4,525.0)
	vehicle_2 = Vehicle(2,6,850.0)
	vehicle_3 = Vehicle(3,12,1000.0)
	vehicle_4 = Vehicle(4,35,3000.0)
	vehicle_5 = Vehicle(5,41,3200.0)

	vehicles_list = []
	vehicles_list.append(vehicle_1)
	vehicles_list.append(vehicle_2)
	vehicles_list.append(vehicle_3)
	vehicles_list.append(vehicle_4)	
	vehicles_list.append(vehicle_5)

	return vehicles_list



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
	weight, coloring = wvc.give_best_coloring(graph, 50)
	print(weight)
	
	total_operator_cost = 0
	vehicles = vehicles_manifest()
	vehicles.sort(comparator)

	for color in coloring:
		# cost, allotment = cs.color_spiltter(coloring[color], vehicles)
		cost, allotment = iva.allot_vehicles(coloring[color], vehicles)
		total_operator_cost += cost

	revenue = sum(rates)-total_operator_cost
	print("Revenue for WVC: %d" %revenue)

	standard_operator_cost = 0
	standard_coloring = ct.dsatur_coloring(graph)
	for color in standard_coloring:
		standard_cost, standard_allotment = cs.color_spiltter(standard_coloring[color], vehicles)
		standard_operator_cost += cost

	standard_revenue = sum(rates)-standard_operator_cost
	print("Revenue for DSATUR: %d" %standard_revenue)

if __name__ == '__main__':
	runner('saatvik_data_len_129_152540.pkl')