import pickle
import datetime
import numpy
import sys
import os
sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),os.pardir)))
import graph.parse_nyc_data as nyc


def read_file(filename):
	"""
	Function to read pickle file and give its data

	Args:
		filename: Name of pickle file

	Returns:
		Data dictionary that was stored in .pkl format.
	"""
	file = filename
	data = {}
	with (open(file, "rb")) as openfile:
		data = pickle.load(openfile)
	return data


def unpickle_data(pickle_file_name):
	"""
	Utility function to read data if it is present in a pickle
	file and write content into the corresponding files.

	Args:
		pickle_file_name: Pickle file to be read

	Returns:
		Adjacency matrix, distance matrix, distance
		between sources, distance between destinations
		distance between source destination pairs and list
		of request objects corresponding to each rider.
	"""
	data_dictionary = read_file(pickle_file_name)
	numpy_adjacency_matrix = data_dictionary['admissibility_matrix']
	distance_matrix = data_dictionary['distance_matrix']
	source_data = data_dictionary['source_data'] 
	destination_data = data_dictionary['destination_data']
	source_destination_data = data_dictionary['source_destination_data']
	requests = data_dictionary['requests']

	adjacency_matrix = []
	if (type(numpy_adjacency_matrix).__name__ != 'list'):
		adjacency_matrix = numpy_adjacency_matrix.values.tolist()
	else:
		adjacency_matrix = numpy_adjacency_matrix
	return adjacency_matrix, distance_matrix, source_data, destination_data, source_destination_data, requests


def pickle_data(adjacency_matrix, distance_matrix, source_data, destination_data, source_destination_data, requests, pickle_file_name):
	"""
	Utility function to take data and pickle the dictionary into 
	the given file.

	Args:
		adjacency_matrix: Adjacency matrix to be pickled

		distance_matrix: Distance matrix to be pickled

		source_data: Distance matrix of sources of riders

		destination_data: Distance matrix of destinations
		of riders

		source_destination_data: Distance matrix of sources
		and destinations of riders

		requests: A list of objects of the class
		Request corresponding to each rider in the
		system.
		
		pickle_file_name: Name of file for data to be 
		stored in.
	
	Returns:
		Void
	"""
	pickle_dictionary = {}
	pickle_dictionary['admissibility_matrix'] = adjacency_matrix
	pickle_dictionary['distance_matrix'] = distance_matrix
	pickle_dictionary['source_data'] = source_data
	pickle_dictionary['destination_data'] = destination_data
	pickle_dictionary['source_destination_data'] = source_destination_data
	pickle_dictionary['requests'] = requests

	pickle_file = open(pickle_file_name,'wb')
	pickle.dump(pickle_dictionary, pickle_file)
	pickle_file.close()


def get_details_from_name(name):
	"""
	A function you make when you fuck
	things up, takes name of pickle
	file and returns parameters from
	which the dataset was queried.

	Args:
		name: Name of pickle file.

	Returns:
		Size of request objects, query
		start time, query end time.
	
	Thank god I used a good naming system.
	"""
	name_details = name.split('_')
	date = int(name_details[3])
	start_time_hour = int(name_details[4][:2])
	start_time_minute = int(name_details[4][2:])
	query_length = int(name_details[5].split('.')[0])

	start_time = datetime.datetime(2014,1,date,start_time_hour, start_time_minute)
	end_time = start_time + datetime.timedelta(minutes=5)
	
	return query_length, start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S')


def pickle_to_new_delta_graph(pickle_file_name, delta):
	"""
	A function that takes data that was pickled
	and converts it into data for new tolerance
	levels.

	Args:
		pickle_file_name: Name of file for data
		to be stored in.

		delta: The new tolerance levels for 
		admissibility.

	Returns:
		Updated data corresponding to the file
	"""
	adjacency_matrix, distance_matrix, source_data, destination_data, source_destination_data, requests = unpickle_data(pickle_file_name)
	for i in len(requests):
		for j in len(requests):
			new_admissibility = nyc.check_admissibility(i, j, source_data, destination_data, source_destination_data, delta)
			adjacency_matrix[i][j] = new_admissibility

	return adjacency_matrix, distance_matrix, source_data, destination_data, source_destination_data, requests


def get_details_from_name(name):
	"""
	A function you make when you fuck
	things up, takes name of pickle
	file and returns parameters from
	which the dataset was queried.

	Args:
		name: Name of pickle file.
	
	Returns:
		Name for pickle file ize of 
		request objects, query
		start time, query end time.
	
	Thank god I used a good naming system.
	"""
	raw_name = name[name.index('new'):]	
	name_details = name.split('_')
	date = int(name_details[3])
	start_time_hour = int(name_details[4][:2])
	start_time_minute = int(name_details[4][2:])
	query_length = int(name_details[5].split('.')[0])

	start_time = datetime.datetime(2014,1,date,start_time_hour, start_time_minute)
	end_time = start_time + datetime.timedelta(minutes=5)
	
	return raw_name, query_length, start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
	pass