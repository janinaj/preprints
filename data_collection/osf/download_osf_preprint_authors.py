# download the contributor information for OSF Preprint API records collected

import sys, json, os

sys.path.append(os.path.join('..', '..', 'util'))
import util

OSF_PREPRINT_FILE = os.path.join('..', '..', '..', 'data', 'osf', 'osf_records.json')
OUTPUT_FILE = os.path.join('..', '..', '..', 'data', 'osf', 'osf_authors.json')

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
	with open(OSF_PREPRINT_FILE, 'r') as f:
		for line in f:
			records = json.loads(line)

			for record in records['data']:
				if record['id'] not in records_processed:
					contributor_url = record['relationships']['contributors']['links']['related']['href']
					
					contributor_data = { 'id' : record['id'], 'data' : [] }
					
					while True:
						status, data = util.download_from_url(contributor_url)

						if status == 'SUCCESS':
							contributor_data['data'].append(data)

							if data['links']['next'] is None:
								break

							# get link to next set of records to download
							contributor_url = data['links']['next']
						else:
							break

					json.dump(contributor_data, o)
					o.write('\n')
					o.flush()

					new_records_processed += 1

print('{} new records collected.'.format(new_records_processed))