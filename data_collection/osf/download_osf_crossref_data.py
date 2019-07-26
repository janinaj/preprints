import sys, os, json, time

sys.path.append(os.path.join('..', '..', 'util'))
import crossref

INPUT_FILE = os.path.join('..', '..', '..', 'data', 'osf', 'osf_records.json')
OUTPUT_FILE = os.path.join('..', '..', '..', 'data', 'osf', 'osf_crossref_records.json')

# current number of records collected
records_processed = set()

if os.path.exists(OUTPUT_FILE):
	with open(OUTPUT_FILE, 'r') as f:
		for line in f:
			data = json.loads(line)
			
			records_processed.add(data['id'])

print('{} records already processed.'.format(len(records_processed)))

# number of new records collected
new_records_processed = 0
with open(OUTPUT_FILE, 'a') as o:
	with open(INPUT_FILE, 'r') as f:
		for line in f:
			data = json.loads(line)

			for record in data['data']:
				if record['id'] not in records_processed:
					preprint = crossref.get_record(record['links']['preprint_doi'].replace('https://doi.org/', ''))

					crossref_publications = []
					if preprint is not None and \
						'message' in preprint and \
						'relation' in preprint['message'] and \
						'is-preprint-of' in preprint['message']['relation']:
						for pub in preprint['message']['relation']['is-preprint-of']:
							crossref_publications.append(crossref.get_record(pub['id']))

					if record['attributes']['doi'] != None:
						osf_publication = crossref.get_record(record['attributes']['doi'].replace('https://doi.org/', ''))
					else:
						osf_publication = None

					row = { 
						'id' : record['id'], 
						'preprint' : preprint,
						'crossref_publications' : crossref_publications,
						'osf_publication' : osf_publication,
					}
					
					json.dump(row, o)
					o.write('\n')
					o.flush()

					new_records_processed += 1

print('{} new records collected.'.format(new_records_processed))