import pickle

def read_file(filename):
	"""
	Function to read pickle file and give its data

	Args:
		filename: Name of pickle file

	Returns:
		Data dictionary that was stored in .pkl format.
	"""
	file = filename
	data = None
	with (open(file, "rb")) as openfile:
		data = pickle.load(openfile)
	return data

if __name__ == '__main__':
	print(read_file('saatvik_data_len_129_152540.pkl'))