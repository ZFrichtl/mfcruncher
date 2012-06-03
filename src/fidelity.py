import urllib
import re
import sys

baseUrl = 'http://fundresearch.fidelity.com/mutual-funds/'

url = urllib.urlopen(baseUrl + 'fund-families-no-transaction-fee')

page = url.read()

symbols  = []

familyLinks = re.findall(r'"funds-by-family\?family=\w+"',page)
familyLinks = [x[1:len(x)-1] for x in familyLinks]

for family in familyLinks:
    sys.stderr.write('\nFamily: %s\n' % family)
    url = urllib.urlopen(baseUrl + family)
    page = url.read()
	
    fundLinks = re.findall(r'"summary/\w+"', page)
    fundLinks = [x[1:len(x)-1] for x in fundLinks]
    
    for fund in fundLinks:
        url = urllib.urlopen(baseUrl + fund)
        page = url.read()

        symbol = re.search(r'SECURITY_ID=\w+&', page).group()
        symbol = symbol[12:len(symbol)-1]
        sys.stderr.write('Fund: %s\n' % symbol)
        
        symbols.append(symbol) 

print symbols
