import pickle_utility as pkl
import sys
import os
sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),os.pardir)))
from graph import parse_nyc_data as nyc
import pandas as pd


def csv_to_data(csv_file_name, time_start, time_end, port, delta, size_limit):
	"""
	Utility function to read content present in csv
	file written in NYC data format and accordingly
	create data from it.

	Args:
		csv_file_name: Path of csv file containing
		data

		time_start: Start time to query the input
		dataset for data.

		time_end: End time to query the input dataset
		for data.

		port: The full link to localhost port on which
		osrm server is running.

		delta: The tolerance value used for admissibility.

		size_limit: The upper bound on number of objects
		that will be created from the riders, used only
		to categorize data on the basis of input size.

	Returns:
		Adjacency matrix, distance from destinations,
		distance between sources, distance between
		destinations, distance between source destination
		pairs and list of request objects.
	"""
	data = nyc.read_dataset(csv_file_name, time_start, time_end)
	requests = nyc.create_request_objects(data, size_limit)
	adjacency_matrix, source_data, destination_data, source_destination_data = nyc.create_adjacency_matrix(requests, port, delta)
	return adjacency_matrix, nyc.create_distance_matrix(source_destination_data), source_data, destination_data, source_destination_data, requests


def graph_to_csv(pickle_file_name, csv_name):
	"""
	Takes graph from pickle file and puts
	adjacency matrix to a csv file.

	Args:
		pickle_file_name: Name of pickle file

		csv_name: Name of output file.
	"""
	data_dictionary = pkl.read_file(pickle_file_name)
	df = pd.DataFrame(data_dictionary['admissibility_matrix'])
	df.to_csv(csv_name)



def csv_to_requests(csv_file_name, time_start, time_end):
	"""
	Function to read the dataset for all ride requests
	in the given timeframe so that it can be used to 
	create dynamic requests.

	Args:
		csv_file_name: Path of csv file containing
		data

		time_start: Start time to query the input
		dataset for data.

		time_end: End time to query the input dataset
		for data.

	Returns:
		A list of request objects containing data about
		the dynamic requests.
	"""
	data = nyc.read_dataset(csv_file_name, time_start, time_end)
	requests = nyc.create_request_objects(data, 2000)

	return requests

if __name__ == '__main__':
	pass