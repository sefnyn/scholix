#Process research output DOIs with positive links to research data

import fileinput
import json
import requests

DATACITE_PREFIX = '10.15128'  #DURHAM prefix
LOCAL_REPO = '******* DURHAM DATA REPOSITORY *******  ' 
API = 'http://api.scholexplorer.openaire.eu/v2/Links'


def process_result(my_result, doi, doi_links, bib, log):
    """ Returns a list of research data DOIs linked with exactly one research output DOI.

    """
    dois_found = []
    if len(my_result) == 0:
        log.write("........did not find research data for research ouput DOI")
    else:
        #process data
        for link in my_result:
            source = link['source']
            target = link['target'] #to get pub date
            pub_date = target['PublicationDate']
            if pub_date == None: 
                pub_date == ""
            elif pub_date == "":
                pass
            else:
                pub_date = pub_date[0:4] #just want the pub year
            pub_list = source['Publisher'] #list of pubs
            pub_names = ""
            for index in range(len(pub_list)):
                pub_names = pub_names + pub_list[index]['name'] + ' ; '
            title = source['Title']
            mat_type = source['Type']
            creator_list = source['Creator'] #list of creators
            idict = source['Identifier']
            for id in idict:
                data_doi = id['ID']
                if data_doi.startswith(DATACITE_PREFIX):
                    #Looks like this link points to local data repository; ignore it........
                    print('Ignoring link to local data repository')
                    log.write("........Ignoring link to local data repository")
                    doi_links[doi] = LOCAL_REPO + data_doi
                    mylist = []
                else:
                    #process id
                    scheme = id['IDScheme']
                    found = 0
                    if scheme == 'doi':
                        for d in dois_found:
                            #no dups allowed
                            if d == data_doi:
                                found = 1
                        if found == 0:		
                            dois_found.append(data_doi)
                            bib_rec = make_data_citation(creator_list, pub_date, title, pub_names, mat_type, data_doi)
                            print(bib_rec)
                            bib.write(bib_rec.encode('utf-8') + '\n\n')
                            log.write("........success!")
        return dois_found

def make_data_citation(creator_list, pub_year, title, pub_names, mat_type, doi):
    """ Returns one data citation of type str.  The citation is in DataCite format except material type enclosed in square brackets instead of parentheses.
            Creator01 ; Creator02 ; Creator03 ... (Pub year):  Title.  Publisher01 ; Publisher02 ....  [material type]  DOI: http://doi.org/...
    """
    creators = ""
    for index in range(len(creator_list)):
        creators = creators + creator_list[index]['Name'] + ' ; '
    if pub_year == "":
        pub_year = "n.d."
    ret_string = creators[:-3] + "  (" + str(pub_year) + "):  " + title + ".  " + pub_names[:-3] + ".  [" + mat_type + "]  DOI: http://doi.org/" + doi
    return ret_string
    
def main():
    data = 'records.json'
    links = 'links.tsv'
    citations = 'citations.txt'
    logfile = 'logfile.log'
    doi_links = {}
    count = 0
  
    print('opening file for JSON records: ' + data)
    j = open(data, 'w')
    tsv = open(links, 'w')
    bib = open(citations,  'w')
    log = open(logfile, 'w')
    
    for doi in fileinput.input():
        doi = doi.rstrip()
        count += 1
        print("##########......##########\n##########  " + str(count ) + "  ##########\n##########......##########\n")
        if not doi:
            #do nothing
            print('found empty line...ignored')
            break
        payload = {'targetPid': doi}
        r = requests.get(API, params=payload)
        if r.raise_for_status() == None:
            print('Processing doi ' + doi)
            log.write('Processing doi ' + doi)
            try:
                json_data = r.json()
            except ValueError:
                print('Invalid JSON')
                log.write("........Invalid JSON")
            else:
                json_string = json.dumps(json_data, indent=4)
                j.write(json_string)
                my_result = json_data['result']
                my_data_dois = process_result(my_result, doi, doi_links, bib, log)
                mystr = ""
                if len(my_data_dois) > 0:
                    for d in my_data_dois:
                        mystr += d + '\t'
                    doi_links[doi] = mystr.rstrip()
            log.write("\n")
    for doi in doi_links:
        tsv.write(doi + '\t' + doi_links[doi] + '\n')
    tsv.close()
    
    print('Dictionary: ')
    print(doi_links)
    
if __name__ == "__main__":
	main()
