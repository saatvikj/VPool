from __future__ import division
import pandas as pd
import numpy
import osrm
from datetime import datetime
from Request import Request


def create_osrm_table(requests):
	"""
	Function to create a numpy array containing
	information about distance and travel time
	between points.

	Args:
		requests: A list of request objects
	
	Returns:
		A numpy array containg all information.
	"""
	data = []
	for request in requests:
		data.append([request.source_lat,request.source_long])

	for request in requests:
		data.append([request.dest_lat, request.dest_long])

	list_id = [i for i in range(2*len(requests))]
	time_matrix, snapped_coords = osrm.table(data,ids_origin=list_id,output='dataframe')

	return time_matrix


def check_admissibility(i, j, delta_1, delta_2, data, n):
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
		data: The numpy array containing information about requests
		n: Number of requests in total

	Returns:
		True if the two requests are admissible, false otherwise. 
	"""
	if data[i,j] < delta_1 and data[n+i,n+j] < delta_2:
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


def read_dataset(filepath):
	"""
	Function to read the NYC dataset and return
	a subset of it with requests lying in a
	particular day (flexible).

	Args:
		filepath: The path of the csv file

	Returns:
		A pandas dataframe containing information
		about rides of that particular time period.
	"""
	ny_dataset = pd.read_csv(filepath)
	ny_dataset['pickup_datetime'] = ny_dataset['pickup_datetime'].map(change_string_to_datetime)

	time_start = change_string_to_datetime('2014-01-08 09:00:00')
	time_end = change_string_to_datetime('2014-01-08 09:05:00')
	start_condition = ny_dataset['pickup_datetime'] > time_start
	end_condition = ny_dataset['pickup_datetime'] < time_end

	subset = ny_dataset[start_condition & end_condition]
	return subset


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

	return requests


def create_adjacency_matrix(requests, delta_1, delta_2, filename):
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
		filename: The file to which adjacency matrix
		will be written.

	It is to be noted that in adjacency matrix, 0 means
	not admissible and 1 means admissible.
	"""
	admissibility_string = ""
	data = create_osrm_table(requests)
	for i,first_request in enumerate(requests):
		for j,second_request in enumerate(requests):
			admissibility = check_admissibility(first_request, second_request, delta_1, delta_2, data, len(requests))
			if admissibility == True and j != len(requests)-1:
				admissibility_string = admissibility_string + "1 "
			elif admissibility == True:
				admissibility_string = admissibility_string + "1"
			elif admissibility == False and j != len(requests)-1:
				admissibility_string = admissibility_string + "0 "
			else:
				admissibility_string = admissibility_string + "0"

		if i != len(requests)-1:
			admissibility_string = admissibility_string + "\n"

	file = open(filename, "w+")
	file.writelines(admissibility_string)
	file.close()


def create_distance_matrix(requests):
	"""
	Function to create distance matrix depicting
	distances between all pairs of requests.
	
	Args:
		requests: All the request objects
		distance_file_name: Name of file to which distance matrix is written
	
	Returns:
		A list containing distance of each request from its destination.
	"""

	distances = []
	for request in requests:
		result = osrm.simple_route([request.source_lat, request.source_long], [request.dest_lat, request.dest_long],output='route', overview="full", geometry='wkt')
		distances.append(result['distance'])

	return distances

if __name__ == '__main__':
	read_dataset('nyc_taxi_data_2014.csv')