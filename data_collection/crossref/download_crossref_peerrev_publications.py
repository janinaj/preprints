import os, json, sys

sys.path.append(os.path.join('..', '..', 'util'))
import crossref

INPUT_FILE = os.path.join('..', '..', '..', 'raw_data', 'CrossRef', 'CrossRef.json')
OUTPUT_FILE = os.path.join('..', '..', '..', 'raw_data', 'CrossRef', 'crossref_peerrev_publications.json')

# total number of records collected
records_processed = set()

if os.path.exists(OUTPUT_FILE):
	with open(OUTPUT_FILE, 'r') as f:
		for line in f:
			data = json.loads(line)
			
			records_processed.add(data['id'])

print('{} records already processed.'.format(len(records_processed)))

new_records_processed = 0
with open(OUTPUT_FILE, 'a') as o:
	with open(INPUT_FILE, 'r') as f:
		for line in f:
			data = json.loads(line)

			if data['DOI'] not in records_processed:
				if 'relation' in data and 'is-preprint-of' in data['relation']:
					if len(data['relation']['is-preprint-of']) > 1:
						print('More than one publication: {}'.format(data['DOI']))

					record = crossref.get_record(data['relation']['is-preprint-of'][0]['id'])
				
					record['id'] = data['DOI']

					json.dump(record, o)
					o.write('\n')
					o.flush()

					new_records_processed += 1

print('{} new records collected.'.format(new_records_processed))