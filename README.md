# Obfuscate Family Tree Xls
Obfuscating family tree xls is useful if you we like to hand over your family tree database to e.g. data science task but would like to keep privacy. A data science task might be to predict living status (living or deceased).

Excel is one input format of the free, open source family tree software available at http://freshmeat.sourceforge.net/projects/familytree_cgi/ . The expected columns are descried in the documentation and copied below as reference.

#Usage of the script.
Run

```python obfuscateXls.py --h```

to learn about the script parameters

## Input format
### Excel

Expected excel format as per readme.txt of project [familytree](http://freshmeat.sourceforge.net/projects/familytree_cgi/):

The excel format is quite straightforward based on the example file. Each row (except the header) represents a person. The fields are:
 * ID: the ID of the person. It can be anything (like 123 or Bart_Simpson), but it should only contain alphanumeric characters and underscore (no whitespace is allowed).
 * title: like: Dr., Prof.
 * prefix: like: sir
 * first name
 * middle name 
 * last Name
 * suffix: like: VIII
 * nickname
 * father's ID
 * mother's ID
 * email
 * webpage
 * date of birth: the format is day/month/year, like: 24/3/1977
 * date of death: the format is day/month/year, like: 24/3/1977
 * gender: 0 for male, 1 female
 * is living?: 0 for live 1 for dead
 * place of birth: the format is: "country" "city". The city part may be omitted. Quotation marks are mandatory.
 * place of death: the format is: "country" "city". The city part may be omitted. Quotation marks are mandatory.

Note, that the extension of an excel data file must be xls.

Tip: Select the second row, click on menu Window and select Freeze Panels.
This will freeze the first row and you can see the title of columns.
