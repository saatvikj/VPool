from __future__ import division
import numpy as np


def user_vs_vehicle_comparison(allotment, rates, vehicle_rate):
	"""
	Function to check number of users paying more 
	than vehicle running cost for a vehicle.

	Args:
		allotment: The allotted riders of the vehicle

		rates: Rates being charged to all riders

		vehicle_rate: Cost of running the vehicle
	
	Returns:
		Number of users paying more than cost
		of running vehicle.
	"""
	number_of_users = 0
	for user in allotment:		
		if rates[user] >= vehicle_rate:
			number_of_users += 1

	return number_of_users


def two_user_route_statistics(i,j, source_data, destination_data, source_destination_data, delta=1.2):
	"""
	Function that enumerates the possible cases for
	a 2-rider vehicle and returns the one with least
	possible distance travelled such that all users still
	satisfy admissibility criteria.

	Args:
		i: The first user

		j: The second user
		
		source_data: Distance matrix of sources of riders

		destination_data: Distance matrix of destinations
		of riders

		source_destination_data: Distance matrix of sources
		and destinations of riders

		delta: The tolerance value used for admissibility

	Returns:
		3 values, the occupancy index, distance for which all 3 users
		were in vehicle and total distance travelled by vehicle.	
	"""
	occupancy_ratio = 0.0
	minimum_distance_so_far = 0.0
	common_travel_distance = 0.0

	try:
		if source_destination_data[j][i] + source_data[i][j] <= 1.2*source_destination_data[i][i] and source_destination_data[j][i] + destination_data[i][j] <= 1.2*source_destination_data[j][j]:
			first = ((source_destination_data[j][i] + source_data[i][j])/(source_destination_data[j][i] + source_data[i][j]+destination_data[i][j]))
			second = ((source_destination_data[j][i] + destination_data[i][j])/(source_destination_data[j][i] + source_data[i][j]+destination_data[i][j]))
			occupancy_ratio = (first+second)/2
			common_travel_distance = source_destination_data[j][i]
			minimum_distance_so_far = source_data[i][j] + source_destination_data[j][i] + destination_data[i][j]

		if source_destination_data[i][j] + destination_data[j][i] <= 1.2*source_destination_data[i][i] and source_destination_data[i][j] + source_data[j][i] <= 1.2*source_destination_data[j][j]:
			first = ((source_destination_data[i][j] + destination_data[j][i])/(source_destination_data[i][j] + destination_data[j][i]+source_data[j][i]))		
			second = ((source_destination_data[i][j] + source_data[j][i])/(source_destination_data[i][j] + destination_data[j][i]+source_data[j][i]))
			total_distance = source_data[j][i] + source_destination_data[i][j] + destination_data[j][i]

			if total_distance < minimum_distance_so_far:
				minimum_distance_so_far = total_distance
				common_travel_distance = source_destination_data[i][j]
				occupancy_ratio = (first+second)/2

		if source_data[i][j]+source_destination_data[j][j]+destination_data[j][i] <= 1.2*source_destination_data[i][i]:
			first = (1)
			second = (source_destination_data[j][j]/(source_data[i][j]+source_destination_data[j][j]+destination_data[j][i]))

			total_distance = source_data[i][j] + source_destination_data[j][j] + destination_data[j][i]

			if total_distance < minimum_distance_so_far:
				minimum_distance_so_far = total_distance
				common_travel_distance = source_destination_data[j][j]
				occupancy_ratio = (first+second)/2

		if source_data[j][i]+source_destination_data[i][i]+destination_data[i][j] <= 1.2*source_destination_data[j][j]:
			first = (source_destination_data[i][i]/(source_data[j][i]+source_destination_data[i][i]+destination_data[i][j]))
			second = (1)

			total_distance = source_data[j][i]+source_destination_data[i][i]+destination_data[i][j]

			if total_distance < minimum_distance_so_far:
				minimum_distance_so_far = total_distance
				common_travel_distance = source_destination_data[i][i]
				occupancy_ratio = (first+second)/2

	except Exception as e:
		occupancy_ratio = 1.0
		minimum_distance_so_far = 0.0
		common_travel_distance = 0.0


	return occupancy_ratio, common_travel_distance, minimum_distance_so_far


if __name__ == '__main__':
	pass