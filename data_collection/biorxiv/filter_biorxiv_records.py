# Save bioRxiv records to a separate file

import os, json

INPUT_FILE = os.path.join('..', '..', '..', 'raw_data', 'CrossRef', 'CrossRef.json')
OUTPUT_FILE = os.path.join('..', '..', '..', 'raw_data', 'biorxiv', 'biorxiv.json')

records_processed = 0
with open(OUTPUT_FILE, 'w') as o:
	with open(INPUT_FILE, 'r') as f:
		for line in f:
			record = json.loads(line)

			# check if record is from biorxiv
			if 'institution' in record and record['institution']['name'] == 'bioRxiv':
				json.dump(record, o)
				o.write('\n')

				records_processed += 1

print('{} bioRxiv records.'.format(records_processed))