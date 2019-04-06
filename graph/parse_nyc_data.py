from __future__ import division
import sys
sys.path.insert(0, 'D:/College/VPool/')
import pandas as pd
import utilities.ride_utility as rUtils
from datetime import datetime
from models.Request import Request


def create_osrm_table(requests, port):
	"""
	Function to create a 2D array containing
	information about distance and travel time
	between points.

	Args:
		requests: A list of request objects
		port: The port on which osrm is running.

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


def check_admissibility(i, j, delta_1, delta_2, source_data, destination_data, source_destination_data, delta=1.2):
	"""
	Function to check whether two requests are admissible or not
	by putting in the given criterion (flexible). Admissibility
	is checked on the basis of difference in between source and 
	destination.

	Args:
		i: Index of first request object
		j: Index of second request object
		delta_1: First condition for sources
		delta_2: Second condition for destination
		source_data: The array containing information about requests' sources
		destination_data: The array containing information about requests' destinations
		source_destination_data: The array containing information about requests' source and destinations
		delta: Condition for total travel time
		delta: Third condition for overall trip

	Returns:
		True if the two requests are admissible, false otherwise. 
	"""
	if source_destination_data[j][i] + source_data[i][j] <= 1.2*source_destination_data[i][i] and source_destination_data[j][i] + destination_data[i][j] <= 1.2*source_destination_data[j][j]:
		return True
	elif source_destination_data[i][j] + destination_data[j][i] <= 1.2*source_destination_data[i][i] and source_destination_data[i][j] + source_data[j][i] <= 1.2*source_destination_data[j][j]:
		return True
	elif source_data[i][j]+source_destination_data[j][j]+destination_data[j][i] <= 1.2*source_destination_data[i][i]:
		return True
	elif source_data[j][i]+source_destination_data[i][i]+destination_data[i][j] <= 1.2*source_destination_data[j][j]:
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
		filepath: The path of the csv file.
		time_start: Start time of subset.
		time_end: End time of subset.

	Returns:
		A pandas dataframe containing information
		about rides of that particular time period.
	"""
	ny_dataset = pd.read_csv(filepath)
	ny_dataset['pickup_datetime'] = ny_dataset['pickup_datetime'].map(change_string_to_datetime)

	time_start = change_string_to_datetime(time_start)
	time_end = change_string_to_datetime(time_end)
	start_condition = ny_dataset['pickup_datetime'] > time_start
	end_condition = ny_dataset['pickup_datetime'] < time_end

	subset = ny_dataset[start_condition & end_condition]
	return ny_dataset


def create_request_objects(data):
	"""
	Function to create request objects
	from the pandas dataframe containg
	information about the requests.

	Args:
		data: The pandas dataframe

	Returns:
		A list of objects of request
		type.
	"""
	requests = []
	for index, row in data.iterrows():
		request = Request(row['pickup_latitude'],row['pickup_longitude'],row['dropoff_latitude'],row['dropoff_longitude'],row['pickup_datetime'],row['passenger_count'])
		requests.append(request)

	if len(requests) > 100:
		return requests[:100]
	else:
		return requests


def create_adjacency_matrix(requests, delta_1, delta_2, port):
	"""
	Function to create adjacency matrix from the
	input data in accordance with given constraints
	in order to be further processed and have graph
	algorithms applied on it.

	Args:
		requests: A list of objects of request type
		containing information about every person
		in the system.
		delta_1: First condition for sources.
		delta_2: Second condition for destination.
		port: The port on which osrm is running.

	Returns:
		4 lists having the adjacency matrix of the riders,
		distances between sources, destinations and sourc
		destination pairs.
		
	It is to be noted that in adjacency matrix, 0 means
	not admissible and 1 means admissible.
	"""
	adjacency_matrix = []
	source_data, destination_data, source_destination_data = create_osrm_table(requests, port)
	for i,first_request in enumerate(requests):
		data = []
		for j,second_request in enumerate(requests):
			admissibility = check_admissibility(i, j, delta_1, delta_2, source_data, destination_data, source_destination_data, 1.2)
			if admissibility == True:
				data.append(1)
			elif admissibility == False:
				data.append(0)
		adjacency_matrix.append(data)

	return adjacency_matrix, source_data, destination_data, source_destination_data


def create_distance_matrix(requests, port):
	"""
	Function to create distance matrix depicting
	distances between all pairs of requests.
	
	Args:
		requests: All the request objects
		port: The port on which osrm is running.
	
	Returns:
		A list containing distance of each request from its destination.
	"""

	distances = []
	for request in requests:
		distance = rUtils.get_distance_between_points([request.source_lat, request.source_long], [request.dest_lat, request.dest_long], port)
		distances.append(distance)
	return distances


if __name__ == '__main__':
	read_dataset('nyc_taxi_data_2014.csv')