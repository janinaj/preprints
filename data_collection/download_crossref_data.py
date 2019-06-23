import os, json, time
from habanero import Crossref

cr = Crossref()

OUTPUT_FILE = os.path.join('..', '..', 'raw_data', 'CrossRef.json')

with open(OUTPUT_FILE, 'a') as o:
	saved_results = 0
	cursor = '*'

	# while there are still records to fetch
	while True:
		try:
			results = cr.works(filter = { 'type' : 'posted-content' }, cursor = cursor, limit = 1000)
			time.sleep(30)
		except Exception as e:
			print(e)

			# retry after 1 hour
			print('Retry: ' + URL)
			time.sleep(3600)

		for result in results:
			total_results = result['message']['total-results']

			# get token for next set of records
			cursor = result['message']['next-cursor']

			# somehow there is an error if there is a backslash on the token
			cursor = cursor.replace('\\', '')
			
			for item in result['message']['items']:
				json.dump(item, o)
				o.write('\n')

				saved_results += 1

		if saved_results >= total_results:
			break
		
print('{} records collected.'.format(saved_results))