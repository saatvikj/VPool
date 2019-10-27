from __future__ import division
import sys
import os
sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),os.pardir)))
import pandas as pd
import utilities.ride_utility as rUtils
import random
from datetime import datetime
from models.Request import Request


def osrm_table(requests, port):
	"""
	Function to create 2D arrays containing
	information about distance between all locations
	of the riders.

	This works using the table service of the osrm
	server.

	Args:
		requests: A list of objects of the class
		Request corresponding to each rider in the
		system.

		port: The full link to localhost port on which
		osrm server is running,

	Returns:
		Three 2D arrays containg all information about
		distances between sources, destinations and sourc
		destination pairs.
	"""
	n = len(requests)

	results = rUtils.polyline_encoded_table(requests, port)

	source_data = []
	destination_data = []
	source_destination_data = []

	for i in range(n):
		source_data.append(results[i][:n])
		destination_data.append(results[n+i][n:])
		source_destination_data.append(results[i][n:])

	return source_data, destination_data, source_destination_data


def create_osrm_table(requests, port):
	"""
	Function to create 2D arrays containing
	information about distance between all locations
	of the riders.

	This works with a point-wise query for all the
	points using the osrm route service.

	Args:
		requests: A list of objects of the class
		Request corresponding to each rider in the
		system.

		port: The full link to localhost port on which
		osrm server is running.

	Returns:
		Three 2D arrays containg all information about
		distances between sources, destinations and sourc
		destination pairs.
	"""
	source_data = []
	destination_data = []
	source_destination_data = []

	for i in requests:

		source_sub_row = []
		destination_sub_row = []
		source_destination_sub_row = []

		for j in requests:
			source_sub_row.append(rUtils.get_distance_between_points([i.source_lat,i.source_long],[j.source_lat,j.source_long], port))
			destination_sub_row.append(rUtils.get_distance_between_points([i.dest_lat,i.dest_long],[j.dest_lat,j.dest_long], port))
			source_destination_sub_row.append(rUtils.get_distance_between_points([i.source_lat,i.source_long],[j.dest_lat,j.dest_long], port))

		source_data.append(source_sub_row)
		destination_data.append(destination_sub_row)
		source_destination_data.append(source_destination_sub_row)

	return source_data, destination_data, source_destination_data


def check_admissibility(i, j, source_data, destination_data, source_destination_data, delta, i_travelled = 0, j_travelled = 0):
	"""
	Function to check whether two requests are admissible or not
	by putting in the given criterion (flexible). Admissibility
	is checked on the basis of ratio of distances of combined and
	individual minimum distance routes.

	Args:
		i: Index of first request object

		j: Index of second request object

		source_data: Distance matrix of sources of riders

		destination_data: Distance matrix of destinations
		of riders

		source_destination_data: Distance matrix of sources
		and destinations of riders

		delta: The tolerance value used for admissibility

		i_travelled: Distance already travelled by rider i.

		j_travelled: Distance already travelled by rider j.

	Returns:
		True if the two requests are admissible, false otherwise. 
	"""
	if source_destination_data[j][i] + source_data[i][j] <= delta*source_destination_data[i][i] - i_travelled and source_destination_data[j][i] + destination_data[i][j] <= delta*source_destination_data[j][j] - j_travelled:
		return True
	elif source_destination_data[i][j] + destination_data[j][i] <= delta*source_destination_data[i][i] - i_travelled and source_destination_data[i][j] + source_data[j][i] <= delta*source_destination_data[j][j] - j_travelled:
		return True
	elif source_data[i][j]+source_destination_data[j][j]+destination_data[j][i] <= delta*source_destination_data[i][i] - i_travelled and j_travelled <= (delta-1)*source_destination_data[j][j]:
		return True
	elif source_data[j][i]+source_destination_data[i][i]+destination_data[i][j] <= delta*source_destination_data[j][j] - j_travelled and i_travelled <= (delta-1)*source_destination_data[i][i]:
		return True
	else:
		return False


def change_string_to_datetime(column):
	"""
	Function to take input string and convert
	it into a datetime format. Used to modify
	the pandas dataframe.

	Args:
		column: The input string in the format
		"YYYY-MM-DD HH:MM:SS"

	Returns:
		A datetime object corresponding to the
		string.
	"""
	column = datetime.strptime(column, '%Y-%m-%d %H:%M:%S')
	return column


def read_dataset(filepath, time_start='2014-01-01 14:00:00', time_end='2014-01-01 14:05:00'):
	"""
	Function to read the NYC dataset and return
	a subset of it with requests lying in a
	particular day (flexible).

	Args:
		filepath: Full path of file containing data.

		time_start: Start time to query the input
		dataset for data.
		
		time_end: Start time to query the input
		dataset for data.

	Returns:
		A pandas dataframe containing information
		about rides of the particular time period
		defined by time_start and time_end.
	"""
	ny_dataset = pd.read_csv(filepath)
	ny_dataset['pickup_datetime'] = ny_dataset['pickup_datetime'].map(change_string_to_datetime)

	time_start = change_string_to_datetime(time_start)
	time_end = change_string_to_datetime(time_end)
	start_condition = ny_dataset['pickup_datetime'] > time_start
	end_condition = ny_dataset['pickup_datetime'] < time_end
	airport_condition = ny_dataset['rate_code'] == 1
	pickup_latititude_condition = ny_dataset['pickup_latitude'] > 40.0
	dropoff_latititude_condition = ny_dataset['dropoff_latitude'] > 40.0 	
	pickup_longitude_condition = ny_dataset['pickup_longitude'] > -75.0
	dropoff_longitude_condition = ny_dataset['dropoff_longitude'] > -75.0 

	subset = ny_dataset[start_condition & end_condition & airport_condition & pickup_latititude_condition & dropoff_latititude_condition & pickup_longitude_condition & dropoff_longitude_condition]
	return subset


def create_request_objects(data, size_limit):
	"""
	Function to create request objects
	from the pandas dataframe containg
	information about the requests.

	Args:
		data: The pandas dataframe containing
		information about all rides.

		size_limit: The upper bound on number 
		of objects that will be created from
		the riders, used only to categorize
		data on the basis of input size.
	
	Returns:
		A list of objects of request
		type.
	"""
	requests = []
	for index, row in data.iterrows():
		request = Request(row['pickup_latitude'],row['pickup_longitude'],row['dropoff_latitude'],row['dropoff_longitude'],row['pickup_datetime'],row['passenger_count'])
		requests.append(request)

	if len(requests) > size_limit:
		return random.sample(requests, size_limit)
	else:
		return requests


def create_adjacency_matrix(requests, port, delta):
	"""
	Function to create adjacency matrix from the
	input data in accordance with given constraints
	in order to be further processed and have graph
	algorithms applied on it.

	Args:
		requests: A list of objects of the class
		Request corresponding to each rider in the
		system.

		port: The full link to localhost port on which
		osrm server is running.
		
		delta: The tolerance value used for admissibility

	Returns:
		4 lists having the adjacency matrix of the riders,
		distances between sources, destinations and sourc
		destination pairs.
		
	It is to be noted that in adjacency matrix, 0 means
	not admissible and 1 means admissible.
	"""
	adjacency_matrix = []
	# source_data, destination_data, source_destination_data = create_osrm_table(requests, port)
	source_data, destination_data, source_destination_data = osrm_table(requests, port)
	for i,first_request in enumerate(requests):
		data = []
		for j,second_request in enumerate(requests):
			admissibility = check_admissibility(i, j, source_data, destination_data, source_destination_data, delta)
			if admissibility == True:
				data.append(1)
			elif admissibility == False:
				data.append(0)
		adjacency_matrix.append(data)

	return adjacency_matrix, source_data, destination_data, source_destination_data


def create_distance_matrix(source_destination_data):
	"""
	Function to create distance matrix depicting
	distances between all pairs of requests.
	
	Args:
		source_destination_data: Distance matrix of sources
		and destinations of riders
	
	Returns:
		A list containing distance of each rider from its destination.
	"""

	distances = []
	for i in range(len(source_destination_data)):
		distances.append(source_destination_data[i][i])
	return distances


if __name__ == '__main__':
	pass