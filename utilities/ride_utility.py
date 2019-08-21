from __future__ import division
import requests
import json
import polyline
import osrm
import urllib
from urllib import quote


def polyline_encoded_table(request, port):
	"""
	Function that uses the python wrapper
	for osrm in order to get the distance
	matrix between given input points by 
	using the table service of the osrm server
	hosted on the input host.

	Args:
		request: A list of objects of the class
		Request corresponding to each rider in the
		system.

		port: The full link to the localhost port on
		which osrm server is running.  
	"""

	osrm.RequestConfig.host = port

	sources_data = [(i.source_long, i.source_lat) for i in request]
	destinations_data = [(i.dest_long, i.dest_lat) for i in request]

	coordinates = []
	for element in sources_data:
		coordinates.append(element)

	for element in destinations_data:
		coordinates.append(element)

	response = osrm.table(coordinates, output='raw', annotations='distance')

	return response['distances']

def get_distance_between_points(point_1, point_2, port):
	"""
	Function to get the driving (road) distance 
	between two points specified in latitude
	longitude form.

	Args:
		point_1: First point

		point_2: Second point

		port: The full link to localhost port
		on which osrm server is running.

	Returns:
		Driving distance between point_1 and
		point_2.
	"""	
	request_string = port +'/route/v1/driving/'+str(point_1[1])+','+str(point_1[0])+';'+str(point_2[1])+','+str(point_2[0])+'?overview=false'
	response = requests.get(request_string)
	json_dictionary = json.loads(response.text)

	return float(json_dictionary['routes'][0]['distance'])


def time_between_points(points, port):
	"""
	Function to get the driving time between 
	all rides.

	Args:
		points: All points in between whom
		time needs to be calculated.

		port: The full link to localhost port
		on which osrm server is running.

	Returns:
		A 2D array having travel time between
		all points.
	"""
	lat_long_string = ""
	for point in points:
		lat_long_string = lat_long_string + str(point[1]) +',' + str(point[0]) +';'

	non_polyline_request_string = port+'/table/v1/driving/'+lat_long_string[:len(lat_long_string)-1]
	response = requests.get(polyline_request_string)
	json_dictionary = json.loads(response.text)

	return json_dictionary['durations']


def create_rates_for_slabs(distances, slab):
	"""
	Create rate matrix according to given slabs
	by reading distance matrix from the input
	file.

	Args:
		distances: The distance list corresponding
		to distance of each node from destination.

		slab: A dictionary with all but last keys
		as starting distance of slab and value as
		list of two elements with first value as
		base price and second as extra rate per km
		for that slab.

	Returns:
		A list of rates for each node in the vertex.
	"""
	rates = []
	for distance in distances:
		for base in slab:
			if distance != '' and int(distance) >= base[0]*1000 and int(distance) < base[1]*1000:
				rates.append(slab[base][0] + int(distance)*slab[base][1])

	return rates


def get_distance_to_travel(distance_matrix):
	"""
	Create a list of distances that every passenger
	has to travel stored in the file.

	Args:
		distance_matrix: The distance matrix.

	Returns:
		List of distances each person has to travel
		to reach the destination.
	"""
	number_of_people = len(distance_matrix)

	return distance_matrix[number_of_people-1][:]


def create_average_distance_between_sources(source_data, graph, option):
	"""
	Create distance matrix according to distance
	from sources of each user, the distance value
	will depict average distance from every other
	person's source.

	Args:
		source_data: Distance matrix of sources 
		of riders.

		graph: The networkx graph corresponding to
		each rider in the system.

		option: Has value 0 if average distance between
		all, and 1 if average distance between admissible
		riders.

	Returns:
		A list of distances for each node in the vertex.
	"""
	source_distances = []
	for i, data in enumerate(source_data):
		if option == 0:
			source_distances.append(sum(data)/len(data))
		else:
			total_sum_for_rider = 0
			number_of_admissible = 0
			for j, distance in enumerate(data):
				if graph.has_edge(i,j) == False:
					total_sum_for_rider += distance
					number_of_admissible += 1

			source_distances.append(total_sum_for_rider/number_of_admissible)
			
	return source_distances


def update_positions(active_riders, current_vehicles, time_elapsed, time_start, source_time, destination_time, source_destination_time, source_distance, destination_distance, source_destination_distance):

	passenger_iterator = 0
	for vehicle in current_vehicles:
		route = vehicle.route
		vehicle_start_time = vehicle.time_start

		# for i in range(len(vehicle.passengers)):
			



if __name__ == '__main__':
	pass