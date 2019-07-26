import urllib.request, time, json, string

def download_from_url(url):
	retries = 0
	while retries < 5:
		try:
			with urllib.request.urlopen(url) as response:
				data = json.loads(response.read().decode())

				time.sleep(10)
				
				return 'SUCCESS', data
		except Exception as e:
			if e.code == 401:
				error_message = str(e)
				print('Error processing URL: {}.'.format(contributor_url))
				
				break

			else:
				error_message = str(e)

				time.sleep(1000)

				retries += 1
				print('Retry: {} for {}'.format(retries, record['id']))

	return 'ERROR', error_message

def normalize_str(str_input):
    for punctuation in string.punctuation:
        str_input = str_input.replace(punctuation, ' ')

    str_input.replace('\n', ' ')
        
    while '  ' in str_input:
        str_input = str_input.replace('  ', ' ')
        
    return str_input.strip().lower()