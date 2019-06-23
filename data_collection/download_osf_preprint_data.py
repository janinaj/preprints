import urllib.request, json, time, os

PREPRINT_URL = 'https://api.osf.io/v2/preprints/?format=json'
OUTPUT_FILE = os.path.join('..', '..', 'raw_data', 'osf.json')

# total number of records collected
records = 0

with open(OUTPUT_FILE, 'w') as o:
	# while there are still records to fetch (usually 10 records per request)
	while True:
		with urllib.request.urlopen(PREPRINT_URL) as url:
		    data = json.loads(url.read().decode())

		    json.dump(data, o)
		    o.write('\n')

		    records += len(data['data'])

		    if data['links']['next'] is None:
		    	break

		    # get link to next set of records to download
		    PREPRINT_URL = data['links']['next']
		    
		    time.sleep(5)

print('{} records collected.'.format(records))
