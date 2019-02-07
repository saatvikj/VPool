from __future__ import division
from graph import weighted_vertex_coloring as wvc
from graph import initiate_graph as init
from utilities import pickle_utility as pUtils
from utilities import csv_utility as cUtils
from utilities import ride_utility as rUtils
from optimization import infinite_vehicle_allocator as iva
from graph import coloring_techniques as ct
from statistics import distance_statistics as stats
from models.Vehicle import Vehicle, comparator
import networkx
import sys
import numpy as np


def vehicles_manifest():
	"""
	Function to return list of available
	vehicles as vehicle objects.
	
	Args:
		None

	Returns:
		List of vehicle objects with given
		specifications.
	"""
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
	"""
	Main runner function that initializes the graph, 
	assigns weights to vertices, applies all algorithms 
	to it and obtains response.
	
	Args:
		filename: The name of file containing data

	Returns:
		Void

	"""
	#Cost slabs is a dictionary where keys are 2 tuples with first value representing
	#start distance and second representing end distance and values are lists with first
	#element as base charge and second as per km charge (in rs)

	slab = {}
	slab[(0,5)] = [50,0]
	slab[(5,10)] = [70,0]
	slab[(10,sys.maxsize)] = [70,2]

	option = int(sys.argv[1])
	adjacency_matrix = []
	distance_from_destination = []
	distance_matrix = []
	if option == 1:
		adjacency_matrix, distance_matrix = pUtils.unpickle_data(filename)
		distance_from_destination = distance_matrix
	else:
		adjacency_matrix, distance_from_destination = cUtils.csv_to_data(filename)

	if len(sys.argv > 2):
		pUtils.pickle_data(adjacency_matrix, distance_from_destination, sys.argv[3])

	graph = init.create_graph_from_input(adjacency_matrix)
	rates = rUtils.create_rates_for_slabs(distance_from_destination, slab)
	graph = init.add_weight_to_vertices(graph, rates)
	weight, coloring = wvc.give_best_coloring(graph, 1)
	total_operator_cost = 0
	vehicles = vehicles_manifest()
	vehicles.sort(comparator)
	total_used_vehicles = 0
	actual_distance = 0
	total_distance = 0
	for color in coloring:
		cost, allotment = iva.allot_vehicles(coloring[color], vehicles)
		total_used_vehicles += len(allotment)
		total_operator_cost += cost
		distance_results = stats.get_distance_from_allocation(allotment,distance_from_destination)
		for stat in distance_results:
			actual_distance += stat[1]
			total_distance += stat[2]

	revenue = sum(rates)-total_operator_cost
	print("Revenue for WVC: %d" %revenue)
	print(total_used_vehicles)
	print(total_distance)
	print(actual_distance)

	standard_operator_cost = 0
	standard_coloring = ct.seq_coloring(graph)
	for color in standard_coloring:
		standard_cost, standard_allotment = iva.allot_vehicles(standard_coloring[color], vehicles)
		standard_operator_cost += standard_cost

	standard_revenue = sum(rates)-standard_operator_cost

	print("Revenue for DSATUR: %d" %standard_revenue)


if __name__ == '__main__':
	runner(sys.argv[2])