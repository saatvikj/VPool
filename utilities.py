import numpy
import pandas
import networkx
import read_pickle_file as rdfl
import parse_nyc_data as nyc


def unpickle_to_file(pickle_file_name, adjacency_file_name, distance_file_name):
	"""
	Utility function to read data if it is present in a pickle
	file and write content into the corresponding files.

	Args:
		pickle_file_name: Pickle file to be read
		adjacency_file_name: File where admissibility
		matrix will be written
		distance_file_name: File where distance
		matrix will be written.
	
	Returns:
		void
	"""
	data_dictionary = rdfl.read_file(pickle_file_name)
	numpy_adjacency_matrix = data_dictionary['admissibility_matrix']
	distance_matrix = data_dictionary['distance_matrix']

	file = open(distance_file_name, "w+")
	for i,source in enumerate(distance_matrix):
		for j,destination in enumerate(source):
			if j != len(distance_matrix) -1:
				file.write("%d " % destination)
		if i != len(distance_matrix) - 1:
			file.write("\n")
	file.close()

	file = open(adjacency_file_name, "w+")
	for i in range(numpy_adjacency_matrix.shape[0]):
		for j in range(numpy_adjacency_matrix.shape[1]):
			if j != numpy_adjacency_matrix.shape[1]-1:
				file.write("%d " % numpy_adjacency_matrix.loc[i,j])
		if i != numpy_adjacency_matrix.shape[0] - 1:
			file.write("\n")
	file.close()		


def csv_to_file(csv_file_name, adjacency_file_name):
	"""
	Utility function to read content present in csv
	file written in NYC data format and put into 
	corresponding files.

	Args:
		csv_file_name: Path of csv file containing
		data
		adjacency_file_name: Name of file to which 
		adjacency matrix will be written.

	Returns:
		Void
	"""
	data = nyc.read_dataset('nyc_taxi_data_2014.csv')
	requests = nyc.create_request_objects(data)
	nyc.create_adjacency_matrix(requests, 5, 5, adjacency_file_name)

	return nyc.create_distance_matrix(requests)

if __name__ == '__main__':
	unpickle_to_file("saatvik_data_len_129_152540.pkl","hi","distance_matrix.txt")