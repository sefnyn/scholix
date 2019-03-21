#Process DRO DOIs with positive links to research data

import fileinput
import json
import requests

def make_data_citation():
     for index in range(len(pub_list)):
        pub_names = pub_list[index]['name'] + ' ; '
     for thingey in range(len(creator_list)):
        creators = creator_list[thingey]['Name'] + ' ; '
    bib.write(creators + pub_date + ':  ' + title + pub_names + '  DOI: http://doi.org' + data_doi + '\n')
    
    
def main():
    DURHAM_DATACITE_PREFIX = '10.15128'
    API = 'http://api.scholexplorer.openaire.eu/v2/Links'
    data = 'records.json'
    links = 'links.tsv'
    citations = 'citations.txt'
    mydata = {} #dict where key is dro_doi and value is json record describing research data
    myscheme = {}
    mydict = {}
    
    print('opening file for JSON records: ' + data)
    g = open(data, 'a')
    fh = open(links, 'w')
    bib = open(citations,  'w')
    
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
                        pub_date = source['PublicationDate'][0:3] #just want the pub year
                        pub_list = source['Publisher']
                        title = source['Title']
                        type = source['Type']
                        creator_list = source['Creator'] #list of creators
                        idict = source['Identifier']
                        for id in idict:
                            data_doi = id['ID']
                            if data_doi.startswith(DURHAM_DATACITE_PREFIX):
                                #Looks like this link points to DRO-DATA; ignore it........
                                print('Ignoring link to DRO-DATA')
                                mydict[data_doi] = '************** DURHAM DATA REPOSITORY *****************'
                                mylist=[]
                            else:
                                #process id
                                scheme = id['IDScheme']
                                found = 0
                                if scheme == 'doi':
                                    for d in mylist:
                                        #no dups allowed
                                        if d == data_doi:
                                            found = 1
                                    if found == 0:		
                                        mylist.append(data_doi)
                                        make_data_citation()
                                else:
                                    try:
                                        val = myscheme[scheme]
                                        val += 1
                                        myscheme[scheme] = val
                                    except KeyError:
                                        myscheme[scheme] = 1
                mystr = ""
                if len(mylist) > 0:
                    for d in mylist:
                        mystr += d + '\t'
                    mydict[dro_doi.rstrip()] = mystr.rstrip()
            except ValueError:
                print('invalid JSON')
    for doi in mydict:
        fh.write(doi + '\t' + mydict[doi] + '\n')
    fh.close()
    
    print('Dictionary: ')
    print(mydict)
    print('Schemes: ')
    print(myscheme)
    
if __name__ == "__main__":
	main()
