from utilities import csv_utility as cUtils
from utilities import dynamic_utility as dUtils
from utilities import ride_utility as rUtils
from graph import initiate_graph as init
from graph import weighted_vertex_coloring as wvc
from graph import parse_nyc_data as nyc
from graph import coloring_techniques as ct
from statistics import distance_statistics as dStats
from statistics import vehicle_statistics as vStats
from statistics import coloring_statistics as cStats
from models.Vehicle import Vehicle, comparator


def vehicles_manifest(four=525.0, six=850.0, twelve=1000.0, thirty_five=3000.0, forty_one= 3200.0):
	"""
	Function to return list of available
	vehicles as vehicle objects.
	
	Args:
		four (optional): The running cost of 4 seater vehicle.

		six (optional): The running cost of 6 seater vehicle.

		twelve (optional): The running cost of 12 seater vehicle.

		thirty_five (optional): The running cost of 35 seater vehicle.

		forty_one (optional): The running cost of 41 seater vehicle.

	Returns:
		List of vehicle objects with given
		specifications.
	"""
	vehicle_1 = Vehicle(1,4,four)
	vehicle_2 = Vehicle(2,6,six)
	vehicle_3 = Vehicle(3,12,twelve)
	vehicle_4 = Vehicle(4,35,thirty_five)
	vehicle_5 = Vehicle(5,41,forty_one)

	vehicles_list = []
	vehicles_list.append(vehicle_1)
	vehicles_list.append(vehicle_2)
	vehicles_list.append(vehicle_3)
	vehicles_list.append(vehicle_4)	
	vehicles_list.append(vehicle_5)

	return vehicles_list


def dynamic_simulation_runner(filename, option, time_start, time_end):

	all_requests = cUtils.csv_to_requests(filename)
	time_elapsed = 0

	current_time = dUtils.convert_to_datetime(time_start)
	time_end = dUtils.convert_to_datetime(time_end)

	active_riders = []
	new_requests = []
	current_vehicles = []

	source_distance = [[]]
	destination_distance = [[]]
	source_destination_distance = [[]]

	source_time = [[]]
	destination_time = [[]]
	source_destination_time = [[]]

	while current_time != time_end:

		#Update active riders list, if an existing rider has finished ride in last checked time, he/she is removed 
		#Checks current position according to rider start time, rider vehicle and time elapsed and then updates their
		#positions as well. Position will be updated by seeing current position, how much time has passed and how much
		#time it takes from going to different points in the vehicle route.
		active_riders = rUtils.update_positions(active_riders, current_vehicles, time_elapsed, time_start, source_time, destination_time, source_destination_time, source_distance, destination_distance, source_destination_distance)

		#Select all new requests made since previous time
		#Selects by giving start time and end time
		new_requests = cUtils.find_new_requests(all_requests, time_start+time_elapsed, time_start+time_elapsed+5 minutes)

		#Update active vehicles list, if all riders of vehicle have finished ride, vehicle is removed from system
		#Updates by checking if all riders of vehicle have been removed from active riders or not
		#Later will be used to keep track of required number of vehicles
		current_vehicles = rUtils.update_vehicles(current_vehicles, active_riders)

		#Create the distance and time matrices corresponding to all the riders
		#From riders it will then be upgraded to vehicle based admissibility
		source_distance, destination_distance, source_destination_distance = rUtils.get_distance_data(active_riders, new_requests) 
		source_time, destination_time, source_destination_time = rUtils.get_time_data(active_riders, new_requests)

		adjacency_matrix, node_type = dUtils.create_vehicle_rider_adjacency_matrix(source_distance, destination_distance, source_destination_distance, new_requests, active_riders)
		graph = init.initiate_dyanmic_graph(adjacency_matrix, node_type)

		rates = rUtils.create_rates_for_slabs(distance_from_destination, slab)
		average_distances = rUtils.create_average_distance_between_sources(source_distance, graph, 0)
		average_distances = rUtils.create_weights_with_vehicles(average_distances, current_vehicles)

		graph = init.add_weight_to_vertices(graph, average_distances)

		weight, coloring = wvc.give_best_coloring(graph, 10)
		wvc_results = cStats.coloring_statistics(coloring, vehicles, distance_from_destination, source_distance, destination_distance, source_destination_distance, copy.deepcopy(rates), requests, text_output, 'wvc','12.972442,77.580643\n')

		standard_coloring = ct.dsatur_coloring(graph)
		standard_weight = ct.calculate_coloring_weight(graph, standard_coloring)
		standard_coloring_results = cStats.coloring_statistics(standard_coloring, vehicles, distance_from_destination, source_distance, destination_distance, source_destination_distance, copy.deepcopy(rates), requests, text_output, 'std','12.972442,77.580643\n')