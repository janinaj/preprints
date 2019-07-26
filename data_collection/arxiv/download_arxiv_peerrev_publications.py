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
	# for each file there are a bunch of arXiv records
	for file in files:
		root = ET.parse(os.path.join(INPUT_FOLDER, file))

		# for each arXiv record in the file
		for record in root.find('oai:ListRecords', namespaces):
			# check if it is a record
			if record.tag == '{' + namespaces['oai'] + '}' + 'record':
				# find the metadata tag
				metadata = record.find('oai:metadata/arXiv:arXiv', namespaces)

				# if it has one, it means the record is not deleted
				if metadata is not None:

					# find the doi
					doi = metadata.find('arXiv:doi', namespaces)

					# if it has a doi, download the CrossRef record if there is one
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