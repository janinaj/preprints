import json, os

def extract_tree_structure(data, key, tree, level = 0, is_list = False):
	if isinstance(data, dict):
		subtree = tree
		if key != None:
			if is_list:
				data_type = 'dict'
			else:
				data_type = 'list of dict'

			if key not in tree:
				tree[key] = {'type' : data_type, 'children' : {}}

			# THIS SHOULD NOT HAPPEN BUT JUST IN CASE
			elif data_type != tree[key]['type']:
				print('DIFF TYPES')
				print(key)
				print(data_type)
				input(tree[key]['type'])

			subtree = tree[key]['children']
			
		for key, value in data.items():
			extract_tree_structure(value, key, subtree, level + 1)
	elif isinstance(data, list):
		for value in data:
			extract_tree_structure(value, key, tree, level, True)
	else:
		if is_list:
			data_type = 'list of {}'.format(type(data).__name__)
		else:
			data_type = '{}'.format(type(data).__name__)

		if key not in tree or (data_type != tree[key] and tree[key] == 'NoneType'):
			tree[key] = data_type

		# THIS SHOULD NOT HAPPEN BUT JUST IN CASE
		elif data_type != tree[key] and not (tree[key] == 'NoneType' or data_type == 'NoneType'):
			print('DIFF TYPES')
			print(key)
			print(data_type)
			input(tree[key])

file = os.path.join('..', '..', 'data', 'share-jan-2019.json')

tree = {}

with open(file, 'r') as f:
	for line in f:
		data = json.loads(line)
		extract_tree_structure(data, None, tree)

with open(os.path.join('..', '..', 'data_exploration_results', 'share_data_format.json'), 'w') as o:
	json.dump(tree, o, indent=4, sort_keys=True)
