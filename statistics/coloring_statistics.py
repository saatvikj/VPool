from __future__ import division
import copy
import sys
sys.path.insert(0, 'D:/College/VPool/')
import optimization.infinite_vehicle_allocator as iva
import distance_statistics as dStats
import vehicle_statistics as vStats


cost_slab = {
   4: [350, 450, 500, 525],
   6: [600, 700, 750, 850],
   12: [650, 800, 850, 1000],
   35: [2800, 2800, 2800, 3000],
   41: [3000, 3000, 3000, 3200],
}

def coloring_statistics(option, coloring, vehicles, distance_from_destination, source_data, destination_data, source_destination_data, rates):

	total_operator_cost = 0
	total_used_vehicles = 0
	in_source_distances = 0
	users_above_slab = 0
	average_ratio = 0.0
	combined_distance = 0.0
	vehicle_distance = 0.0
	single_user_vehicles = 0

	for color in coloring:
		cost, allotment = iva.allot_vehicles(coloring[color], vehicles)
		total_used_vehicles += len(allotment)
		distance_results = dStats.get_distance_from_allocation(allotment,distance_from_destination)

		for vehicle in allotment:
			vehilce_distances = [distance_from_destination[index] for index in vehicle.passengers]
			maximum_vehicle_distance = max(vehilce_distances)/1000.0
			cost_incurred = 0

			if len(vehicle.passengers) == 1:
				rates[vehicle.passengers[0]] = maximum_vehicle_distance*20
				average_ratio += 1
				combined_distance += source_destination_data[vehicle.passengers[0]][vehicle.passengers[0]]
				vehicle_distance += source_destination_data[vehicle.passengers[0]][vehicle.passengers[0]]
				single_user_vehicles += 1

			if option == 1:
				if maximum_vehicle_distance <= 10:
					cost = cost + cost_slab[vehicle.cap][0] - vehicle.cost
					cost_incurred = cost_slab[vehicle.cap][0]
				elif maximum_vehicle_distance > 10 and maximum_vehicle_distance <= 20:
					cost = cost + cost_slab[vehicle.cap][1] - vehicle.cost
					cost_incurred = cost_slab[vehicle.cap][1]
				elif maximum_vehicle_distance > 20 and maximum_vehicle_distance <= 30:
					cost = cost + cost_slab[vehicle.cap][2] - vehicle.cost
					cost_incurred = cost_slab[vehicle.cap][2]
				else:
					cost = cost
					cost_incurred = vehicle.cost
			else:
				cost_incurred = maximum_vehicle_distance*15
				cost = cost + cost_incurred - vehicle.cost

			in_source_distances += dStats.users_stats_in_coloring(vehicle.passengers, source_data)
			users_above_slab += vStats.user_vs_vehicle_comparison(vehicle.passengers, rates, cost_incurred)

		total_operator_cost += cost

		revenue = sum(rates)-total_operator_cost
		
		average_ratio = average_ratio/total_used_vehicles
		combined_distance = combined_distance/total_used_vehicles
		vehicle_distance = vehicle_distance/total_used_vehicles

	return [revenue, in_source_distances/total_used_vehicles, users_above_slab, total_used_vehicles, average_ratio, combined_distance/vehicle_distance, single_user_vehicles]