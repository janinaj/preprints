import sys, os, json

sys.path.append(os.path.join('..', '..', 'util'))
import util

INPUT_FILE = os.path.join('..', '..', '..', 'raw_data', 'biorxiv', 'biorxiv_records.json')
OUTPUT_FILE = os.path.join('..', '..', '..', 'raw_data', 'biorxiv', 'biorxiv_author_disambiguation.json')

author_keys = set()
orcids = {}
with open(INPUT_FILE, 'r') as f:
	for line in f:
		record = json.loads(line)

		if 'author' in record:
			for author in record['author']:

				# 'authenticated-orcid' is always false for biorxiv data
				if 'ORCID' in author and 'authenticated-orcid' in author:
					if author['ORCID'] not in orcids:
						orcids[author['ORCID']] = []
					orcids[author['ORCID']].append(author)
				# for key in author.keys():
				# 	author_keys.add(key)

				# if len(author['affiliation']) > 0:
				# 	print(author['affiliation'])

more_than_1 = 0
for orcid, authors in orcids.items():
	if len(authors) > 1:
		for i in range(1, len(authors)):
			for key in authors[0].keys():
				if authors[0][key] != authors[i][key] and key != 'sequence':
					print(key)
					print(authors[0])
					input(authors[i])


		more_than_1 += 1
print(more_than_1)
print(len(orcids.keys()))
# 		title = ''
# 		for title in record['title']:
# 			title += title + ' '
# 		title = title.strip()

# 		first_author_str = ''
# 		if 'author' in record:
# 			for author in record['author']:
# 				if author['sequence'] == 'first':
# 					if 'given' in author:
# 						first_author_str = author['given']

# 					if 'family' in author:
# 						first_author_str = first_author_str + ' ' + author['family']

# 					if 'suffix' in author:
# 						first_author_str = first_author_str + ' ' + author['suffix']

# 					# it seems that if name is present, there are no other name fields (e.g. given, family)
# 					if 'name' in author:
# 						first_author_str = first_author_str + ' ' + author['name']
# 					break

# 		result = crossref.search_title_author(util.normalize_str(title), 
# 			util.normalize_str(first_author_str),
# 			record['DOI'])

# 		result['id'] = record['DOI']

# 		new_records_processed += 1

# 		json.dump(result, o)
# 		o.write('\n')
# 		o.flush()

# print('Search results for {} records collected.'.format(new_records_processed))