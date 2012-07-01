import urllib
import re
import sys
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import fund

engine = sqlalchemy.create_engine('sqlite:///funds.sqlite', echo=True)
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

dbFunds = []

baseUrl = 'http://fundresearch.fidelity.com/mutual-funds/'

url = urllib.urlopen(baseUrl + 'fund-families-no-transaction-fee')

page = url.read()
url.close()

symbols  = []
fundpicks = []

familyLinks = re.findall(r'"funds-by-family\?family=\w+"',page)
familyLinks = [x[1:len(x)-1] for x in familyLinks]

for family in familyLinks:
    sys.stderr.write('\nFamily: %s\n' % family)
    url = urllib.urlopen(baseUrl + family)
    page = url.read()
    url.close()
	
    fundLinks = re.findall(r'"summary/\w+"', page)
    fundLinks = [x[1:len(x)-1] for x in fundLinks]
    
    for fundlink in fundLinks:

        url = urllib.urlopen(baseUrl + fundlink)
        page = url.read()
        url.close()

        symbol = re.search(r'SECURITY_ID=\w+&', page)
        if symbol is None:
            continue
        symbol = symbol.group()
        symbol = symbol[12:len(symbol)-1]
        sys.stderr.write('Fund: %s\n' % symbol)

        #need to add name
        dbFund = fund.Fund(symbol, '')
        dbFund.FundDataSources.append(fund.FundDataSource(baseUrl + fundlink))
   
        ntf = re.search(r'ntf.gif',page)
        if ntf is None:
            sys.stderr.write('Not NTF\n')
            continue

        closed = re.search(r'closed to new', page)
        if closed is not None:
            sys.stderr.write('Closed to new investors\n')
            continue

     
        fpa = re.search(r'Fidelity Portfolio Advisor',page)
        if fpa is not None:
            sys.stderr.wite('Throwing out Fidelity Portfolio Advisor\n')
        
  
        ffp = re.search(r'fund_pick.gif',page)
        if ffp is not None:
            fundpicks.append(symbol)
        
        print '%s,' % symbol
        symbols.append(symbol)

        session.add(dbFund)
        fund.FundTable(session).add(dbFund)
session.commit()
session.close()

print '\nfundpicks = '
print fundpicks

print '\ntf = '
print symbols
