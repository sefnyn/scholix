#Query Scholix API
#
#Example query:
#curl -X GET --header 'Accept: application/json' 'http://api.scholexplorer.openaire.eu/v2/Links/?targetPid=10.1109%2FICIP.2015.7351744'
#
import fileinput
import json
import requests

API = 'http://api.scholexplorer.openaire.eu/v2/Links'
out = 'records.json'
hits = 'hits'
success = 0
no_link = 0
found = []
links = {} #dict where key is dro-doi and value is json record describing research data
count = 0

print('opening output file ' + out)
g = open(out, 'w')
fh = open(hits, 'w')

for doi in fileinput.input():
    count += 1
    print("################  " + str(count) + "  #################")
    if not doi.strip():
        #do nothing
        print('found empty line...ignored')
        break
    payload = {'targetPid': doi.rstrip()}
    r = requests.get(API, params=payload)
    if r.raise_for_status() == None:
        print('URL: ' + r.url)
        print('Status: ')
        print(r.status_code)
        print('Headers: ')
        print(r.headers)
        print('Encoding: ')
        print(r.encoding)
        try:
            data = r.json()
            res = data['result']
            if len(res) > 0:
                #print(res)
                success += 1
                fh.write(doi)
            else:
                print('Did not find any research data for doi ' + doi)
                no_link += 1
        except ValueError:
            print('Invalid JSON')
"""     json_string = json.dumps(r.json())
        print(json_string)
        print('\n')
"""
fh.close()
print('Total DOIs in sample ' + str(success + no_link))
print('Links found ' + str(success))
print('Did not find a link ' + str(no_link))
