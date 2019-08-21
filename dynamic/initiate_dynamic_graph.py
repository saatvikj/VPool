def create_dynamic_graph(adj_matrix, types):
	data = nx.Graph()
	for i in range(len(adj_matrix)):
		data.add_node(i)


	for i, source in enumerate(adj_matrix):
		for j, value in enumerate(source):
			if i != j and int(value) == 1:
				data.add_edge(i,j)

	nx.set_node_attributes(data, 1, 'weight')

	data = nx.complement(data)
	nx.set_node_attributes(data, 'rider', 'type')
	rider_type_dictionary = nx.get_node_attributes(data,'type')

	for i in range(len(adj_matrix)):
		rider_type_dictionary[i] = types[i]

	nx.set_node_attributes(data, rider_type_dictionary, 'type')

	return data