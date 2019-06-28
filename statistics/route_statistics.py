from __future__ import division
import copy
import sys
import os
sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),os.pardir)))


def occupancy_index(passengers, route, order, source_data, destination_data, source_destination_data):
	"""
	Function to calculate occupancy index of the
	given vehicle with the given set of passengers.

	Args:
		passengers: A list of the passengers of the vehicle.

		route: The route for the given vehicle, the route
		is a list with index of passenger representing the
		next point to go to.

		order: The order of source and destinations in 
		the route, S represents source and D represents
		destination.

		source_data: Distance matrix of sources of riders

		destination_data: Distance matrix of destinations
		of riders

		source_destination_data: Distance matrix of sources
		and destinations of riders
	
	Returns:
		The occupancy index and total travel distance of the given
		vehicle.
	"""
	total_user_travel_distance = 0.0
	total_vehicle_travel_distance = 0.0

	i = 0
	while i != len(route)-1:
		if order[i] == 'S' and order[i+1] == 'S':
			total_vehicle_travel_distance += source_data[route[i]][route[i+1]]
		elif order[i] == 'S' and order[i+1] == 'D':
			total_vehicle_travel_distance += source_destination_data[route[i]][route[i+1]]
		elif order[i] == 'D' and order[i+1] == 'S':
			total_vehicle_travel_distance += source_destination_data[route[i]][route[i+1]]
		else:
			total_vehicle_travel_distance += destination_data[route[i]][route[i+1]]

		i = i + 1

	for passenger in passengers:
		passenger_indices = [i for i, value in enumerate(route) if value == passenger]

		i = passenger_indices[0]
		while i != passenger_indices[1]:
			if order[i] == 'S' and order[i+1] == 'S':
				total_user_travel_distance += source_data[route[i]][route[i+1]]
			elif order[i] == 'S' and order[i+1] == 'D':
				total_user_travel_distance += source_destination_data[route[i]][route[i+1]]
			elif order[i] == 'D' and order[i+1] == 'S':
				total_user_travel_distance += source_destination_data[route[i]][route[i+1]]
			else:
				total_user_travel_distance += destination_data[route[i]][route[i+1]]

			i = i + 1

	if total_vehicle_travel_distance == 0.0:
		return 1, 0
	else:
		return total_user_travel_distance/(len(passengers)*total_vehicle_travel_distance), total_vehicle_travel_distance



def sharing_ratio(passengers, route, order, source_data, destination_data, source_destination_data, total_vehicle_distance):
	"""
	Function to calculate sharing index of the given 
	vehicle with the given set of passengers.

	Args:
		passengers: A list of the passengers of the vehicle.

		route: The route for the given vehicle, the route
		is a list with index of passenger representing the
		next point to go to.

		order: The order of source and destinations in 
		the route, S represents source and D represents
		destination.

		source_data: Distance matrix of sources of riders

		destination_data: Distance matrix of destinations
		of riders

		source_destination_data: Distance matrix of sources
		and destinations of riders
		
		total_vehicle_distance: The total distance travelled
		by the given vehicle.

	Returns:
		The total distance of the given vehicle that was spent sharing
		with maximum number of passengers in the ride in the vehicle.
	"""
	users_per_point = []
	previous_value = 0
	for i,passenger in enumerate(route):
		if order[i] == 'S':
			users_per_point.append(previous_value+1)
		else:
			users_per_point.append(previous_value-1)

	max_value_index = users_per_point.index(max(users_per_point))

	if order[max_value_index] == 'S' and order[max_value_index+1] == 'S':
		combined_sharing_distance = source_data[route[max_value_index]][route[max_value_index+1]]
	elif order[max_value_index] == 'S' and order[max_value_index+1] == 'D':
		combined_sharing_distance += source_destination_data[route[max_value_index]][route[max_value_index+1]]
	elif order[max_value_index] == 'D' and order[max_value_index+1] == 'S':
		combined_sharing_distance += source_destination_data[route[max_value_index]][route[max_value_index+1]]
	else:
		combined_sharing_distance += destination_data[route[max_value_index]][route[max_value_index+1]]

	return combined_sharing_distance


def in_vehicle_user_stats(passengers, route, source_data, destination_data, source_destination_data):
	"""
	Function to calculate route statistics of the
	given vehicle with the given set of passengers
	and given route that it is following.

	Args:
		passengers: A list of the passengers of the vehicle.

		route: The route for the given vehicle, the route
		is a list with index of passenger representing the
		next point to go to.

		source_data: Distance matrix of sources of riders

		destination_data: Distance matrix of destinations
		of riders

		source_destination_data: Distance matrix of sources
		and destinations of riders
	
	Returns:
		The occupancy index, sharing distance and total travel 
		distance of the given vehicle.
	"""
	route = route.split(" ")
	order = []

	for i, passenger in enumerate(route):
		route[i] = int(passenger)

	for passenger in route:
		if passenger not in order:
			order.append("S")
		else:
			order.append("D")

	occupancy_index_value, total_vehicle_distance = occupancy_index(passengers, route, order, source_data, destination_data, source_destination_data)
	combined_sharing_distance = sharing_ratio(passengers, route, order, source_data, destination_data, source_destination_data, total_vehicle_distance)

	return [occupancy_index_value, combined_sharing_distance, total_vehicle_distance]


if __name__ == '__main__':
	pass