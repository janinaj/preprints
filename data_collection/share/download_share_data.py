import requests, json, configparser

config = configparser.ConfigParser()
config.read('sample-config.txt')

search_param = []
for key in config['FILTER']:
	if config['FILTER'][key] != '':
		if 'date' in key:
			search_param.append({ "range": { key: {
						"gte": config['FILTER'][key] + "||/y",
						"lte": config['FILTER'][key] + "||/y"
					}
				}} )
		else:
			search_param.append({ "term" : { key : config['FILTER'][key]}})


headers = {
    'Content-Type': 'application/json',
}
data = {"size": 10000, "query": { "bool" : { "must": { "query_string": { "query": "*" } }, "filter": search_param }}}

# REMOVE: aggregation does not work on text data
# if 'AGGREGATE' in config:
# 	if config['AGGREGATE']['aggregrate'] != '':
# 		data['aggs'] = { "agg" : { "terms" : { "field" : config['AGGREGATE']['aggregrate'] } } }

print(data)
response = requests.post('https://share.osf.io/api/v2/search/creativeworks/_search', headers=headers, data=json.dumps(data))

data = json.loads(response.content)

with open(config['OUTPUT']['filename'], 'w') as f:
	json.dump(data, f)



