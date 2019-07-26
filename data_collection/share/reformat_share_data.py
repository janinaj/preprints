# THIS CODE TRANFORMS THE SHARE DATA DUMP INTO A JSON FILE WITH ONE RECORD PER LINE

import json, ijson, os

# contains the number of records
count = 0

# name of the output file / folder
share = 'share-jan-2019'

# make sure the file is empty
# warning: it will replace the file if it already exists
open(os.path.join('..', '..', 'data', + '.json'), 'w').close() 

with open(os.path.join('..', '..', 'raw_data', 'asapbio.json'), 'r') as f:
	with open(os.path.join(share + '.json'), 'a') as o:
		for item in ijson.items(f, "item"):
			count += 1

			json.dump(item['_source'], o)
			o.write('\n')

			# uncomment these lines if you want to generate a single file for each record
			# with open(os.path.join(share, item['_source']['id'] + '.json'), 'w') as o:
			# 	json.dump(item['_source'], o)

print('Total number of records: {}'.format(count))
