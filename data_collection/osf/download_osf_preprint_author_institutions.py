# download the institution information for each contributor for OSF Preprint API records collected

import sys, json, os

sys.path.append(os.path.join('..', '..', 'util'))
import util

OSF_AUTHOR_FILE = os.path.join('..', '..', '..', 'raw_data', 'osf', 'osf_authors.json')
OUTPUT_FILE = os.path.join('..', '..', '..', 'raw_data', 'osf', 'osf_author_institutions.json')

# OSF_AUTHOR_FILE = os.path.join('..', '..', '..', 'data', 'osf', 'osf_authors.json')
# OUTPUT_FILE = os.path.join('..', '..', '..', 'data', 'osf', 'osf_author_institutions.json')

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
	with open(OSF_AUTHOR_FILE, 'r') as f:
		for line in f:
			record = json.loads(line)

			if record['id'] not in records_processed:
				institution_data = { 'id' : record['id'], 'data' : {} }

				for author_list in record['data']:
					for author in author_list['data']:
						try:
							institution_url = author['embeds']['users']['data']['relationships']['institutions']['links']['related']['href']
						except:
							institution_url = None

						if institution_url is not None:
							institution_list = []
							while True:
								status, data = util.download_from_url(institution_url)

								if status == 'SUCCESS':
									institution_list.append(data)

									if data['links']['next'] is None:
										break

									# get link to next set of records to download
									institution_url = data['links']['next']
								else:
									break

							institution_data[author['id']] = institution_list


				json.dump(institution_data, o)
				o.write('\n')
				o.flush()

				new_records_processed += 1

print('institution information from {} records collected.'.format(new_records_processed))
