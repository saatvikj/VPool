import pandas as pd
import numpy
from datetime import datetime
from Request import Request

def change_string_to_datetime(column):
	column = datetime.strptime(column, '%Y-%m-%d %H:%M:%S')
	return column

def read_dataset(filepath):
	ny_dataset = pd.read_csv(filepath)
	ny_dataset['pickup_datetime'] = ny_dataset['pickup_datetime'].map(change_string_to_datetime)

	time_start = change_string_to_datetime('2014-01-08 09:00:00')
	time_end = change_string_to_datetime('2014-01-08 09:10:00')
	start_condition = ny_dataset['pickup_datetime'] > time_start
	end_condition = ny_dataset['pickup_datetime'] < time_end

	subset = ny_dataset[start_condition & end_condition]
	return subset


def create_request_objects(data):
	
	requests = []
	for index, row in data.iterrows():
		request = Request(row['pickup_latitude'],row['pickup_longitude'],row['dropoff_latitude'],row['dropoff_longitude'],row['pickup_datetime'],row['passenger_count'])
		requests.append(request)

	return requests



if __name__ == '__main__':
	read_dataset('nyc_taxi_data_2014.csv')