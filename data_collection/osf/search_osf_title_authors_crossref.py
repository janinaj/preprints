import sys, os, json
from collections import OrderedDict

sys.path.append(os.path.join('..', '..', 'util'))
import util, crossref

INPUT_FILE = os.path.join('..', '..', '..', 'data', 'osf', 'osf_records.json')
AUTHOR_FILE = os.path.join('..', '..', '..', 'data', 'osf', 'osf_authors.json')

OUTPUT_FILE = os.path.join('..', '..', '..', 'data', 'osf', 'osf_title_author_search_results.json')

# total number of records collected
records_processed = set()

if os.path.exists(OUTPUT_FILE):
	with open(OUTPUT_FILE, 'r') as f:
		for line in f:
			data = json.loads(line)
			
			records_processed.add(data['id'])

print('{} records already processed.'.format(len(records_processed)))

osf_records = OrderedDict()

with open(INPUT_FILE, 'r') as f:
	for line in f:
		data = json.loads(line)

		for record in data['data']:
			if record['id'] not in records_processed:
				osf_records[record['id']] = {'title' : record['attributes']['title'], \
					'doi' : record['links']['preprint_doi'].replace('https://doi.org/', '')}

with open(AUTHOR_FILE, 'r') as f:
	for line in f:
		record = json.loads(line)
		
		if record['id'] in osf_records:
			first_author_str = ''
			try:
				for author_list in record['data']:
					for author in author_list['data']:
						if author['attributes']['bibliographic']:
							try:
								first_author = author['embeds']['users']['data']['attributes']
							except:
								first_author = author['embeds']['users']['errors'][0]['meta']

							first_author['unregistered_contributor'] = author['attributes']['unregistered_contributor']

							if first_author['given_name'] != '':
								first_author_str = first_author['given_name']

							if author['middle_names'] != '':
								first_author_str = first_author_str + ' ' + first_author['middle_names']

							if author['family_name'] != '':
								first_author_str = first_author_str + ' ' + first_author['family_name']

							if 'suffix' in author and author['suffix'] != '':
								first_author_str = first_author_str + ' ' + first_author['suffix']

							if first_author_str == '':
								first_author_str = first_author['full_name']

							break

					if first_author_str != '':
						break
			except:
				pass

			osf_records[data['id']]['first_author_str'] = first_author_str

new_records_processed = 0
with open(OUTPUT_FILE, 'a') as o:
	for id_, record in osf_records.items():
		result = crossref.search_title_author(util.normalize_str(record['title']), 
			util.normalize_str(record['first_author_str']),
			record['doi'])

		result['id'] = id_

		new_records_processed += 1

		json.dump(result, o)
		o.write('\n')
		o.flush()

print('Search results for {} records collected.'.format(new_records_processed))

##########################################################
			# input(osf_records[data['DOI'].split('/')[2]])
			# title = data['title'][0]

			# if title.strip() != '':

			# 	first_author = ''
			# 	if 'author' in data:
			# 		for author in data['author']:
			# 			if author['sequence'] == 'first':
			# 				if 'given' in author:
			# 					first_author = author['given']

			# 				if 'family' in author:
			# 					first_author = first_author + ' ' + author['family']

			# 				if 'suffix' in author:
			# 					first_author = first_author + ' ' + author['suffix']

			# 				# it seems that if name is present, there are no other name fields (e.g. given, family)
			# 				if 'name' in author:
			# 					first_author = first_author + ' ' + author['name']

# errors = 0
# all_ = 0
# with open(OUTPUT_FILE, 'r') as f:
# 	for line in f:
# 		data = json.loads(line)
# 		all_ += 1
# 		if 'error' in data and not data['error'].startswith('Empty title'):
# 			errors += 1
# 			# break
# 		# else:
# 		# processed_dois.append(data['DOI'])
# print(errors)
# print(all_)
# existing_results = {}
# with open(CURRENT_FILE, 'r') as f:
# 	for line in f:
# 		data = json.loads(line)
# 		if 'error' in data:
# 			pass
# 		# elif data['DOI'] not in processed_dois:
# 		elif data['DOI'] not in existing_results:
# 			existing_results[data['DOI']] = data

# print(errors)
# print(len(processed_dois))
# print(len(existing_results.keys()))
# cr = Crossref()

# with open(OUTPUT_FILE, 'a') as o:
# 	with open(INPUT_FILE, 'r') as f:
# 		for line in f:
# 			data = json.loads(line)

# 			# if data['DOI'] not in processed_dois:
# 			if data['DOI'] in existing_results:
# 				result = existing_results[data['DOI']]
# 			else:
# 				title = data['title'][0]

# 				if title.strip() != '':

# 					first_author = ''
# 					if 'author' in data:
# 						for author in data['author']:
# 							if author['sequence'] == 'first':
# 								if 'given' in author:
# 									first_author = author['given']

# 								if 'family' in author:
# 									first_author = first_author + ' ' + author['family']

# 								if 'suffix' in author:
# 									first_author = first_author + ' ' + author['suffix']

# 								# it seems that if name is present, there are no other name fields (e.g. given, family)
# 								if 'name' in author:
# 									first_author = first_author + ' ' + author['name']

# 					# if 'contributors' in data['lists']:

# 					# 	data_creators = {}
# 					# 	data_contributors = {}
# 					# 	for contributor in data['lists']['contributors']:
# 					# 		if contributor['type'] == 'person':
# 					# 			if 'order_cited' in contributor:
# 					# 				# we don't care if this is repeating, just get any author with that order_cited value
# 					# 				if contributor['relation'] == 'creator':
# 					# 					data_creators[contributor['order_cited']] = contributor['name']
# 					# 				else:
# 					# 					data_contributors[contributor['order_cited']] = contributor['name']

# 					# 	if len(data_creators.keys()) > 0:
# 					# 		min_order_cited = min(data_creators.keys())
# 					# 		first_author = data_creators[min_order_cited]
# 					# 	elif len(data_contributors.keys()) > 0:
# 					# 		min_order_cited = min(data_contributors.keys())
# 					# 		first_author = data_contributors[min_order_cited]

# 					retries = 0
# 					while retries < 10:
# 						query_title = normalize_str(title)
# 						query_author = normalize_str(first_author)
# 						try:
# 							if first_author.strip() != '':
# 								result = cr.works(query_title=query_title, query_author=query_author, limit = 10)
# 							else:
# 								result = cr.works(query_title=query_title, limit = 10)
							
# 							break
# 						except Exception as e:
# 							retries += 1

# 							if retries == 1:
# 								print('Error for DOI {}'.format(data['DOI']))
# 							print(e)
# 							print('Retry #{}'.format(retries))

# 							result = { 'error' : str(e), 'query_title' :  query_title, 'query_author' : query_author}
# 							time.sleep(10 * retries)
					
# 					result['DOI'] = data['DOI']

# 					time.sleep(0.05)
# 				else:
# 					print('Error for DOI {} : empty title'.format(data['DOI']))
# 					result = { 'error' : 'Empty title', 'DOI' : data['DOI'] }

# 			json.dump(result, o)
# 			o.write('\n')
# 			o.flush()