"""
Code that iterates over all files in the given
input folder, applies algorithms on it and stores
all results in a single compiled input CSV file.
"""
import datetime
import pandas as pd
from driver_script import runner
import utilities.pickle_utility as pUtils
import glob
import sys


filenames = []
for file in glob.glob(sys.argv[1]+"/*.pkl"):
	filenames.append(file)
	
j = 0
df = pd.DataFrame(columns=['Title','Size','DSATUR','WVC','Difference','DSATUR More Than Vehicle','WVC More Than Vehicle','DSATUR Vehicles','WVC Vehicles', 'DSATUR Ratio','WVC Ratio','DSATUR Single user vehicles','WVC Single user vehicles'])
for i,name in enumerate(filenames):

	try:
		raw_name, size, start_time, end_time = pUtils.get_details_from_name(name)
		pickle_results = runner(filename=name, option=1)
		print(j)
		df.loc[j,'Title'] = name
		df.loc[j,'Size'] = pickle_results[0]
		df.loc[j,'WVC'] = pickle_results[1]
		df.loc[j,'DSATUR'] = pickle_results[2]	
		df.loc[j,'Difference'] = pickle_results[3]
		df.loc[j,'DSATUR More Than Vehicle'] = pickle_results[5]
		df.loc[j,'WVC More Than Vehicle'] = pickle_results[4]
		df.loc[j,'DSATUR Vehicles'] = pickle_results[7]	
		df.loc[j,'WVC Vehicles'] = pickle_results[6]	
		df.loc[j,'DSATUR Ratio'] = pickle_results[9]
		df.loc[j,'WVC Ratio'] = pickle_results[8]
		df.loc[j,'DSATUR Sharing Ratio'] = pickle_results[11]
		df.loc[j,'WVC Sharing Ratio'] = pickle_results[10]
		df.loc[j,'DSATUR Single user vehicles'] = pickle_results[13]
		df.loc[j,'WVC Single user vehicles'] = pickle_results[12]
		df.loc[j,'DSATUR Vehicle Distance'] = pickle_results[15]
		df.loc[j,'WVC Vehicle Distance'] = pickle_results[14]

		j += 1
	except Exception as e:
		print(e)

df.to_csv(sys.argv[2])