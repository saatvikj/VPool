from __future__ import division
import requests
import json
import polyline
from urllib import quote


def get_distance_between_points(point_1, point_2, port):
	"""
	Function to get the driving (road) distance 
	between two points specified in latitude
	longitude form.

	Args:
		point_1: First point
		point_2: Second point
		port: The port running osrm.

	Returns:
		Driving distance between point_1 and
		point_2.
	"""	
	request_string = 'http://127.0.0.1:'+ str(port) +'/route/v1/driving/'+str(point_1[1])+','+str(point_1[0])+';'+str(point_2[1])+','+str(point_2[0])+'?overview=false'
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
		port: The port running osrm.

	Returns:
		A 2D array having travel time between
		all points.
	"""
	lat_long_string = ""
	for point in points:
		lat_long_string = lat_long_string + str(point[1]) +',' + str(point[0]) +';'

	encoded_string = polyline_encoding(points)
	non_polyline_request_string = 'http://127.0.0.1:'+str(port)+'/table/v1/driving/'+lat_long_string[:len(lat_long_string)-1]
	polyline_request_string = 'http://127.0.0.1:5000/table/v1/driving/polyline('+quote(polyline_encoding([(point[0],point[1]) for point in points]))+')'
	response = requests.get(polyline_request_string)
	json_dictionary = json.loads(response.text)

	return json_dictionary['durations']

def polyline_encoding(points):
	"""
	Function to get a polyline encoded
	string of the latitude and longitude
	of the given point.

	Args: 
		points: The points to be encoded.

	Returns:
		A string encoding of the points.

	The encoding is based on Google's
	algorithm: http://goo.gl/PvXf8Y.
	"""
	return polyline.encode(points)


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


def divide_and_conquer(requests):
	"""
	Function to appropriately divide the requests
	into sub parts and then calculate the distance 
	matrix for the entire part using the smaller
	parts.

	Args:
		requests: The request objects.

	Returns:
		A 2D matrix having travel distance between 
		all points.
	"""
	pass



def create_average_distance_between_sources(source_data):
	"""
	Create distance matrix according to distance
	from sources of each user, the distance value
	will depict average distance from every other
	person's source.

	Args:
		source_data: The matrix having distances
		between each of the sources.

	Returns:
		A list of distances for each node in the vertex.
	"""
	source_distances = []
	for i in source_data:
		source_distances.append(sum(i)/len(i))


	return source_distances


if __name__ == '__main__':
	pass