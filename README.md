# Find links between research outputs and research data in other data repositories

## History
The list of research output DOIs was created by the Repository Manager on 14/3/2019.
This list is the input file.


## Query Scholix API script: **query.py2**
The script takes one command line parameter; namely, a file containing DOIs from our repository containing research outputs.

The script makes one API call for every DOI in the input file.  If the API finds corresponding research data for the DOI then it writes the DOI to the output file.

Execute script
> python query.py2 testDOI.csv

Output file: **hits**  
10.1039/c8ra01257a  
10.1107/S1600536804011663  
10.1163/22134808-20191324



## Make citations: **mk_citations.py2**
Like query.py2, this script makes one API call for every DOI in the input file.

Execute script
> python mk_citations.py2 hits

The script creates several output files:
- links.tsv
- citations.txt
- records.json
- logfile.log

Output file: **links.tsv**
File format is:  
*DOI\tDATA-DOI\tDATA-DOI\tDATA-DOI...*

This file includes data DOIs pointing to the Durham research data repository and are included for completeness.  For example:  
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


## Post data: post_data.py2

Under development
