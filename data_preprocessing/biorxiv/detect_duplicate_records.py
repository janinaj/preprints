import os, json, itertools, csv, sys
import multiprocessing as mp
from fuzzywuzzy import fuzz

sys.path.append(os.path.join('..', '..', 'util'))
import util

def get_ratio(records):
	record_1, record_2 = records
	return record_1, record_2, fuzz.ratio(record_1['normalized_title'], record_2['normalized_title'])

def get_author_sim(record_1, record_2):
	same_first_author_surname = None
	if len(record_1['authors']) > 0 and len(record_2['authors']) > 0:
		same_first_author_surname = (record_1['author_surnames'][0] == record_2['author_surnames'][0])
	
	same_author_surnames = 0
	same_author_names = 0
	for i in range(len(record_1['authors'])):
		for j in range(len(record_2['authors'])):
			if i < len(record_1['author_surnames']) and j < len(record_2['author_surnames']) and \
				record_1['author_surnames'][i] == record_2['author_surnames'][j]:
				same_author_surnames += 1
				
			if i < len(record_1['author_names']) and j < len(record_2['author_names']) and \
				record_1['author_names'][i] == record_2['author_names'][j]:
				same_author_names += 1
				
	return same_first_author_surname, same_author_surnames, same_author_names

# read biorxiv records
BIORXIV_FILE = os.path.join('..', '..', '..', 'raw_data', 'biorxiv', 'biorxiv_records.json')

biorxiv_records = []
with open(BIORXIV_FILE) as f:
	for line in f:
		data = json.loads(line)
		
		try:
			posted_date = data['posted']['date-parts'][0]
		except:
			posted_date = None
			
		if 'relation' in data and 'is-preprint-of' in data['relation']:
			publication_doi = data['relation']['is-preprint-of'][0]['id']
		else:
			publication_doi = None
			
		if 'group-title' in data:
			subject = data['group-title']
		else:
			subject = None
		
		authors = []
		author_names = []
		author_surnames = []
		
		if 'author' in data:
			for author in data['author']:
				for key in author.keys():
					if key in ['family', 'given', 'suffix', 'name']:
						author[key] = util.normalize_str(author[key])
				
				author_name = ''
				if 'given' in author:
					author_name = author['given']
				
				if 'family' in author:
					author_name = author_name + ' ' + author['family']
					author_surnames.append(author['family'])
					
				if 'suffix' in author:
					author_name = author_name + ' ' + author['suffix']

				# it seems that if name is present, there are no other name fields (e.g. given, family)
				if 'name' in author:
					author_name = author_name + ' ' + author['name']
					author_surnames.append(author['name'])

				authors.append(author)
				author_names.append(author_name.strip())

		title = ''
		for t in data['title']:
			title += t + ' '
		title = title.strip()
		
		row = {
			'id' : data['DOI'],
			'title' : title,
			'normalized_title' : util.normalize_str(title),
			'posted_date' : posted_date,
			'publication_doi' : publication_doi,
			'subject' : subject,
			'authors' : authors,
			'author_names' : author_names,
			'author_surnames' : author_surnames,
			'total_authors' : len(authors),
		}
		
		biorxiv_records.append(row)

# perform duplicate detection
THRESHOLD = 50

OUTPUT_FILE = os.path.join('..', '..', '..', 'raw_data', 'biorxiv', 'biorxiv_possible_duplicates.csv')

pairs_processed = 0
with open(OUTPUT_FILE, 'w') as o:
	writer = csv.DictWriter(o, fieldnames = ['id_1',
		'id_2',
		'title_1',
		'title_2',
		'posted_date_1',
		'posted_date_2',
		'authors_1',
		'authors_2',
		'num_authors_1',
		'num_authors_2',
		'same_first_author_surname',
		'same_author_surnames',
		'same_author_names',
		'same_publication_doi',
		'title similarity'])
	writer.writeheader()

	with mp.Pool() as pool:
		for record_1, record_2, ratio in pool.imap_unordered(get_ratio, itertools.combinations(biorxiv_records, 2)):
			pairs_processed += 1
			if pairs_processed % 1000 == 0:
				print('Pairs processed: {}'.format(pairs_processed))

			if ratio >= THRESHOLD:
				same_publication_doi = None
				if record_1['publication_doi'] is not None and record_2['publication_doi'] is not None:
					same_publication_doi = (record_1['publication_doi'] == record_2['publication_doi'])
				
				same_first_author_surname, same_author_surnames, same_author_names = get_author_sim(record_1, record_2)
				
				writer.writerow({
					'id_1' : record_1['id'],
					'id_2' : record_2['id'],
					'title_1' : record_1['normalized_title'],
					'title_2' : record_2['normalized_title'],
					'posted_date_1' : record_1['posted_date'],
					'posted_date_2' : record_2['posted_date'],
					'authors_1' : record_1['author_names'],
					'authors_2' : record_2['author_names'],
					'num_authors_1' : len(record_1['authors']),
					'num_authors_2' : len(record_2['authors']),
					'same_first_author_surname' : same_first_author_surname,
					'same_author_surnames' : same_author_surnames,
					'same_author_names' : same_author_names,
					'same_publication_doi' : same_publication_doi,
					'title similarity' : ratio
				})

				o.flush()