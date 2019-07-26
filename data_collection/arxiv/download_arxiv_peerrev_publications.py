import os, json, time
import xml.etree.ElementTree as ET
from habanero import Crossref

def get_record(doi):
	retries = 0
	
	while retries < 5:
		try:
			record = cr.works(doi)
			break
		except Exception as e:
			print(e)
			record = { 'error' : str(e) }

			retries += 1
			print('Retry: {} for {}'.format(retries, doi))

			time.sleep(10)
		
		time.sleep(0.05)

	return record

INPUT_FOLDER = os.path.join('..', '..', 'raw_data', 'arXiv')
OUTPUT_FILE = os.path.join('..', '..', 'data', 'arxiv_peerrev_publications.json')

files = os.listdir(INPUT_FOLDER)
if '.DS_Store' in files:
	files.remove('.DS_Store')

cr = Crossref()

namespaces = {'oai': 'http://www.openarchives.org/OAI/2.0/',
             'arXiv' : 'http://arxiv.org/OAI/arXiv/'}

with open(OUTPUT_FILE, 'w') as o:
	for file in files:
		root = ET.parse(os.path.join(INPUT_FOLDER, file))
		for record in root.find('oai:ListRecords', namespaces):
			if record.tag == '{' + namespaces['oai'] + '}' + 'record':

				metadata = record.find('oai:metadata/arXiv:arXiv', namespaces)
				if metadata is not None:

					doi = metadata.find('arXiv:doi', namespaces)
					if doi is not None:
						doi = doi.text
						identifier = record.find('oai:header/oai:identifier', namespaces).text
						id_ = metadata.find('arXiv:id', namespaces).text

						row = {
							'doi' : doi,
							'identifier' : identifier,
							'id' : id_,
							'data' : get_record(doi)
						}

						json.dump(row, o)
						o.write('\n')
						o.flush()