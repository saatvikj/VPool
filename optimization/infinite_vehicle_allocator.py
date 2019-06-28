import copy
import sys
import os
sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),os.pardir)))
import math
from models.Vehicle import comparator


def allot_vehicles(coloring, vehicles):
	"""
	Function to first get minimum cost through solving
	the 0-1 knapsack problem and then backtracking it
	to get the corresponding allotment of passengers
	in the vehicle.

	Args:
		coloring: The color class (people to be allotted)
		vehicles: List of vehicle objects

	Returns:
		A list of allotted vehicles with passengers.
	"""	
	number_people=len(coloring)
	vehicle_list=[]
	person_iterator = 0
	
	for i in vehicles:
		required_copies = 0
		if number_people%i.cap == 0:
			required_copies=number_people/i.cap
		else:
			required_copies=number_people/i.cap
			required_copies=required_copies+1		
		for j in range(required_copies):
			vehicle = copy.deepcopy(i)
			vehicle_list.append(vehicle)

	total_required_vehicles=len(vehicle_list)
	table=[[-1 for u in range(10**5)] for y in range(total_required_vehicles)]
	minimum_cost=knapsack_with_atleast(0,0,table,total_required_vehicles,number_people,vehicle_list)

	i = 0
	weight = 0
	allotment = []

	while (i<=total_required_vehicles-1 and weight<=number_people):
		if i == total_required_vehicles-1:
			if (person_iterator+vehicle_list[i].cap >= number_people):
				vehicle_list[i].passengers = coloring[person_iterator:]
			else:
				vehicle_list[i].passengers = coloring[person_iterator:person_iterator+vehicle_list[i].cap]
				person_iterator+=vehicle_list[i].cap
			allotment.append(vehicle_list[i])
			i += 1
		else:
			if(table[i][weight]-table[i+1][weight+vehicle_list[i].cap]==vehicle_list[i].cost):
				weight+=vehicle_list[i].cap
				if (person_iterator+vehicle_list[i].cap >= number_people):
					vehicle_list[i].passengers = coloring[person_iterator:]
				else:
					vehicle_list[i].passengers = coloring[person_iterator:person_iterator+vehicle_list[i].cap]
					person_iterator+=vehicle_list[i].cap
				allotment.append(vehicle_list[i])
				i += 1
			else:
				i += 1
	return minimum_cost, allotment


def knapsack_with_atleast(index, value, table, n, lower_bound, vehicles):
	"""
	Implementation of the dynamic programming 0-1 knapsack algorithm
	with a variation that you need to fit a value at least greater than
	equal to given value filled in the bag (vehicles in our case).

	Args:
		index: Current index of vehicle being considered
		value: Number of people already allotted 
		n: Total number of vehicles
		lower_bound: The lower bound on number of objects
		(people)  in the bag (vehicles), equal to number of
		people in our case.
		vehicles: The list of available vehicles, contains
		information about both cost and capacity of the 
		vehicles.
	
	Returns:
		The minimum cost that satisfied the above criteria.
	"""
	if index == n:
		if value >= lower_bound:
			return 0
		else:
			return 10**30
	if table[index][value] != -1:
		return table[index][value]
	
	cost_without_i = knapsack_with_atleast(index+1, value, table, n, lower_bound, vehicles)
	cost_with_i = knapsack_with_atleast(index+1, value+vehicles[index].cap, table, n, lower_bound, vehicles)

	if cost_with_i != 10**30:
		cost_with_i += vehicles[index].cost

	choice = min(cost_without_i, cost_with_i)
	table[index][value] = choice

	return table[index][value]


if __name__ == '__main__':
	pass