from __future__ import division
import sys
import os
sys.path.insert(0,os.path.abspath(os.path.join(os.getcwd(),os.pardir)))
import folium
import pandas as pd
from graph import parse_nyc_data as nyc
from models.Request import Request


def create_map(requests):
	"""
	Function to create the map depicting positions
	of all sources and destinations from given 
	requests (NYC only). Creates an interactive
	webpage for the same based on leaflet.js

	Args:
		requests: A list of objects of the class
		Request corresponding to each rider in the
		system.
		
	Returns:
		Void
	"""
	lat = 40.7128
	longd = -74.0060

	data_map = folium.Map(location=[lat,longd],zoom_start=10)
	feature_group = folium.FeatureGroup("Locations")

	requests = [requests[19], requests[50], requests[86], requests[14]]

	for i,request in enumerate(requests):
		feature_group.add_child(folium.Marker(location=[request.source_lat,request.source_long],popup=str(i)))
		feature_group.add_child(folium.Marker(location=[request.dest_lat,request.dest_long],popup=str(i),icon=folium.Icon(color='red')))

	data_map.add_child(feature_group)
	data_map.save(outfile = "map.html")


if __name__ == '__main__':
	data = nyc.read_dataset('nyc_taxi_data_2014.csv', time_start='2014-01-02 09:00:00', time_end='2014-01-02 09:05:00')
	requests = nyc.create_request_objects(data)
	create_map(requests[:100])