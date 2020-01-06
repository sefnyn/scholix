# Find links between research outputs and research data in other data repositories

## Requirements
You must install the 3rd party module: requests  
Full details: http://python-requests.org/

You will need a list of DOIs for research papers from your institutional repository.
This list is the input file for the *Query* script.


## Query Scholix API script: **query.py**
The script takes one command line parameter; namely, a file containing DOIs from the repository containing research outputs.

The script makes one API call for every DOI in the input file.  If the API finds corresponding research data for the DOI then it writes the DOI to the output file.

Execute script
> python query.py testDOI.csv

Output file: **hits**  
10.1039/c8ra01257a  
10.1107/S1600536804011663  
10.1163/22134808-20191324



## Make citations: **mk_citations.py**
Like query.py, this script makes one API call for every DOI in the input file.

Execute script
> python mk_citations.py hits

The script creates several output files:
- links.tsv
- citations.txt
- records.json
- logfile.log

Output file: **links.tsv**
File format is:  
*DOI\tDATA-DOI\tDATA-DOI\tDATA-DOI...* where \t represents a tab character

This file includes data DOIs pointing to the local research data repository and are included for completeness.  For example:  
10.1021/ol801121p	10.5517/ccqt7yp	10.5517/ccqt7wm	10.5517/ccqt7xn  
10.1016/j.compstruc.2017.05.004	******* DURHAM DATA REPOSITORY *******  10.15128/r1n870zq804  
10.1186/s40814-016-0053-3	10.6084/m9.figshare.c.3610439_d1	10.6084/m9.figshare.c.3610439_d1.v1

Remove lines containing DURHAM DATA REPOSITORY:
>grep -v DURHAM links.tsv > linksWithoutDurham.tsv

Output file: **citations.txt**  [lines appear to wrap here but do not wrap in the file]
>Šibalić, N.  (2017):  ARC: An open-source library for calculating properties of alkali Rydberg atoms.  Mendeley.  [dataset]  DOI: http://doi.org/10.17632/hm5n8w628c.1  
>
>Addison, John T. ; Teixeira, Paulino  (2019):  Workplace Employee Representation and Industrial Relations Performance ‘(replication data)’..  ZBW - Leibniz Informationszentrum Wirtschaft.  [dataset]  DOI: http://doi.org/10.15456/jbnst.2018197.152711  
>
>Aguilar, Juan A. ; Gimenez, Diana ; Bromley, Elizabeth H. C. ; Cobb, Steven L.  (2018):  CCDC 1567327: Experimental Crystal Structure Determination.  Cambridge Crystallographic Data Centre.  [dataset]  DOI: http://doi.org/10.5517/ccdc.csd.cc1plxy4


Output file: **logfile.log**  
Processing doi 10.1680/jgele.17.00081........Ignoring link to local data repoository  
Processing doi 10.1186/s40814-016-0053-3........success!........success!........success!  
Processing doi 10.1002/anie.201309680........success!


## Post data: post_data.py
The script illustrates how you might post JSON data to a repository API.  This particular script is designed to call a Sufia/Hydra API only.

The Sufia/Hydra API has been customised in two ways:
1. The API accepts JSON data without depositing a research dataset
2. The API allows HTTP basic authentication by repository admin users only

### What this script does:
For each research paper DOI, create one deposit record in the local data repository.  The record will contain all research data DOIs associated with the research paper.

The script has been successfuly tested with Sufia/Hydra v.6.3.0.

Execute the script:
> python2 post_data.py2 hits.out  
>  
> Enter CIS username: pzvx49  
> Enter password (N.B.: you will *not* see any input as you type):   
>  
> ##########......##########  
> #########  1  ##########  
> #########......##########  
>  
>  Processing doi 10.1111/ecog.02712  
>  /usr/local/lib/python2.7/dist-packages/urllib3/connectionpool.py:851: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings InsecureRequestWarning)  
>  
>  Response from https://collections-test.durham.ac.uk/files  
>  ok posting data  

