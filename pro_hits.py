#Process DRO DOIs with positive links to research data
#
#

import fileinput
import json
import requests
import sys

API = 'http://api.scholexplorer.openaire.eu/v2/Links'
out = 'records.json'
links = 'links.csv'
mydata = {} #dict where key is dro_doi and value is json record describing research data
mydict = {}

print('opening output file ' + out)
g = open(out, 'w')
fh = open(links, 'w')

for dro_doi in fileinput.input():
    if not dro_doi.strip():
        #do nothing
        print('found empty line...ignored')
        break
    payload = {'targetPid': dro_doi.rstrip()}
    r = requests.get(API, params=payload)
    if r.raise_for_status() == None:
        print('************************************ Processing doi ' + dro_doi)
        try:
            data = r.json()
            myres = data['result']
            mylist = []
            if len(myres) == 0:
                raise SystemExit('Did not find research data for doi ' + dro_doi)
            else:
                #process data
                for link in myres:
                    source = link['source']
                    print('Source: ')
                    print(source)
                    ids = source['Identifier']
                    print('Ids: ')
                    print(ids)
                    for idict in ids:
                        data_doi = idict['ID']
                        scheme = idict['IDScheme']
                        if scheme == 'doi':
                            mylist.append(data_doi)
                            print('*********************************')
                            print('******** DATA DOI ********: ' + data_doi)
                            print('*********************************')
            mydict[dro_doi.rstrip()] = mylist
        except ValueError:
            print('invalid JSON')
"""     json_string = json.dumps(r.json())
        print(json_string)
        print('\n')
"""
for d in mydict:
    fh.write(d + '\t' + str(mydict[d]) + '\n')
print(mydict)
