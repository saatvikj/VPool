import datetime
import pandas as pd
from driver_script import runner
import glob
import sys


filenames = []
for file in glob.glob(sys.argv[1]+"/*.pkl"):
	filenames.append(file)

# filenames = filenames[:int(sys.argv[4])]

df = pd.DataFrame(columns=['Title','Size','DSATUR','WVC','Difference','DSATUR More Than Vehicle','WVC More Than Vehicle','DSATUR Vehicles','WVC Vehicles', 'DSATUR Ratio','WVC Ratio','DSATUR Single user vehicles','WVC Single user vehicles'])
for i,name in enumerate(filenames):
	pickle_results = runner(name,1, text_output=sys.argv[3])
	print(i)
	df.loc[i,'Title'] = name
	df.loc[i,'Size'] = pickle_results[0]
	df.loc[i,'WVC'] = pickle_results[1]
	df.loc[i,'DSATUR'] = pickle_results[2]	
	df.loc[i,'Difference'] = pickle_results[3]
	df.loc[i,'DSATUR More Than Vehicle'] = pickle_results[5]
	df.loc[i,'WVC More Than Vehicle'] = pickle_results[4]
	df.loc[i,'DSATUR Vehicles'] = pickle_results[7]	
	df.loc[i,'WVC Vehicles'] = pickle_results[6]	
	df.loc[i,'DSATUR Ratio'] = pickle_results[9]
	df.loc[i,'WVC Ratio'] = pickle_results[8]
	df.loc[i,'DSATUR Sharing Ratio'] = pickle_results[11]
	df.loc[i,'WVC Sharing Ratio'] = pickle_results[10]
	df.loc[i,'DSATUR Single user vehicles'] = pickle_results[13]
	df.loc[i,'WVC Single user vehicles'] = pickle_results[12]
	df.loc[i,'DSATUR Vehicle Distance'] = pickle_results[15]
	df.loc[i,'WVC Vehicle Distance'] = pickle_results[14]

df.to_csv(sys.argv[2])