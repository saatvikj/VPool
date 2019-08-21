from __future__ import division
import copy
import sys
import os
sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),os.pardir)))
import optimization.infinite_vehicle_allocator as iva
import distance_statistics as dStats
import vehicle_statistics as vStats
import route_statistics as rStats


def create_vehicle_text_file(i, vehicle, route_statistics, requests, rates, cost_incurred, route, root):
	"""
	Function to store details about all vehicles in a
	text file in the given folder so that it can be
	accessed later if required.

	Args:
		i: The vehicle number

		vehicle: The vehicle object corresponding
		to the vehicle number.

		route_statsitics: List of statistics which
		summarize the route of the vehicle, include
		things like occupancy index, distance etc.

		requests: A list of objects of the class
		Request corresponding to each rider in the
		system. 

		rates: The rate that will be charged to all the 
		riders in the system so that vehicle profit can
		be calculated.

		cost_incurred: The rate that will be charged for
		running that particular vehicle so that vehicle
		profit can be calculated.

		route: The route for the given vehicle, the route
		is a list with index of passenger representing the
		next point to go to.

		root: The type of coloring algorithm used to get the
		graph coloring, needed for website.

	Returns:
		Void
	"""
	contents = []
	contents.append(str(vehicle.cap)+'\n')
	contents.append(str(len(vehicle.passengers))+'\n')
	contents.append(str(route_statistics[2])+'\n')

	profit = 0

	for j in vehicle.passengers:
		profit += rates[j]

	profit -= cost_incurred

	contents.append(str(profit/1000.0)+'\n')
	contents.append(str(route_statistics[0])+'\n')

	string = ","

	contents.append(string.join(str(v) for v in vehicle.passengers)+'\n')
	contents.append(route+'\n')

	for j in vehicle.passengers:
		rider_content = []
		rider_content.append(j)
		rider_content.append(requests[j].source_lat)
		rider_content.append(requests[j].source_long)
		rider_content.append(requests[j].dest_lat)
		rider_content.append(requests[j].dest_long)

		string = " "
		contents.append(string.join(str(v) for v in rider_content)+'\n')

	filename = os.getcwd()+"\\"+root+"\\"+str(i+1)+".txt"
	file = open(filename,"w+")
	file.writelines(contents)
	file.close()


def coloring_statistics(coloring, vehicles, distance_from_destination, source_data, destination_data, source_destination_data, rates, requests, text_output, root, start='40.730610,-73.935242\n'):
	"""
	Function to calculate statistics related to the coloring
	obtained, statistics range from vehicle to route
	statistics and statistics about operator profits.

	Args:
		coloring: The obtained color class from graph coloring.

		vehicles: The vehicles allocated to the given color
		class.

		distance_from_destination: Distance of each rider from
		their destination.

		source_data: Distance matrix of sources of riders

		destination_data: Distance matrix of destinations
		of riders

		source_destination_data: Distance matrix of sources
		and destinations of riders

		rates: The list of rates charged to each rider for
		being part of the system.

		requests: A list of objects of the class request
		corresponding to each rider in the system.

		text_output: The output text file used to communicate
		with jsprit java code.

		root: The type of coloring algorithm used to get the
		graph coloring, needed for website.

		start: A string representing the starting position of the
		vehicle. Center of new york by default.

	Returns:
		The statistics obtained of the given
		coloring.
	"""
	total_operator_cost = 0
	total_used_vehicles = 0
	in_source_distances = 0
	users_above_slab = 0
	average_ratio = 0.0
	combined_distance = 0.0
	vehicle_distance = 0.0
	single_user_vehicles = 0

	i = 0
	for color in coloring:
		cost, allotment = iva.allot_vehicles(coloring[color], vehicles)
		total_used_vehicles += len(allotment)
		distance_results = dStats.get_distance_from_allocation(allotment,distance_from_destination)

		for vehicle in allotment:
			cost_incurred = 0

			file_contents = []
			file_contents.append(str(len(vehicle.passengers))+'\n')
			file_contents.append(str(vehicle.cap)+'\n')

			occupants_string = ""
			for user in vehicle.passengers:
				occupants_string = occupants_string + str(user) +','
			occupants_string = occupants_string[:len(occupants_string)-1]

			file_contents.append(occupants_string+'\n')

			file_contents.append(start)

			for user in vehicle.passengers:
				if requests[user].source_lat != 0.0:
					file_contents.append(str(requests[user].source_lat)+','+str(requests[user].source_long)+'\n')
				else:
					file_contents.append(start)

			for user in vehicle.passengers:
				if requests[user].dest_lat != 0.0:
					file_contents.append(str(requests[user].dest_lat)+','+str(requests[user].dest_long)+'\n')			
				else:
					file_contents.append(start)			

			file = open(text_output,"w+")
			file.writelines(file_contents)
			file.close()

			query_string = 'java -jar vehicle_routing.jar ' + text_output
			route = os.popen(query_string).read()
 
			if len(vehicle.passengers) == 1:
				route_statistics = [1.0,source_destination_data[vehicle.passengers[0]][vehicle.passengers[0]],source_destination_data[vehicle.passengers[0]][vehicle.passengers[0]]]
			else:
				route_statistics = rStats.in_vehicle_user_stats(vehicle.passengers, route, source_data, destination_data, source_destination_data)

			average_ratio = average_ratio + route_statistics[0]
			combined_distance = combined_distance + route_statistics[1]
			vehicle_distance = vehicle_distance + route_statistics[2]

			if len(vehicle.passengers) == 1:
				rates[vehicle.passengers[0]] = route_statistics[2]*20
				single_user_vehicles += 1
			elif vehicle.cap > 4:
				for passenger in vehicle.passengers:
					rates[passenger] = (rates[passenger]/1.5)

			if vehicle.cap == 4:
				cost_incurred = (route_statistics[2]*15)
			elif vehicle.cap == 6:
				cost_incurred = (route_statistics[2]*25)
			else:
				cost_incurred = (route_statistics[2]*30)

			cost = cost + cost_incurred - vehicle.cost

			create_vehicle_text_file(i, vehicle, route_statistics, requests, rates, cost_incurred, route, root)

			i += 1
			
			in_source_distances += dStats.users_stats_in_coloring(vehicle.passengers, source_data)
			users_above_slab += vStats.user_vs_vehicle_comparison(vehicle.passengers, rates, cost_incurred)

		total_operator_cost += cost

	revenue = sum(rates)-total_operator_cost
	
	average_ratio = average_ratio/total_used_vehicles
	combined_distance = combined_distance/total_used_vehicles
	vehicle_distance = vehicle_distance/total_used_vehicles
	return [revenue/1000.0, in_source_distances/total_used_vehicles, users_above_slab, total_used_vehicles, average_ratio, combined_distance/vehicle_distance, single_user_vehicles, vehicle_distance]


	if __name__ == '__main__':
		pass