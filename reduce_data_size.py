import graph.parse_nyc_data as nyc
import pandas as pd


data = nyc.read_dataset('nyc_taxi_data_2014.csv', time_start='2014-01-01 08:00:00', time_end='2014-01-30 13:00:00')
data.to_csv('reduced_nyc_data.csv')
print(data.shape)