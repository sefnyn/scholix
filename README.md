# Find links between Durham research outputs and Durham research data

## History
The list of DRO DOIs was created by Heather on 14/3/2019.
This list is the input file.


## Query Scholix API script: query.py2
The script takes one command line parameter; namely, a file containing DRO DOIs.

The script makes one API call for every DOI in the input file.  If the API finds corresponding research data for the DOI then it writes the DOI to the output file.

Execute script
> python query.py2 test.csv

Output file: hits
10.1039/c8ra01257a
10.1107/S1600536804011663
10.1163/22134808-20191324


## Process hits: pro_hits.py2


