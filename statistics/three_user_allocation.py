from __future__ import division
from vehicle_statistics import two_user_route_statistics


def three_user_route_statistics(i, j, k, source_data, destination_data, source_destination_data, delta=1.2):
	"""
	Function that enumerates the possible cases for
	a 3-seater vehicle and returns the one with least
	possible distance travelled such that all users still
	satisfy admissibility criteria.

	Args:
		i: The first user

		j: The second user

		k: The third user

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
	minimum_distance_so_far = 10**15
	common_travel_distance = 0.0

	try:
		if source_data[i][j] + source_data[j][k] + source_destination_data[k][i] <= 1.2*source_destination_data[i][i] and source_data[j][k] + source_destination_data[k][i] + destination_data[i][j] <= 1.2*source_destination_data[j][j] and source_destination_data[k][i] + destination_data[i][j] + destination_data[j][k] <= 1.2*source_destination_data[k][k]:

			total_distance = source_data[i][j] + source_data[j][k] + source_destination_data[k][i] + destination_data[i][j] + destination_data[j][k]

			user_distance = source_data[i][j] + source_data[j][k] + source_destination_data[k][i] 
			+ source_data[j][k] + source_destination_data[k][i] + destination_data[i][j]
			+ source_destination_data[k][i] + destination_data[i][j] + destination_data[j][k]

			common_travel_distance = source_destination_data[k][i]
			occupancy_ratio = user_distance/(3*total_distance)
			minimum_distance_so_far = total_distance

		if source_data[i][j] + source_data[j][k] + source_destination_data[k][i] <= 1.2*source_destination_data[i][i] and source_data[j][k] + source_destination_data[k][i] + destination_data[i][k] + destination_data[k][j] <= 1.2*source_destination_data[j][j] and source_destination_data[k][i] + destination_data[i][k] <= 1.2*source_destination_data[k][k]:

			total_distance = source_data[i][j] + source_data[j][k] + source_destination_data[k][i] + destination_data[i][k] + destination_data[k][j]

			user_distance = source_data[i][j] + source_data[j][k] + source_destination_data[k][i] 
			+ source_data[j][k] + source_destination_data[k][i] + destination_data[i][k] + destination_data[k][j]
			+ source_destination_data[k][i] + destination_data[i][k]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[k][i]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance

		
		if source_data[i][j] + source_data[j][k] + source_destination_data[k][j] + destination_data[j][i] <= 1.2*source_destination_data[i][i] and source_data[j][k] + source_destination_data[k][j] <= 1.2*source_destination_data[j][j] and source_destination_data[k][j] + destination_data[j][i] + destination_data[i][k] <= 1.2*source_destination_data[k][k]:

			total_distance = source_data[i][j] + source_data[j][k] + source_destination_data[k][j] + destination_data[j][i] + destination_data[i][k]

			user_distance = source_data[i][j] + source_data[j][k] + source_destination_data[k][j] + destination_data[j][i] 
			+ source_data[j][k] + source_destination_data[k][j]
			+ source_destination_data[k][j] + destination_data[j][i] + destination_data[i][k]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[k][j]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance


		if source_data[i][j] + source_data[j][k] + source_destination_data[k][j] + destination_data[j][k] + destination_data[k][i] <= 1.2*source_destination_data[i][i] and source_data[j][k] + source_destination_data[k][j] <= 1.2*source_destination_data[j][j] and source_destination_data[k][j] + destination_data[j][k] <= 1.2*source_destination_data[k][k]:

			total_distance = source_data[i][j] + source_data[j][k] + source_destination_data[k][j] + destination_data[j][k] + destination_data[k][i]

			user_distance = source_data[i][j] + source_data[j][k] + source_destination_data[k][j] + destination_data[j][k] + destination_data[k][i]
			+ source_data[j][k] + source_destination_data[k][j]
			+ source_destination_data[k][j] + destination_data[j][k]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[k][j]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance


		if source_data[i][j] + source_data[j][k] + source_destination_data[k][k] + destination_data[k][i] <= 1.2*source_destination_data[i][i] and source_data[j][k] + source_destination_data[k][k] + destination_data[k][i] + destination_data[i][j] <= 1.2*source_destination_data[j][j]:

			total_distance = source_data[i][j] + source_data[j][k] + source_destination_data[k][k] + destination_data[k][i] + destination_data[i][j]

			user_distance = source_data[i][j] + source_data[j][k] + source_destination_data[k][k] + destination_data[k][i]
			+ source_data[j][k] + source_destination_data[k][k] + destination_data[k][i] + destination_data[i][j]
			+ source_destination_data[k][k]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[k][k]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance


		if source_data[i][j] + source_data[j][k] + source_destination_data[k][k] + destination_data[k][j] + destination_data[j][i] <= 1.2*source_destination_data[i][i] and source_data[j][k] + source_destination_data[k][k] + destination_data[k][j] <= 1.2*source_destination_data[j][j]:

			total_distance = source_data[i][j] + source_data[j][k] + source_destination_data[k][k] + destination_data[k][j] + destination_data[j][i]

			user_distance = source_data[i][j] + source_data[j][k] + source_destination_data[k][k] + destination_data[k][j] + destination_data[j][i]
			+ source_data[j][k] + source_destination_data[k][k] + destination_data[k][j]
			+ source_destination_data[k][k]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[k][k]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance


		# S3 S2 S1 D1 D2 D3
		if source_data[k][j] + source_data[j][i] + source_destination_data[i][i] + destination_data[i][j] + destination_data[j][k] <= 1.2*source_destination_data[k][k] and  source_data[j][i] + source_destination_data[i][i] + destination_data[i][j] <= 1.2*source_destination_data[j][j] and source_destination_data[i][i] <= 1.2*source_destination_data[i][i]:

			total_distance = source_data[k][j] + source_data[j][i] + source_destination_data[i][i] + destination_data[i][j] + destination_data[j][k]

			user_distance = source_data[k][j] + source_data[j][i] + source_destination_data[i][i] + destination_data[i][j] + destination_data[j][k] + source_data[j][i] + source_destination_data[i][i] + destination_data[i][j] + source_destination_data[i][i]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[i][i]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S3 S2 S1 D1 D3 D2

		if source_data[k][j] + source_data[j][i] + source_destination_data[i][i] + destination_data[i][k] <= 1.2*source_destination_data[k][k]  and source_data[j][i] + source_destination_data[i][i] + destination_data[i][k] + destination_data[k][j] <= 1.2*source_destination_data[j][j] and source_destination_data[i][i] <= 1.2*source_destination_data[i][i]:
			total_distance = source_data[k][j] + source_data[j][i] + source_destination_data[i][i] + destination_data[i][k] + destination_data[k][j]

			user_distance = source_data[k][j] + source_data[j][i] + source_destination_data[i][i] + destination_data[i][k] + source_data[j][i] + source_destination_data[i][i] + destination_data[i][k] + destination_data[k][j] + source_destination_data[i][i]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[i][i]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S3 S2 S1 D2 D1 D3

		if source_data[k][j] + source_data[j][i] + source_destination_data[i][j] + destination_data[j][i] + destination_data[i][k] <= 1.2*source_destination_data[k][k] and source_data[j][i] + source_destination_data[i][j] <= 1.2*source_destination_data[j][j] and source_destination_data[i][j] + destination_data[j][i] <= 1.2*source_destination_data[i][i]:

			total_distance = source_data[k][j] + source_data[j][i] + source_destination_data[i][j] + destination_data[j][i] + destination_data[i][k]

			user_distance = source_data[k][j] + source_data[j][i] + source_destination_data[i][j] + destination_data[j][i] + destination_data[i][k] + source_data[j][i] + source_destination_data[i][j] + source_destination_data[i][j] + destination_data[j][i]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[i][j]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S3 S2 S1 D2 D3 D1

		if source_data[k][j] + source_data[j][i] + source_destination_data[i][j] + destination_data[j][k] <= 1.2*source_destination_data[k][k] and source_data[j][i] + source_destination_data[i][j] <= 1.2*source_destination_data[j][j] and source_destination_data[i][j] + destination_data[j][k] + destination_data[k][i] <= 1.2*source_destination_data[i][i]:
			
			total_distance = source_data[k][j] + source_data[j][i] + source_destination_data[i][j] + destination_data[j][k] + destination_data[k][i]

			user_distance = source_data[k][j] + source_data[j][i] + source_destination_data[i][j] + destination_data[j][k] + source_data[j][i] + source_destination_data[i][j] + source_destination_data[i][j] + destination_data[j][k] + destination_data[k][i]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[i][j]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S3 S2 S1 D3 D1 D2

		if source_data[k][j] + source_data[j][i] + source_destination_data[i][k] <= 1.2*source_destination_data[k][k] and source_data[j][i] + source_destination_data[i][k] + destination_data[k][i] + destination_data[i][j] <= 1.2*source_destination_data[j][j] and source_destination_data[i][k] + destination_data[k][i] <= 1.2*source_destination_data[i][i]:

			total_distance = source_data[k][j] + source_data[j][i] + source_destination_data[i][k] + destination_data[k][i] + destination_data[i][j]

			user_distance = source_data[k][j] + source_data[j][i] + source_destination_data[i][k] + source_data[j][i] + source_destination_data[i][k] + destination_data[k][i] + destination_data[i][j] + source_destination_data[i][k] + destination_data[k][i]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[i][k]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S3 S2 S1 D3 D2 D1 

		if source_data[k][j] + source_data[j][i] + source_destination_data[i][k] <= 1.2*source_destination_data[k][k] and source_data[j][i] + source_destination_data[i][k] + destination_data[k][j] <= 1.2*source_destination_data[j][j] and source_destination_data[i][k] + destination_data[k][j] + destination_data[j][i] <= 1.2*source_destination_data[i][i]:
			
			total_distance = source_data[k][j] + source_data[j][i] + source_destination_data[i][k] + destination_data[k][j] + destination_data[j][i]

			user_distance = source_data[k][j] + source_data[j][i] + source_destination_data[i][k] + source_data[j][i] + source_destination_data[i][k] + destination_data[k][j] + source_destination_data[i][k] + destination_data[k][j] + destination_data[j][i]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[i][k]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S3 S1 S2 D1 D2 D3

		if source_data[k][i] + source_data[i][j] + source_destination_data[j][i] + destination_data[i][j] + destination_data[j][k] <= 1.2*source_destination_data[k][k] and source_data[i][j] + source_destination_data[j][i] <= 1.2*source_destination_data[i][i] and source_destination_data[j][i] + destination_data[i][j] <= 1.2*source_destination_data[j][j]:

			total_distance = source_data[k][i] + source_data[i][j] + source_destination_data[j][i] + destination_data[i][j] + destination_data[j][k]

			user_distance = source_data[k][i] + source_data[i][j] + source_destination_data[j][i] + destination_data[i][j] + destination_data[j][k] + source_data[i][j] + source_destination_data[j][i] + source_destination_data[j][i] + destination_data[i][j]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[j][i]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S3 S1 S2 D1 D3 D2

		if source_data[i][j] + source_destination_data[j][i] <= 1.2*source_destination_data[i][i] and source_data[k][i] + source_data[i][j] + source_destination_data[j][i] + destination_data[i][k] <= 1.2*source_destination_data[k][k] and source_destination_data[j][i] + destination_data[i][k] + destination_data[k][j] <= 1.2*source_destination_data[j][j]:

			total_distance = source_data[k][i] + source_data[i][j] + source_destination_data[j][i] + destination_data[i][k] + destination_data[k][j]

			user_distance = source_data[i][j] + source_destination_data[j][i] + source_data[k][i] + source_data[i][j] + source_destination_data[j][i] + destination_data[i][k] + source_destination_data[j][i] + destination_data[i][k] + destination_data[k][j]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[j][i]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S3 S1 S2 D2 D1 D3

		if source_data[k][i] + source_data[i][j] + source_destination_data[j][j] + destination_data[j][i] + destination_data[i][k] <= 1.2*source_destination_data[k][k] and source_data[i][j] + source_destination_data[j][j] + destination_data[j][i] <= 1.2* source_destination_data[i][i] and source_destination_data[j][j] <= 1.2*source_destination_data[j][j]:

			total_distance = source_data[k][i] + source_data[i][j] + source_destination_data[j][j] + destination_data[j][i] + destination_data[i][k]

			user_distance = source_data[k][i] + source_data[i][j] + source_destination_data[j][j] + destination_data[j][i] + destination_data[i][k] + source_data[i][j] + source_destination_data[j][j] + destination_data[j][i] + source_destination_data[j][j]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[j][j]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S3 S1 S2 D2 D3 D1

		if source_data[k][i] + source_data[i][j] + source_destination_data[j][j] + destination_data[j][k] <= 1.2*source_destination_data[k][k] and source_data[i][j] + source_destination_data[i][j] + destination_data[j][k] + destination_data[k][i] <= 1.2*source_destination_data[i][i] and source_destination_data[j][j] <= 1.2*source_destination_data[j][j]:

			total_distance = source_data[k][i] + source_data[i][j] +source_destination_data[j][j] + destination_data[j][k] + destination_data[k][i]

			user_distance = source_data[k][i] + source_data[i][j] + source_destination_data[j][j] + destination_data[j][k] + source_data[i][j] + source_destination_data[i][j] + destination_data[j][k] + destination_data[k][i] + source_destination_data[j][j]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[j][j]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S3 S1 S2 D3 D1 D2

		if source_data[k][i] + source_data[i][j] + source_destination_data[j][k] <= 1.2*source_destination_data[k][k] and source_data[i][j] + source_destination_data[j][k] +destination_data[k][i] <= 1.2*source_destination_data[i][i] and source_destination_data[j][k] + destination_data[k][i] + destination_data[i][j] <= 1.2*source_destination_data[j][j]:

			total_distance = source_data[k][i] + source_data[i][j] + source_destination_data[j][k] + destination_data[k][i] + destination_data[i][j]

			user_distance = source_data[k][i] + source_data[i][j] + source_destination_data[j][k] + source_data[i][j] + source_destination_data[j][k] +destination_data[k][i] + source_destination_data[j][k] + destination_data[k][i] + destination_data[i][j]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[j][k]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S3 S1 S2 D3 D2 D1

		if source_data[k][i] + source_data[i][j] + source_destination_data[j][k] <= 1.2*source_destination_data[k][k] and source_data[i][j] + source_destination_data[j][k] + destination_data[k][j] +destination_data[j][i] <= 1.2*source_destination_data[i][i] and source_destination_data[j][k] + destination_data[k][j] <= 1.2*source_destination_data[j][j]:

			total_distance = source_data[k][i] + source_data[i][j] + source_destination_data[j][k] + destination_data[k][j] + destination_data[j][i]

			user_distance = source_data[k][i] + source_data[i][j] + source_destination_data[j][k] + source_data[i][j] + source_destination_data[j][k] + destination_data[k][j] +destination_data[j][i] + source_destination_data[j][k] + destination_data[k][j]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[j][k]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S2 S1 S3 D1 D2 D3

		if source_data[j][i] + source_data[i][k] + source_destination_data[k][i] + destination_data[i][j] <= 1.2*source_destination_data[j][j] and source_data[i][k] + source_destination_data[k][i] <= 1.2*source_destination_data[i][i] and source_destination_data[k][i] + destination_data[i][j] + destination_data[j][k] <= 1.2*source_destination_data[k][k]:

			total_distance = source_data[j][i] + source_data[i][k] + source_destination_data[k][i] + destination_data[i][j] + destination_data[j][k]

			user_distance = source_data[j][i] + source_data[i][k] + source_destination_data[k][i] + destination_data[i][j] + source_data[i][k] + source_destination_data[k][i] + source_destination_data[k][i] + destination_data[i][j] + destination_data[j][k]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[k][i]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S2 S1 S3 D1 D3 D2

		if source_data[j][i] + source_data[i][k] + source_destination_data[k][i] + destination_data[i][k] + destination_data[k][j] <= 1.2*source_destination_data[j][j] and source_data[i][k] + source_destination_data[k][i] <= 1.2*source_destination_data[i][i] and source_destination_data[k][i] + destination_data[i][k] <= 1.2*source_destination_data[k][k]:

			total_distance = source_data[j][i] + source_data[i][k] + source_destination_data[k][i] + destination_data[i][k] + destination_data[k][j]

			user_distance = source_data[j][i] + source_data[i][k] + source_destination_data[k][i] + destination_data[i][k] + destination_data[k][j] + source_data[i][k] + source_destination_data[k][i] + source_destination_data[k][i] + destination_data[i][k]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[k][i]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S2 S1 S3 D2 D1 D3

		if source_data[j][i] + source_data[i][k] + source_destination_data[k][j] <= 1.2*source_destination_data[j][j] and source_data[i][k] + source_destination_data[k][j] + destination_data[j][i] <= 1.2*source_destination_data[i][i] and source_destination_data[k][j] + destination_data[j][i] + destination_data[i][k] <= 1.2*source_destination_data[k][k]:

			total_distance = source_data[j][i] + source_data[i][k] + source_destination_data[k][j] + destination_data[j][i] + destination_data[i][k]

			user_distance = source_data[j][i] + source_data[i][k] + source_destination_data[k][j] + source_data[i][k] + source_destination_data[k][j] + destination_data[j][i] + source_destination_data[k][j] + destination_data[j][i] + destination_data[i][k]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[k][j]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S2 S1 S3 D2 D3 D1

		if source_data[j][i] + source_data[i][k] + source_destination_data[k][j] <= 1.2*source_destination_data[j][j] and source_data[i][k] + source_destination_data[k][j] + destination_data[j][k] + destination_data[k][i] <= 1.2*source_destination_data[i][i] and source_destination_data[k][j] + destination_data[j][k] <= 1.2*source_destination_data[k][k]:

			total_distance = source_data[j][i] + source_data[i][k] + source_destination_data[k][j] + destination_data[j][k] + destination_data[k][i]

			user_distance = source_data[j][i] + source_data[i][k] + source_destination_data[k][j] + source_data[i][k] + source_destination_data[k][j] + destination_data[j][k] + destination_data[k][i] + source_destination_data[k][j] + destination_data[j][k]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[k][j]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S2 S1 S3 D3 D1 D2

		if source_data[j][i] + source_data[i][k] + source_destination_data[k][k] + destination_data[k][i] + destination_data[i][j] <= 1.2*source_destination_data[j][j] and source_data[i][k] + source_destination_data[k][k] + destination_data[k][i] <= 1.2*source_destination_data[i][i] and source_destination_data[k][k] <= 1.2*source_destination_data[k][k]:

			total_distance = source_data[j][i] + source_data[i][k] + source_destination_data[k][k] + destination_data[k][i] + destination_data[i][j]

			user_distance = source_data[j][i] + source_data[i][k] + source_destination_data[k][k] + destination_data[k][i] + destination_data[i][j] + source_data[i][k] + source_destination_data[k][k] + destination_data[k][i] + source_destination_data[k][k]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[k][k]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S2 S1 S3 D3 D2 D1

		if source_data[j][i] + source_data[i][k] + source_destination_data[k][k] + destination_data[k][j] <= 1.2*source_destination_data[j][j] and source_data[i][k] + source_destination_data[k][k] + destination_data[k][j] + destination_data[j][i] <= 1.2*source_destination_data[i][i] and source_destination_data[k][k] <= 1.2*source_destination_data[k][k]:

			total_distance = source_data[j][i] + source_data[i][k] + source_destination_data[k][k] + destination_data[k][j] + destination_data[j][i]

			user_distance = source_data[j][i] + source_data[i][k] + source_destination_data[k][k] + destination_data[k][j] + source_data[i][k] + source_destination_data[k][k] + destination_data[k][j] + destination_data[j][i] + source_destination_data[k][k]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[k][k]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance
				


		# S2 S3 S1 D1 D2 D3

		if source_data[j][k] + source_data[k][i] + source_destination_data[i][i] + destination_data[i][j] <= 1.2*source_destination_data[j][j] and source_data[k][i] + source_destination_data[i][i] + destination_data[i][j] + destination_data[j][k] <= 1.2*source_destination_data[k][k] and source_destination_data[i][i] <= 1.2*source_destination_data[i][i]:

			total_distance = source_data[j][k] + source_data[k][i] + source_destination_data[i][i] + destination_data[i][j] + destination_data[j][k]

			user_distance = source_data[j][k] + source_data[k][i] + source_destination_data[i][i] + destination_data[i][j] + source_data[k][i] + source_destination_data[i][i] + destination_data[i][j] + destination_data[j][k] + source_destination_data[i][i]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[i][i]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S2 S3 S1 D1 D3 D2

		if source_data[j][k] + source_data[k][i] + source_destination_data[i][i] + destination_data[i][k] + destination_data[k][j] <= 1.2*source_destination_data[j][j] and source_data[k][i] + source_destination_data[i][i] + destination_data[i][k] <= 1.2*source_destination_data[k][k] and source_destination_data[i][i] <= 1.2*source_destination_data[i][i]:
			
			total_distance = source_data[j][k] + source_data[k][i] + source_destination_data[i][i] + destination_data[i][k] + destination_data[k][j]

			user_distance = source_data[j][k] + source_data[k][i] + source_destination_data[i][i] + destination_data[i][k] + destination_data[k][j] + source_data[k][i] + source_destination_data[i][i] + destination_data[i][k] + source_destination_data[i][i]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[i][i]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S2 S3 S1 D2 D1 D3

		if source_data[j][k] + source_data[k][i] + source_destination_data[i][j] <= 1.2*source_destination_data[j][j] and source_data[k][i] + source_destination_data[i][j] + destination_data[j][i] + destination_data[i][k] <= 1.2*source_destination_data[k][k] and source_destination_data[i][j] + destination_data[j][i] <= 1.2*source_destination_data[i][i]:

			total_distance = source_data[j][k] + source_data[k][i] + source_destination_data[i][j] + destination_data[j][i] + destination_data[i][k]

			user_distance = source_data[j][k] + source_data[k][i] + source_destination_data[i][j] + source_data[k][i] + source_destination_data[i][j] + destination_data[j][i] + destination_data[i][k] + source_destination_data[i][j] + destination_data[j][i]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[i][j]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S2 S3 S1 D2 D3 D1

		if source_data[j][k] + source_data[k][i] + source_destination_data[i][j] <= 1.2*source_destination_data[j][j] and source_data[k][i] + source_destination_data[i][j] + destination_data[j][k] <= 1.2*source_destination_data[k][k] and source_destination_data[i][j] + destination_data[j][k] + destination_data[k][i] <= 1.2*source_destination_data[i][i]:

			total_distance = source_data[j][k] + source_data[k][i] + source_destination_data[i][j] + destination_data[j][k] + destination_data[k][i]

			user_distance = source_data[j][k] + source_data[k][i] + source_destination_data[i][j] + source_data[k][i] + source_destination_data[i][j] + destination_data[j][k] + source_destination_data[i][j] + destination_data[j][k] + destination_data[k][i]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[i][j]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S2 S3 S1 D3 D1 D2

		if source_data[j][k] + source_data[k][i] + source_destination_data[i][k] + destination_data[k][i] + destination_data[i][j] <= 1.2*source_destination_data[j][j] and source_data[k][i] + source_destination_data[i][k] <= 1.2*source_destination_data[k][k] and source_data[i][k] + destination_data[k][i] <= 1.2*source_destination_data[i][i]:

			total_distance = source_data[j][k] + source_data[k][i] + source_destination_data[i][k] + destination_data[k][i] + destination_data[i][j]

			user_distance = source_data[j][k] + source_data[k][i] + source_destination_data[i][k] + destination_data[k][i] + destination_data[i][j] + source_data[k][i] + source_destination_data[i][k] + source_data[i][k] + destination_data[k][i]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[i][k]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S2 S3 S1 D3 D2 D1

		if source_data[j][k] + source_data[k][i] + source_destination_data[i][k] + destination_data[k][j] <= 1.2*source_destination_data[j][j] and source_data[k][i] + source_destination_data[i][k] <= 1.2*source_destination_data[k][k] and source_destination_data[i][k] + destination_data[k][j] + destination_data[j][i] <= 1.2*source_destination_data[i][i]:

			total_distance = source_data[j][k] + source_data[k][i] + source_destination_data[i][k] + destination_data[k][j] + destination_data[j][i]

			user_distance = source_data[j][k] + source_data[k][i] + source_destination_data[i][k] + destination_data[k][j] + source_data[k][i] + source_destination_data[i][k] + source_destination_data[i][k] + destination_data[k][j] + destination_data[j][i]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[i][k]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S1 S3 S2 D1 D2 D3

		if source_data[i][k] + source_data[k][j] + source_destination_data[j][i] <= 1.2*source_destination_data[i][i] and source_data[k][j] + source_destination_data[j][i] + destination_data[i][j] + destination_data[j][k] <= 1.2*source_destination_data[k][k] and source_destination_data[j][i] + destination_data[i][j] <= 1.2*source_destination_data[j][j]:

			total_distance = source_data[i][k] + source_data[k][j] + source_destination_data[j][i] + destination_data[i][j] + destination_data[j][k]

			user_distance = source_data[i][k] + source_data[k][j] + source_destination_data[j][i] + source_data[k][j] + source_destination_data[j][i] + destination_data[i][j] + destination_data[j][k] + source_destination_data[j][i] + destination_data[i][j]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[j][i]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S1 S3 S2 D1 D3 D2

		if source_data[i][k] + source_data[k][j] + source_destination_data[j][i] <= 1.2*source_destination_data[i][i] and source_data[k][j] + source_destination_data[j][i] + destination_data[i][k] <= 1.2*source_destination_data[k][k] and source_destination_data[j][i] + destination_data[i][k] + destination_data[k][j] <= 1.2*source_destination_data[j][j]:

			total_distance = source_data[i][k] + source_data[k][j] + source_destination_data[j][i] + destination_data[i][k] + destination_data[k][j]

			user_distance = source_data[i][k] + source_data[k][j] + source_destination_data[j][i] + source_data[k][j] + source_destination_data[j][i] + destination_data[i][k] + source_destination_data[j][i] + destination_data[i][k] + destination_data[k][j]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[j][i]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S1 S3 S2 D2 D1 D3

		if source_data[i][k] + source_data[k][j] + source_destination_data[j][j] + destination_data[j][i] <= 1.2*source_destination_data[i][i] and source_data[k][j] + source_destination_data[j][j] + destination_data[j][i] + destination_data[i][k] <= 1.2*source_destination_data[k][k] and source_destination_data[j][j] <= 1.2*source_destination_data[j][j]:

			total_distance = source_data[i][k] + source_data[k][j] + source_destination_data[j][j] + destination_data[j][i] + destination_data[i][k]

			user_distance = source_data[i][k] + source_data[k][j] + source_destination_data[j][j] + destination_data[j][i] + source_data[k][j] + source_destination_data[j][j] + destination_data[j][i] + destination_data[i][k] + source_destination_data[j][j]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[j][j]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance	



		# S1 S3 S2 D2 D3 D1

		if source_data[i][k] + source_data[k][j] + source_destination_data[j][j] + destination_data[j][k] + destination_data[k][i] <= 1.2*source_destination_data[i][i] and source_data[k][j] + source_destination_data[j][j] + destination_data[j][k] <= 1.2*source_destination_data[k][k] and source_destination_data[j][j] <= 1.2*source_destination_data[j][j]:

			total_distance = source_data[i][k] + source_data[k][j] + source_destination_data[j][j] + destination_data[j][k] + destination_data[k][i]

			user_distance = source_data[i][k] + source_data[k][j] + source_destination_data[j][j] + destination_data[j][k] + destination_data[k][i] + source_data[k][j] + source_destination_data[j][j] + destination_data[j][k] + source_destination_data[j][j]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[j][j]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S1 S3 S2 D3 D1 D2

		if source_data[i][k] + source_data[k][j] + source_destination_data[j][k] + destination_data[k][i] <= 1.2*source_destination_data[i][i] and source_data[k][j] + source_destination_data[j][k] <= 1.2*source_destination_data[k][k] and source_destination_data[j][k] + destination_data[k][i] + destination_data[i][j] <= 1.2*source_destination_data[j][j]:

			total_distance = source_data[i][k] + source_data[k][j] + source_destination_data[j][k] + destination_data[k][i] + destination_data[i][j]

			user_distance = source_data[i][k] + source_data[k][j] + source_destination_data[j][k] + destination_data[k][i] + source_data[k][j] + source_destination_data[j][k] + source_destination_data[j][k] + destination_data[k][i] + destination_data[i][j]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[j][k]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance



		# S1 S3 S2 D3 D2 D1

		if source_data[i][k] + source_data[k][j] + source_destination_data[j][k] + destination_data[k][j] + destination_data[j][i] <= 1.2*source_destination_data[i][i] and source_data[k][j] + source_destination_data[j][k] <= 1.2*source_destination_data[k][k] and source_destination_data[j][k] + destination_data[k][j] <= 1.2*source_destination_data[j][j]:

			total_distance = source_data[i][k] + source_data[k][j] + source_destination_data[j][k] + destination_data[k][j] + destination_data[j][i]

			user_distance = source_data[i][k] + source_data[k][j] + source_destination_data[j][k] + destination_data[k][j] + destination_data[j][i] + source_data[k][j] + source_destination_data[j][k] + source_destination_data[j][k] + destination_data[k][j]

			if total_distance < minimum_distance_so_far:
				common_travel_distance = source_destination_data[j][k]
				occupancy_ratio = user_distance/(3*total_distance)
				minimum_distance_so_far = total_distance


		if occupancy_ratio == 0.0:
			occupancy_ratio, common_travel_distance, minimum_distance_so_far = two_user_route_statistics(i,j, source_data, source_destination_data, destination_data)

	except Exception as e:
		occupancy_ratio = 1.0
		minimum_distance_so_far = 0.0
		common_travel_distance = 0.0

	return occupancy_ratio, common_travel_distance, minimum_distance_so_far


if __name__ == '__main__':
	pass