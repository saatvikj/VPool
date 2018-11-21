import pickle

def read_file(filename):
	file = filename
	data = None
	with (open(file, "rb")) as openfile:
		data = pickle.load(openfile)
	return data

if __name__ == '__main__':
	print(read_file('saatvik_data_len_129_152540.pkl'))