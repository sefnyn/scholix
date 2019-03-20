#Process DRO DOIs with positive links to research data

import fileinput
import json
import requests

DURHAM_DATACITE_PREFIX = '10.15128'
API = 'http://api.scholexplorer.openaire.eu/v2/Links'
data = 'records.json'
links = 'links.tsv'
mydata = {} #dict where key is dro_doi and value is json record describing research data
myscheme = {}
mydict = {}

print('opening file for JSON records: ' + data)
g = open(data, 'a')
fh = open(links, 'w')
fh.write('hello')

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
            json_string = json.dumps(data, indent=4)
            g.write(json_string)
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
                    idict = source['Identifier']
                    pub = source['Publisher']
                    for id in idict:
                        data_doi = id['ID']
                        if data_doi.startswith(DURHAM_DATACITE_PREFIX):
                            #Looks like this link points to DRO-DATA; ignore it........
                            print('Ignoring link to DRO-DATA')
                        else:
                            #process id
                            scheme = id['IDScheme']
                            found = 0
                            if scheme == 'doi':
                                for d in mylist:
                                    if d == data_doi:
                                        found = 1
                                if found == 0:		
                                    mylist.append(data_doi)
                            else:
                                try:
                                    val = myscheme[scheme]
                                    val += 1
                                    myscheme[scheme] = val
                                except KeyError:
                                    myscheme[scheme] = 1
            mystr = ""
            for d in mylist:
                mystr += d + '\t'
            mydict[dro_doi.rstrip()] = mystr.rstrip()
        except ValueError:
            print('invalid JSON')
for doi in mydict:
    fh.write(doi + '\t' + mydict[doi] + '\n')


print('Dictionary: ')
print(mydict)
print('Schemes: ')
print(myscheme)
