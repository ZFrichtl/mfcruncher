# NOTE: This script processed MONTHLY listing from mfpull.py scripts
#       This script is hard-coded to evaluate previous 3-month change

import os
import glob
import fileinput

class FundInfo:
    def __init__(self, fundFilename):
        (head, tail) = os.path.split(fundFilename)
        fundName = tail.split('.')[0]
        fundName = fundName.split('_')[1]
        fundName = fundName.upper()
        self.fundName = fundName
        self.history = None

        self.monthly = []
        isFirst = True
        limit = 0
        for line in fileinput.input(fundFilename):
            limit += 1
            #if limit == 200:
            #    break
            if isFirst: # skip first line, column headers
                isFirst = False
                continue 
            parts = line.split(',')
            self.monthly.append( (parts[0], float(parts[-1]) ) )

        fileinput.close()


pastMonths = 3 # number of months price change to compare

allFunds = []

for infile in glob.glob( os.path.join('', 'zz_*.csv') ):
    print 'Reading', infile, '...'
    allFunds.append( FundInfo(infile) )

performance = []

for fund in allFunds:
    print 'Fund: %s, '%(fund.fundName),
    print 'Price: %s,'%(fund.monthly[0][1]),
    endPrice = float(fund.monthly[0][1])
    startPrice = float(fund.monthly[pastMonths][1])
    delta = (endPrice - startPrice) / startPrice
    print '%d Month Change: %0.2f%%'%(pastMonths, 100*delta)
    performance.append( (delta, fund.fundName) )

performance.sort()
performance.reverse()

print '%d-Month Winner: %s, %0.2f%%'%(pastMonths,
        performance[0][1], 100*performance[0][0])




