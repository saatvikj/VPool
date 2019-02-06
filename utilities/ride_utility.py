import requests
import json
import polyline


def get_distance_between_points(point_1, point_2):
	"""
	Function to get the driving (road) distance 
	between two points specified in latitude
	longitude form.

	Args:
		point_1: First point
		point_2: Second point

	Returns:
		Driving distance between point_1 and
		point_2.
	"""	
	request_string = 'http://127.0.0.1:5000/route/v1/driving/'+str(point_1[1])+','+str(point_1[0])+';'+str(point_2[1])+','+str(point_2[0])+'?overview=false'
	response = requests.get(request_string)
	json_dictionary = json.loads(response.text)

	return float(json_dictionary['routes'][0]['distance'])


def time_between_points(points):
	"""
	Function to get the driving time between 
	all rides.

	Args:
		points: All points in between whom
		time needs to be calculated.

	Returns:
		A 2D array having travel time between
		all points.
	"""
	encoded_string = polyline_encoding(points)
	request_string = 'http://127.0.0.1:5000/table/v1/driving/polyline('+encoded_string+')'
	response = requests.get(request_string)
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


if __name__ == '__main__':
	pass