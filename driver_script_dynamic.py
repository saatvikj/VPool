from datetime import datetime
from graph import parse_nyc_data as nyc
import networkx as nx
import random
import string


all_vehicles = {}
all_passengers = {}
all_ids = []



def generate_random_id():
	global all_ids


	while True:
		random = ''.join([random.choice(string.digits) for n in range(5)]) 
		if random not in all_ids:
			all_ids.append(random)
			return int(random)


def query_specific_route(vehicle_id):
	global all_vehicles
	global all_passengers


	vehicle_object = all_vehicles[vehicle_id]
	starting_point_id = vehicle_object.route[vehicle_object.route_flag]





def update_positions_of_active_vehicles(minutes, global_timer):
	global all_vehicles
	global all_passengers

	vehicle_items = all_vehicles.items()
	passenger_items = all_passengers.items()

	id_to_index_passenger_mapping = [passenger[0] for passenger in passenger_items if passenger.is_active == 1]
	vehicles_requiring_position_updates = [vehicle[1] for vehicle in vehicle_items if vehicle[1].is_active == 1]

	source_time_data, destination_time_data, source_destination_time_data = get_time_matrices()
	source_distance_data, destination_distance_data, source_destination_distance_data = get_distance_matrices()

	for vehicle_object in vehicles_requiring_position_updates:

		previous_route_flag = vehicle_object.route_flag
		current_position_id = int(vehicle_object.route[route_flag])

		update_iteration_timer = 0
		marker = previous_route_flag + 1

		#First get to nearest pair of nodes in the route
		while update_iteration_timer < minutes*60 and marker < len(vehicle_object.route):

			time_for_this_stop = 0
			
			if marker >= len(vehicle_object.route):
				#End of route

			else:
				passenger_id_for_current_waypoint = vehicle_object.route[marker-1]
				passenger_id_for_next_waypoint = vehicle_object.route[marker]
				current_position_type = vehicle_object.waypoint_type[marker-1]
				next_position_type = vehicle_object.waypoint_type[marker]

				

				if current_position_type == 'S' and next_position_type == 'S':
					time_for_this_stop = source_time_data[][]
					global_timer = global_timer + datetime.timedelta(seconds=time_for_this_stop)

					vehicle_object.distance_traveled += source_distance_data[][]
					all_passengers[passenger_id_for_current_waypoint].distance_traveled += source_distance_data[][]
					all_passengers[passenger_id_for_next_waypoint].pickup_time = global_timer
					all_passengers[passenger_id_for_next_waypoint].is_active = 1
					all_passengers[passenger_id_for_next_waypoint].car_status = 1

				elif current_position_type == 'S' and next_position_type == 'D':
					time_for_this_stop = source_destination_time_data[][]
					global_timer = global_timer + datetime.timedelta(seconds=time_for_this_stop)

					vehicle_object.distance_traveled += source_destination_distance_data[][]
					all_passengers[passenger_id_for_current_waypoint].distance_traveled += source_destination_distance_data[][]
					all_passengers[passenger_id_for_next_waypoint].dropoff_time = global_timer
					all_passengers[passenger_id_for_next_waypoint].is_active = 0

				elif current_position_type == 'D' and next_position_type == 'S':
					time_for_this_stop = source_destination_time_data[][]
					global_timer = global_timer + datetime.timedelta(seconds=time_for_this_stop)

					vehicle_object.distance_traveled += source_destination_distance_data[][]
					all_passengers[passenger_id_for_current_waypoint].distance_traveled += source_destination_distance_data[][]
					all_passengers[passenger_id_for_next_waypoint].pickup_time = global_timer
					all_passengers[passenger_id_for_next_waypoint].is_active = 1
					all_passengers[passenger_id_for_next_waypoint].car_status = 1

				else:
					time_for_this_stop = destination_time_data[][]
					global_timer = global_timer = datetime.timedelta(seconds=time_for_this_stop)

					vehicle_object.distance_traveled += destination_distance_data[][]
					all_passengers[passenger_id_for_current_waypoint].distance_traveled += destination_distance_data[][]
					all_passengers[passenger_id_for_next_waypoint].dropoff_time = global_timer
					all_passengers[passenger_id_for_next_waypoint].is_active = 0

				marker += 1

				update_iteration_timer += time_for_this_stop

			global_timer = global_timer - datetime.timedelta(seconds=time_for_this_stop)
			update_iteration_timer -= time_for_this_stop
			vehicle_object.route_flag = marker-2

		distances, times, locations = query_specific_route(vehicle_object.vehicle_id)
		
		time_left = minutes*60 - update_iteration_timer

		specific_location_timer = 0
		iterator = 0

		while specific_location_timer <= time_left:
			specific_location_timer += times[iterator]
			iterator += 1

		vehicle_object.current_position = locations[iterator-1]

		for passenger_object in vehicle_object.passengers:
			if passenger_object.is_active == 1 and passenger_object.car_status == 1:
				passenger_object.current_position = vehicle_object.current_position


def set_routes_for_vehicles(text_output):

	global all_vehicles
	global all_passengers

	vehicle_items = all_vehicles.items()
	vehicles_requiring_route_updates = [vehicle[1] for vehicle in vehicle_items if vehicle[1].is_active == 1 and vehicle[1].update_required == 1]

	for vehicle_object in vehicles_requiring_route_updates:
		file_contents = []
		file_contents.append(str(len(vehicle_object.passengers))+'\n')
		file_contents.append(str(vehicle_object.capacity)+'\n')

		occupants_string = ""
		for user in vehicle.passengers:
			occupants_string = occupants_string + str(user.passenger_id) +','
		occupants_string = occupants_string[:len(occupants_string)-1]

		file_contents.append(occupants_string+'\n')

		file_contents.append(",".join(vehicle_object.current_position))

		#First put sources of passengers
		for user in vehicle_object.passengers:
			if user.car_status == 1:
				file_contents.append(",".join(vehicle_object.current_position))
			else:
				file_contents.append(",".join(user.source_location))

		#Then put destination of passengers
		for user in vehicle_object.passengers:
			file_contents.append(",".join(user.destination_location))

		file = open(text_output,"w+")
		file.writelines(file_contents)
		file.close()

		query_string = 'java -jar vehicle_routing.jar ' + text_output
		route = os.popen(query_string).read()

		vehicle_object.route = route.split(" ")


def add_new_vehicles(vehicle_allocation, graph):

	global all_vehicles
	global all_passengers

	information = nx.get_node_attributes(graph, 'information')

	for car in vehicle_allocation:

		#First see if there are any idle vehicles available of same capcity
		vehicle_items = all_vehicles.items()
		inactive_vehicles_of_same_capacity = [vehicle[1] for vehicle in vehicle_items if vehicle[1].is_active == 0 and vehicle[1].capacity == car.capacity]


		#If available, add passengers to that vehicle and make it active
		if len(inactive_vehicles_of_same_capacity) > 0:
			vehicle_object = inactive_vehicles_of_same_capacity[0]
			vehicle_object.is_active = 1
			vehicle_object.update_required = 1

		#Else create a new vehicle object required to do the computation and add to all vehicles
		else:
			vehicle_object = Cab(generate_random_id(), car.capacity, car.cost, [], [], 0, [], 1, 1, 0, [])
			all_vehicles[vehicle_object.unique_id] = vehicle_object

		#Create the passenger list from the obtained index from the allocation
		passengers_list = []
		for passenger in car.passengers:
			passenger_id = information[passenger][1]
			passenger_object = all_passengers[passenger_id]
			passenger_object.alloted_vehicle = vehicle_object.unique_id
			passenger_object.is_active = 1
			passengers_list.append(passenger_object)


		#Add passengers to the vehicle
		vehicle_object.passengers = passengers_list


def allot_vehicles_to_color_classes(color_classes, graph):

	global all_vehicles
	global all_passengers

	for color_class in color_classes:

		#Get information about the graph nodes
		information = nx.get_node_attributes(graph, 'information')

		#Initiate all the vehicles and passengers in the given color class.
		class_vehicles = []
		class_passengers = []

		#Find all passengers and vehicles and fill the lists.
		for node in color_class:
			if information[node][0] == 1:
				class_vehicles.append(node)
			else:
				class_passengers.append(node)

		class_passengers_iterator = 0
		class_vehicles_iterator = 0

		#First fill all vehicles, so iterate over all vehicles
		while class_vehicles_iterator != len(class_vehicles):

			#Find the vehicle object for current iteration
			vehicle_index = class_vehicles[class_vehicles_iterator]
			vehicle_id = information[vehicle_index][1]
			vehicle_object = all_vehicles[vehicle_id]


			#If the vehicle has space then till the time it can be filled, add passengers.
			if len(vehicle_object.passengers) < vehicle_object.capacity:
				while len(vehicle_object.passengers) != vehicle_object.capacity:


					#If passengers are available to fill, fill them.
					if class_passengers_iterator < len(class_passengers):

						#Find the passenger object for current index
						passenger_index = class_passengers[class_passengers_iterator]
						passenger_id = information[passenger_index][1]
						passenger_object = all_passengers[passenger_id]

						#Add passenger object as passenger to the vehicle and increment to next passenger.
						vehicle_object.passengers.append(passenger_object)
						passenger_object.alloted_vehicle = vehicle_id
						passenger_object.is_active = 1

						class_passengers_iterator += 1

						#Update flag of route update required to indicate vehicle route needs to be updated.
						vehicle_object.update_required = 1

			class_vehicles_iterator += 1

		if class_passengers_iterator < len(class_passengers):
			remaining_passengers = class_passengers[class_passengers_iterator:]
			cost, vehicle_allocation = iva.allot_vehicles(remaining_passengers, vehicle_list)
			add_new_vehicles(vehicle_allocation)


def get_first_requests(filepath, start_time, end_time, first_number):
	data = nyc.read_dataset(filepath, start_time, end_time)
	requests = nyc.create_request_objects(data, first_number)

	return requests
	


def runner(filepath, start_time, end_time, initial_number, iteration_number, goal_number, delta, minutes):
	
	global all_vehicles
	global all_passengers

	#Get first requests
	requests = get_first_requests(filepath, start_time, end_time, initial_number)
	vehicles = []

	#Create admissibility matrix from the data
	source_distance_data, destination_distance_data, source_destination_distance_data = get_distance_matrices(requests, vehicles)
	admissibility_matrix = create_admissibility_matrix(source_distance_data, destination_distance_data, source_destination_distance_data, delta, requests, vehicles)

	#Create properties for nodes (Weights, type and ID)
	node_type_properties = create_node_properties(requests, vehicles)
	weights = create_weights(requests, vehicles, source_distance_data, destination_distance_data, source_destination_distance_data)
	
	#Create graph and color it
	graph = create_graph_from_admissibility_matrix(admissibility_matrix, node_properties, weights)
	color_classes = weighted_vertex_coloring(graph)

	#Allot vehicles to color classes
	allot_vehicles_to_color_classes(color_classes, graph)

	#Allot routes to vehicles
	set_routes_for_vehicles(text_output)

	request_counter = len(requests)

	global_timer = end_time

	while request_counter >= goal_number:


		#Update positions since last x minutes
		update_positions_of_active_vehicles(minutes)

		#Get new requests
		requests = get_new_requests(global_timer, iteration_number)

		#Create graph


		#Call coloring routine


		#Calculate routes
		set_routes_for_vehicles(text_output)

		request_counter += iteration_number



if __name__ == '__main__':
	runner()