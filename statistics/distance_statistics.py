def get_distance_from_allocation(allocation, distances):
	"""
	Function to get total distance travelled
	from the given allocation of vehicles.

	Args:
		allocation: The vehicles allocated to 
		the riders.

		distances: Distance of each passenger from
		its destination.

	Returns:
		A list of tuples of the format:
		(Vehicle Index, Distance Travelled, Total Distance travelled).
	"""
	result = []
	for i,vehicle in enumerate(allocation):
		max_distance = 0
		total_individual_distance = 0
		for passenger in vehicle.passengers:
			total_individual_distance += int(distances[passenger])
			if distances[passenger] > max_distance:
				max_distance = distances[passenger]
		result.append((i,max_distance,total_individual_distance))

	return result


def users_stats_in_coloring(allocation, distances):
	"""
	Gives distance between the sources of
	two users in the allocated vehicle.

	Args:
		allocation: The passengers in the vehicle.
		
		distances: Distance matrix of sources of the
		riders.

	Returns:
		Average distance between sources of users
		in the allocation.
	"""
	total_distance = 0
	for i,user_1 in enumerate(allocation):
		for j,user_2 in enumerate(allocation):
			if j <= i:
				total_distance += distances[user_1][user_2]

	return total_distance


if __name__ == '__main__':
	pass