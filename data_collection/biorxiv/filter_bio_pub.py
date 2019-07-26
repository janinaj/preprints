import os, json

INPUT_FILE = os.path.join('..', '..', '..', 'raw_data', 'CrossRef', 'CrossRef.json')

biorxiv_dois = []
with open(INPUT_FILE, 'r') as f:
	for line in f:
		record = json.loads(line)

		# check if record is from biorxiv
		if 'institution' in record and record['institution']['name'] == 'bioRxiv':
			biorxiv_dois.append(record['DOI'])

print('{} bioRxiv records.'.format(len(biorxiv_dois)))

CROSSREF_RESULTS_FILE = os.path.join('..', '..', '..', 'raw_data', 'CrossRef', 'crossref_title_author_search_results.json')
OUTPUT_FILE = os.path.join('..', '..', '..', 'raw_data', 'biorxiv', 'biorxiv_title_author_search_results_orig.json')

with open(OUTPUT_FILE, 'w') as o:
	with open(CROSSREF_RESULTS_FILE, 'r') as f:
		for line in f:
			record = json.loads(line)
			if record['DOI'] in biorxiv_dois:
				record['id'] = record['DOI']
				o.write(line)