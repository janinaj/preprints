import os, urllib.request, time
import xml.etree.ElementTree as ET

EUROPEPMC_URL = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=SRC:PPR'

OUTPUT_FOLDER = os.path.join('..', '..', 'raw_data', 'europepmc')
if not os.path.exists(OUTPUT_FOLDER):
	os.mkdir(OUTPUT_FOLDER)

file_count = 3100

URL = EUROPEPMC_URL

# while there are still records to fetch
while True:	
	retry = True
	while retry:
		try:
			url_output = urllib.request.urlopen(URL, timeout=10000000)

			# means the current set of records were collected successfully
			retry = False
		except Exception as e:
			print(e)

			# retry after 1 hour
			print('Retry: ' + URL)
			time.sleep(3600)

	data = url_output.read().decode()

	# save fetched records to file
	file_count += 1
	file_name = os.path.join(OUTPUT_FOLDER, str(file_count) + '.xml')
	with open(file_name, 'w') as o:
		o.write(data)

	# get token for next set of records
	root = ET.parse(file_name)
	cursor_mark = root.find('nextCursorMark')
	if cursor_mark is not None:
		cursor_mark = cursor_mark.text
	else:
		break

	results = root.find('resultList/result')
	if results is None:
		break

	URL = EUROPEPMC_URL + '&cursorMark=' + cursor_mark

	# request data every second
	time.sleep(1)
		
print('{} files saved.'.format(file_count))