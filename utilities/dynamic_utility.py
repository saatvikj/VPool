from datetime import datetime
import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),os.pardir)))
import graph.parse_nyc_data as nyc


def convert_to_datetime(column):
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


def create_vehicle_rider_adjacency_matrix(source_distance, destination_distance, source_destination_distance, new_requests, active_riders, current_vehicles):
	"""


	"""
	riderwise_adjacency_matrix = []
	for i in range(len(new_requests)+len(active_riders)):
		data = []
		for j in range(len(new_requests)+len(active_riders)):

			if i >= len(new_requests):
				if j >= len(new_requests):
					if active_riders[i].vehicle_id == active_riders[j].vehicle_id:
						data.append(1)
					else:
						data.append(0)
				else:
					if nyc.check_admissibility(i,j,source_distance, destination_distance,source_destination_distance, j_travelled = active_riders[j-len(new_requests)].distance_travelled):
						data.append(1)
					else:
						data.append(0)
			else:
				if j >= len(new_requests):
					if nyc.check_admissibility(i,j,source_distance, destination_distance,source_destination_distance, i_travelled = active_riders[i-len(new_requests)].distance_travelled):
						data.append(1)
					else:
						data.append(0)
				else:
					if nyc.check_admissibility(i,j, source_distance, destination_distance, source_destination_distance):
						data.append(1)
					else:
						data.append(0)

		riderwise_adjacency_matrix.append(data)


	adjacency_matrix = []
	for i in range(len(new_requests)):
		data = []
		for j in range(len(new_requests)):
			data.append(riderwise_adjacency_matrix[i][j])

		passenger_iterator = 0
		for k in range(len(current_vehicles)):
			vehicle_admissibility = 1
			for l in range(len(current_vehicles[j],passengers)):
				vehicle_admissibility *= riderwise_adjacency_matrix[i][len(new_requests)+passenger_iterator]
				passenger_iterator += 1

			data.append(vehicle_admissibility)

		adjacency_matrix.append(data)


	return adjacency_matrix