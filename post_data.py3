#Post JSON data to data repository

"""
This implementation has been tested on Sufia/Hydra v.6.3.0:
(1) Sufia/Hydra API modified to accept JSON data without depositing research data
(2) Sufia/Hydra API modified to allow HTTP basic authentication by repository admin users only

What this script does:

For each research paper DOI, create one deposit record in the local data repository.
The record will contain all research data DOIs associated with the research paper.


Create record in test repo using curl command:

curl -X POST -H "Content-type: application/json" -u <USERNAME > --insecure -d file.json <SERVER>
"""

JSON_TEMPLATE = {
  "create_api": "true",
  "visibility": "restricted",
  "generic_file": {
    "title": [
    ],
    "abstract": [
    ],
    "tag": [
    ],
    "related_url": [
    ],
    "resource_type": [
    ],
    "contributors_attributes": [
      {
        "contributor_name": [
          "Research Data Manager"
        ],
        "affiliation": [
          "Durham University"
        ],
        "role": [
          "http://id.loc.gov/vocabulary/relators/cre"
        ]
      }
    ],
    "description": [
    ],
    "identifier": [
    ],
    "publisher": [
    ],
    "date_created": [
    ]
  }
}

AUTHOR_TEMPLATE = {
    "contributor_name": [
    ],
    "affiliation": [
    ],
    "role": [
    ]
}

#import pdb
import sys
import copy
import fileinput
import json
import requests
import getpass #hides password of admin user
from requests.auth import HTTPBasicAuth


DATACITE_PREFIX = '10.15128'  #DURHAM prefix
LOCAL_REPO = '******* DURHAM DATA REPOSITORY *******  ' 
API = 'http://api.scholexplorer.openaire.eu/v2/Links'
HTTPBIN_POST_METHOD = 'https://httpbin.org/post'
TEST_POST_METHOD = 'https://collections-test.durham.ac.uk/files'
LIVE_POST_METHOD = 'https://collections.durham.ac.uk/files'
RESOURCE_TYPE = 'Dataset'
DEPOSIT_DESCRIPTION = 'The University does not hold this research data.  According to the Scholix OpenAIRE API, the research data associated with this research is located in one or more other repositories.  Follow the DOI links to get the research data.'
CURRENT_POST_METHOD = TEST_POST_METHOD

class CancelledError(Exception): pass

def post_result(my_result, doi, username, pwd, log):
    """ Trys to post JSON data to server

    """
    if len(my_result) == 0:
        log.write("........did not find research data for research ouput DOI")
    else:
        #process data
        dois_found = []
        for link in my_result:
            json_data = copy.deepcopy(JSON_TEMPLATE)
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
            title = target['Title']
            mat_type = source['Type']
            creator_list = source['Creator'] #list of creators
            idict = source['Identifier']
            for id in idict:
                data_doi = id['ID']
                if data_doi.startswith(DATACITE_PREFIX):
                    #Looks like this link points to local data repository; ignore it........
                    print('Ignoring link to local data repository')
                    log.write("........Ignoring link to local data repository")
                    #doi_links[doi] = LOCAL_REPO + data_doi
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
        if len(dois_found) > 0:
            gen_file = json_data['generic_file']
            title = title + " [dataset]"
            gen_file['title'].append(title)
            if len(creator_list) > 0:
                for index in range(len(creator_list)):
                    author = copy.deepcopy(AUTHOR_TEMPLATE)
                    author['contributor_name'].append(creator_list[index]['Name'])
                    author['affiliation'].append("University X")   #bug fix
                    author['role'].append('http://id.loc.gov/vocabulary/relators/cre')
                    gen_file['contributors_attributes'].append(author)
            gen_file['resource_type'].append(RESOURCE_TYPE)
            gen_file['description'].append(DEPOSIT_DESCRIPTION)
            gen_file['related_url'].append("http://doi.org/" + doi)
            for data_doi in dois_found:
                gen_file['identifier'].append("http://doi.org/" + data_doi)
            gen_file['publisher'].append(pub_names[:-3])
            gen_file['date_created'].append(pub_date)

#######################################################################################################################
#                pdb.set_trace()
#######################################################################################################################

            r = requests.post(CURRENT_POST_METHOD, verify=False, json=json_data, auth=HTTPBasicAuth(username, pwd))
#        print('FAKE posting data')
#        json_string = json.dumps(json_data, indent=4)
#        print(json_string)
            return r
        else:
            sys.exit('No data DOIs found for this research paper DOI')

def post():
    logfile = 'logfile_post_data.log'
    doi_links = {}
    count = 0

    j = open('data.json', 'w')  
    log = open(logfile, 'w')

    username = input("Enter CIS username: ")
    if not username:
        raise CancelledError()
    pwd = getpass.getpass(prompt="Enter password (N.B.: you will *not* see any input as you type): ", stream=None)
    if not pwd:
        raise CancelledError()
    
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
                response = post_result(my_result, doi, username, pwd, log)
                print('Response from ' + CURRENT_POST_METHOD)
                try:
                    who_shot_jr = response.json()
                    if who_shot_jr['status'] == 'ok':
                        log.write('... ... ... ok posting data')
                        print('ok posting data')
                    else:
                        log.write('... ... ... FAILED posting data')
                        print(who_shot_jr['status'])
                        sys.exit('Failed to post data')
                except ValueError:
                    log.write('No JSON data returned...check your credentials...')
                    sys.exit('No JSON data returned...check your credentials...')
            log.write("\n")
    
if __name__ == "__main__":
	post()
