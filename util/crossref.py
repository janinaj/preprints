from habanero import Crossref
import time

cr = Crossref()

def get_record(doi):
	retries = 0
	
	while retries < 5:
		try:
			record = cr.works(doi)
			break
		except Exception as e:
			print(e)
			record = { 'error' : str(e) }

			if e.__class__.__name__ == 'HTTPError' and e.response.status_code == 404:
				break

			retries += 1
			print('Retry: {} for {}'.format(retries, doi))

			time.sleep(10)
		
		time.sleep(0.05)

	return record

def search_title_author(title, author = None, doi = None):
	if title.strip() != '':
		retries = 0

		while retries < 5:
			try:
				if author is not None:
					result = cr.works(query_title = title, query_author = author, limit = 10)
				else:
					result = cr.works(query_title = title, limit = 10)
				
				break
			except Exception as e:
				print(e)
				result = { 'error' : str(e), 'query_title' :  title, 'query_author' : author }

				retries += 1

				if retries == 1:
					print('Error for DOI {}'.format(doi))
				
				print('Retry #{}'.format(retries))

				time.sleep(5)
		
		time.sleep(0.05)

		result['DOI'] = doi
	else:
		print('Error for DOI {} : empty title'.format(doi))
		result = { 'error' : 'Empty title', 'DOI' : doi }

	return result