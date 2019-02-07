import pickle_utility as pkl
import sys
sys.path.insert(0, 'D:/College/VPool/')
from graph import parse_nyc_data as nyc
import pandas as pd


def csv_to_data(csv_file_name):
	"""
	Utility function to read content present in csv
	file written in NYC data format and put into 
	corresponding files.

	Args:
		csv_file_name: Path of csv file containing
		data

	Returns:
		Adjacency matrix and distance matrix.
	"""
	data = nyc.read_dataset('nyc_taxi_data_2014.csv')
	requests = nyc.create_request_objects(data)
	adjacency_matrix = nyc.create_adjacency_matrix(requests, 600, 600)

	return adjacency_matrix, nyc.create_distance_matrix(requests)


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


if __name__ == '__main__':
	pass