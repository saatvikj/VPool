from __future__ import division
from graph import weighted_vertex_coloring as wvc
from graph import initiate_graph as init
from utilities import pickle_utility as pUtils
from utilities import csv_utility as cUtils
from utilities import ride_utility as rUtils
from optimization import infinite_vehicle_allocator as iva
from optimization import naive_wvc_solution as naive
from optimization import minimum_approximate as ma
from graph import coloring_techniques as ct
from statistics import distance_statistics as dStats
from statistics import vehicle_statistics as vStats
from statistics import three_user_allocation as three
from statistics import coloring_statistics as cStats
from models.Vehicle import Vehicle, comparator
import networkx
import sys
import numpy as np
import copy
import math


cost_slab = {
   4: [350, 450, 500, 525],
   6: [600, 700, 750, 850],
   12: [650, 800, 850, 1000],
   35: [2800, 2800, 2800, 3000],
   41: [3000, 3000, 3000, 3200],
}


def vehicles_manifest(four=525.0, six=850.0, twelve=1000.0, thirty_five=3000.0, forty_one= 3200.0):
	"""
	Function to return list of available
	vehicles as vehicle objects.
	
	Args:
		None

	Returns:
		List of vehicle objects with given
		specifications.
	"""
	vehicle_0 = Vehicle(0,3,400.0)
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


def runner(filename, option, output=None,time_start='2014-01-01 10:00:00', time_end='2014-01-01 10:05:00', port=5000):
	"""
	Main runner function that initializes the graph, 
	assigns weights to vertices, applies all algorithms 
	to it and obtains response.
	
	Args:
		filename: The name of file containing data
		option: 1 for pickled data, 2 for csv
		output: Name of output pickle file (optional)
		time_start: Start time for subset.
		time_end: End time for subset.
		port: The port running osrm.

	Returns:
		Void
	"""
	#Cost slabs is a dictionary where keys are 2 tuples with first value representing
	#start distance and second representing end distance and values are lists with first
	#element as base charge and second as per km charge (in rs)

	slab = {}
	slab[(0,5)] = [0,15]
	slab[(5,10)] = [0,15]
	slab[(10,sys.maxsize)] = [0,15]

	adjacency_matrix = []
	distance_from_destination = []
	distance_matrix = []
	if int(option) == 1:
		adjacency_matrix, distance_matrix, source_data, destination_data, source_destination_data = pUtils.unpickle_data(filename)
		distance_from_destination = distance_matrix
	else:
		adjacency_matrix, distance_from_destination, source_data, destination_data, source_destination_data = cUtils.csv_to_data(filename, time_start, time_end, port)

	if output is not None:
		pUtils.pickle_data(adjacency_matrix, distance_from_destination, source_data, destination_data, source_destination_data, output)

	maximum_distance = max(distance_from_destination)/1000.0
	graph = init.create_graph_from_input(adjacency_matrix)
	rates = rUtils.create_rates_for_slabs(distance_from_destination, slab)
	average_distances = rUtils.create_average_distance_between_sources(source_data)
	graph = init.add_weight_to_vertices(graph, average_distances)
	
	vehicles = vehicles_manifest()
	vehicles.sort(comparator)

	for vehicle in vehicles:
		vehicle.cost = math.ceil(maximum_distance)*15

	weight, coloring = wvc.give_best_coloring(graph, 50)
	wvc_results = cStats.coloring_statistics(0, coloring, vehicles, distance_from_destination, source_data, destination_data, source_destination_data, copy.deepcopy(rates))

	print("Revenue for WVC: %d" %wvc_results[0])

	standard_coloring = ct.dsatur_coloring(graph)
	standard_weight = ct.calculate_coloring_weight(graph, standard_coloring)
	standard_coloring_results = cStats.coloring_statistics(0, standard_coloring, vehicles, distance_from_destination, source_data, destination_data, source_destination_data, copy.deepcopy(rates))

	print("Revenue for DSATUR: %d" %standard_coloring_results[0])

	return [graph.number_of_nodes(), wvc_results[0], standard_coloring_results[0] , wvc_results[1]-standard_coloring_results[1], wvc_results[2], standard_coloring_results[2], wvc_results[3], standard_coloring_results[3], wvc_results[4], standard_coloring_results[4], wvc_results[5], standard_coloring_results[5], wvc_results[6], standard_coloring_results[6]]


if __name__ == '__main__':
	if len(sys.argv) > 3:
		runner(sys.argv[2],sys.argv[1], sys.argv[3])
	else:
		runner(sys.argv[2], sys.argv[1])