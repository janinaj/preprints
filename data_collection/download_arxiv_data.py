import os, urllib.request, time
import xml.etree.ElementTree as ET


ARXIV_URL = 'http://export.arxiv.org/oai2?verb=ListRecords'
METADATA_FORMAT = 'arXivRaw' # possible values: oai_dc, arXiv, arXivRaw

OUTPUT_FOLDER = os.path.join('..', '..', 'raw_data', METADATA_FORMAT)
if not os.path.exists(OUTPUT_FOLDER):
	os.mkdir(OUTPUT_FOLDER)

namespaces = {'oai': 'http://www.openarchives.org/OAI/2.0/'}

file_count = 0

# while there are still records to fetch
while True:
	if file_count == 0:
		URL = ARXIV_URL + '&metadataPrefix=' + METADATA_FORMAT
		
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
	resumption_token = root.find('oai:ListRecords/oai:resumptionToken', namespaces)
	if resumption_token is not None:
		resumption_token = resumption_token.text
	else:
		break

	URL = ARXIV_URL + '&resumptionToken=' + resumption_token

	# request data every 30 seconds
	time.sleep(30)
		
print('{} files saved.'.format(file_count))