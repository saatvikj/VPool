from flask import Flask, render_template, request, Response, url_for, redirect
from werkzeug import secure_filename
import os
import glob
import folium
import driver_script


number_of_vehicles = 5
app = Flask(__name__, template_folder='./static', static_folder='./static', static_url_path='/static')


def marker_to_js(route):
	"""
	Function to return the popup text for all the
	markers that will appear on the map using
	leaflet.js

	Args:
		route: The route that the vehicle will
		be following. It is also the order in
		which markers are added to the map.

	Returns:
		A list of strings corresponding to each
		marker in the map and a list telling the
		order of points, S or D.
	"""
	sources = []
	popup = []
	order = []
	for i in route:
		if i not in sources:
			sources.append(i)
			popup.append('Source of '+str(i))
			order.append('S')
		else:
			popup.append('Destination of '+str(i))
			order.append('D')

	return popup, order


def point_to_js(points):
	"""
	Function to return the string that will
	correspond to creation of the leaflet.js
	LatLng objects as a single list.

	Args:
		points: The different points that the
		vehicle will be reaching. It corresponds
		to the sources and destinations of the
		riders.

	Returns:
		A string that will act as array creation
		query string for leaflet.js
	"""
	main_string = '['
	point_list = []
	for point in points:
		point_list.append('new L.LatLng' + str(point))

	comma = ","
	main_string += comma.join(point_list) + ']'

	return main_string


def get_vehicle_details(i, root):
	"""
	Function to read the output files generated during
	runs of the algorithm specific to the vehicles and
	return the content.

	Args:
		i: The vehicle number whose contents need to be
		read.

		root: The algorithm type whose output needs to
		be read, 'std' for standard coloring and 'wvc'
		for weighted vertex coloring.

	Returns:
		The contents of the file as mentioned by the given
		parameters.
	"""
	contents = open(root+'/'+i+'.txt',"rb").read().split('\n')
	return contents
	

@app.route('/', methods=['POST','GET'])
def index():
	"""
	Flask function for the default route, it has
	the form that needs to be filled for running
	the algorithms on it.

	The form on the page consists of options to
	enter the place where data is being input from,
	the value of tolerance for admissibility, the
	input of all available cars and input of the
	actual file.

	Input format supported is of two types: .csv
	and .pkl, csv should be in NYC Taxi Open Data
	format only, and pkl should have data pickled
	in proper format (Refer to /utils/pickle_utility
	to see the same)
	"""
	if request.method == 'GET':
		return render_template('index.html')
	else:
		file = request.files['csv']
		filename = secure_filename(file.filename)
		file.save(os.path.join(os.getcwd(),filename))

		delta = float(request.form['delta'])
		country = request.form['name']
		time_start = request.form['start-time']
		time_end = request.form['end-time']
		size_limit = request.form['size-limit']

		if country == 'India':
			host = 'http://traffickarma.iiitd.edu.in:8091'

		else:
			host = '127.0.1.1:5000'

		name, extension = os.path.splitext(os.path.join(os.getcwd(),filename))

		if extension == '.pkl':
			results = driver_script.runner(os.path.join(os.getcwd(),filename), 1, delta = delta, port = host)
		else:
			results = driver_script.runner(os.path.join(os.getcwd(),filename), 2, delta = delta, time_start = time_start, time_end=time_end, port = host, size_limit=size_limit)
		number_of_vehicles = results[7] if results[7] > results[6] else results[6]
		return render_template('index.html', results = results)


@app.route('/results', methods=['POST','GET'])
def display_vehicle_results():
	"""
	Flask function for the route that displays
	the obtained results, it has a map with a
	sidebar that shows different kinds of statistics
	and details about the selected vehicle. The map
	shows the route that has been selected.

	It also has an option to select a new vehicle
	from whatever algorithm you want.
	"""

	if request.method == 'GET':
		number = '1'
		contents = get_vehicle_details(number, 'std')
		vehicle = contents[:6]
		
		std_vehicles = len(glob.glob(os.getcwd()+'/std/*.txt'))
		wvc_vehicles = len(glob.glob(os.getcwd()+'/wvc/*.txt'))
		
		number_of_vehicles = std_vehicles if std_vehicles > wvc_vehicles else wvc_vehicles

		route = contents[6].split(" ")
		for x, car in enumerate(route):
			route[x] = int(car)
		
		passengers = contents[5].split(",")
		for x, passenger in enumerate(passengers):
			passengers[x] = int(passenger)

		rider_details = contents[7:]
		sources = []
		points = []
		for i in route:
			index = passengers.index(i)
			details = rider_details[index].split(" ")
			if int(i) not in sources:
				points.append((float(details[1]),float(details[2])))
				sources.append(int(i))
			else:
				points.append((float(details[3]),float(details[4])))

		ave_lat = sum(p[0] for p in points)/len(points)
		ave_lon = sum(p[1] for p in points)/len(points)

		popup, order = marker_to_js(route)

		return render_template('map.html', length=number_of_vehicles, vehicle=vehicle, points = point_to_js(points), lat=ave_lat, long=ave_lon, coloring='Standard', number=number, popup=popup, order=order)

	if request.method == 'POST':
		number = request.form['vehicle']
		root = request.form['root']

		if root == 'std':
			root_string = 'Standard'
		else:
			root_string = 'WVC'

		contents = get_vehicle_details(number, root)
		vehicle = contents[:6]

		std_vehicles = len(glob.glob(os.getcwd()+'/std/*.txt'))
		wvc_vehicles = len(glob.glob(os.getcwd()+'/wvc/*.txt'))

		number_of_vehicles = std_vehicles if std_vehicles > wvc_vehicles else wvc_vehicles

		route = contents[6].split(" ")
		for x, car in enumerate(route):
			route[x] = int(car)
		
		passengers = contents[5].split(",")
		for x, passenger in enumerate(passengers):
			passengers[x] = int(passenger)

		rider_details = contents[7:]
		sources = []
		points = []
		for i in route:
			index = passengers.index(i)
			details = rider_details[index].split(" ")
			if int(i) not in sources:
				points.append((float(details[1]),float(details[2])))
				sources.append(int(i))
			else:
				points.append((float(details[3]),float(details[4])))

		ave_lat = sum(p[0] for p in points)/len(points)
		ave_lon = sum(p[1] for p in points)/len(points)

		popup, order = marker_to_js(route)

		return render_template('map.html', length=number_of_vehicles, vehicle=vehicle, points = point_to_js(points), lat=ave_lat, long=ave_lon, coloring=root_string, number=number, popup=popup, order=order)


if __name__ == '__main__':
	app.run(port='16000', debug=False)