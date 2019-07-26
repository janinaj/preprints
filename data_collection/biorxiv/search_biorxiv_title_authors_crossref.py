import sys, os, json

sys.path.append(os.path.join('..', '..', 'util'))
import util, crossref

INPUT_FILE = os.path.join('..', '..', '..', 'raw_data', 'biorxiv', 'biorxiv_records.json')
OUTPUT_FILE = os.path.join('..', '..', '..', 'raw_data', 'biorxiv', 'biorxiv_title_author_search_results.json')

# total number of records collected
records_processed = set()

if os.path.exists(OUTPUT_FILE):
	with open(OUTPUT_FILE, 'r') as f:
		for line in f:
			record = json.loads(line)
			
			records_processed.add(record['id'])

print('{} records already processed.'.format(len(records_processed)))

new_records_processed = 0
with open(OUTPUT_FILE, 'a') as o:
	with open(INPUT_FILE, 'r') as f:
		for line in f:
			record = json.loads(line)

			if record['DOI'] not in records_processed:
				title = ''
				for title in record['title']:
					title += title + ' '
				title = title.strip()

				first_author_str = ''
				if 'author' in record:
					for author in record['author']:
						if author['sequence'] == 'first':
							if 'given' in author:
								first_author_str = author['given']

							if 'family' in author:
								first_author_str = first_author_str + ' ' + author['family']

							if 'suffix' in author:
								first_author_str = first_author_str + ' ' + author['suffix']

							# it seems that if name is present, there are no other name fields (e.g. given, family)
							if 'name' in author:
								first_author_str = first_author_str + ' ' + author['name']
							break

				result = crossref.search_title_author(util.normalize_str(title), 
					util.normalize_str(first_author_str),
					record['DOI'])

				result['id'] = record['DOI']

				new_records_processed += 1

				json.dump(result, o)
				o.write('\n')
				o.flush()

print('Search results for {} records collected.'.format(new_records_processed))