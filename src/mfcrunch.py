import os
import sys
import glob
import fileinput

class FundInfo:
    def __init__(self, fundFilename):
        fundName = fundFilename.split('\\')[-1].split('.')[0]
        fundName = fundName.split('_')[1]
        fundName = fundName.upper()
        self.fundName = fundName
        self.history = None

        self.daily = []
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
            self.daily.append( (parts[0], float(parts[-1]) ) )

        fileinput.close()
        self.daily.reverse()  # order from oldest to newest
        # print self.daily

        self.monthly = []
        isFirst = True
        for entry in self.daily:
            parts = entry[0].split('-')
            year = parts[0]
            month = parts[1]
            if isFirst:
                prevMonth = month
                isFirst = False
                continue
            if month != prevMonth:
                if prevMonth == '12':
                    year = '%d'%(int(year)-1)
                self.monthly.append( ('%s-%s'%(year,prevMonth), entry[1]) )
                prevMonth = month

        #if self.fundName == 'ISCAX':
        #    print self.monthly

        self.nMonthChange = {}

        for n in range(1,7): # record 1-6 months of deltas
            changes = {}
            for i in range(n, len(self.monthly)):
                date = self.monthly[i][0]
                before = self.monthly[i-n][1]
                after = self.monthly[i][1]
                change = (after-before)/before
                #if self.fundName == 'ISCAX':
                #    print '(adding ISCAX hist for %s)'%(date)
                changes[date] = change
            self.nMonthChange[n] = changes

        # print self.nMonthChange

    def getMonthChange(self, date, monthsBack=1):
        if monthsBack not in self.nMonthChange.keys():
            print 'No history available for that big of a delta'
            print 'Change the last loop in the previous method to get more'
            return None
        # print self.nMonthChange[monthsBack].keys()
        if date not in self.nMonthChange[monthsBack].keys():
            print '(%s does not have history for %s)'%(self.fundName, date)
            return None
        return self.nMonthChange[monthsBack][date]

    def getPrice(self, date):
        for item in self.monthly:
            if date == item[0]:
                return item[1] 
        return None

inputFilePath = '..\\testfiles\\'

if len(sys.argv) == 2:
    inputFilePath = sys.argv[1]

allFunds = []

for infile in glob.glob( os.path.join(inputFilePath, 'zz_*.csv') ):
    print 'Reading', infile, '...'
    allFunds.append( FundInfo(infile) )

sp500 = None
for i in range(len(allFunds)):
    if allFunds[i].fundName == "CGSPC":
        sp500 = allFunds[i]
        break


# loop through months chronologically from X date to Y date
# for initial date, find top N funds and split initial amount across them
#     e.g. $10000: buy $5000 of each of the top two funds for N==2
# for each date after the start date:
#     find top N performs among allFunds
#         "top performer" must be defined: e.g. best 3-month performance
#     redistribute investment, sell if necessary

initialAmount = 10000.00
startDate = '2000-01'
endDate     = '2002-06'
maxPastMonths = 3
maxInvestedFunds = 2
fundsToDisplay = 10

# omitFund = []

# build a list of dates to be analyzed
dates = []
results = []

currentDate = startDate

while True:
    dates.append(currentDate)
    
    # increment the date    
    if currentDate == endDate:
        break
    parts = currentDate.split('-')
    year = int(parts[0])
    month = int(parts[1])
    month += 1
    if month > 12:
        year += 1
        month = 1
    currentDate = '%d-%02d'%(year,month)

if sp500 is not None:
    sp500Shares = initialAmount / sp500.getPrice(startDate)
    totalValue = ['S&P 500']
    for currentDate in dates:
        accountValue = sp500Shares * sp500.getPrice(currentDate)
        totalValue.append(accountValue)
    results.append(totalValue)

for pastMonths in range(1, maxPastMonths+1):
    for investedFunds in range( 1, maxInvestedFunds+1):
        totalValue = ['%dm+%df'%(pastMonths,investedFunds)]
        lastTrade = []
        currentAmount = initialAmount
        for currentDate in dates:
            print 'Processing date: %s'%(currentDate)
            monthlyTotals = []
            for i in range(len(allFunds)):
                #if i in omitFund:
                #    continue
                fund = allFunds[i]
                if fund.fundName == "CGSPC": # exclude S&P500
                    continue
                change = fund.getMonthChange(currentDate, pastMonths)
                if change == None:
                    # omitFund.append(i)
                    continue
                monthlyTotals.append( (change, i) )

                fundName = fund.fundName
                sharePrice = fund.getPrice(currentDate)
                print '[%s, $%0.2f,'%(fundName, sharePrice),
                print '%0.2f%%]'%(100*change),
            print
            monthlyTotals.sort()
            monthlyTotals.reverse()

            # cash out
            print 'Selling...'
            if len(lastTrade) == 0:
                currentAmount = initialAmount
            else:
                accountValue = 0
                for trade in lastTrade:
                    index = trade[0]
                    shares = trade[1]
                    sharePrice = allFunds[index].getPrice(currentDate)
                    fundName = allFunds[index].fundName
                    print '%s: %0.2f shares * $%0.2f'%(fundName, shares, sharePrice)
                    accountValue += shares * sharePrice
                currentAmount = accountValue
                lastTrade = []

            print 'Account Value = $%0.2f'%(currentAmount)

            # log date and current amount for csv generation later
            totalValue.append(currentAmount)
            
            amountPerFund = currentAmount / investedFunds
            
            print 'Buying...'
            if len(monthlyTotals) >= investedFunds:
                displayCount = investedFunds
            else:
                displayCount = len(monthlyTotals)
            for j in range(displayCount):
                rate = monthlyTotals[j][0]
                index = monthlyTotals[j][1]
                fundName = allFunds[index].fundName
                sharePrice = allFunds[index].getPrice(currentDate)
                #print '%s $%0.2f: %0.2f%%  '%(fundName, sharePrice, rate*100)
                #print monthlyTotals[:investedFunds]
                #print monthlyTotals
                lastTrade.append( (index, amountPerFund / sharePrice) )
                print '%s: %0.2f shares * $%0.2f'%(fundName, amountPerFund / sharePrice, sharePrice)
            print
        results.append(totalValue)

# Generate csv output
performance = []
i=-1
for totalValue in results:
    i += 1
    if i==0:  # exclude S&P 500
        continue
    performance.append( (totalValue[-1], i) )

performance.sort()
performance.reverse()

dates = ['Date'] + dates

outstr = ''

outstr += 'Date,'
outstr += 'Initial Amt,'

outstr += '%s,'%(results[0][0]) # S&P 500 is first list

limit = fundsToDisplay
for j in range(len(performance)):
    index = performance[j][1]
    totalValue = results[index]
    outstr += '%s,'%(totalValue[0])
    limit -= 1
    if limit == 0:
        break
    
outstr += '\n'

for i in range(1, len(dates)):
    outstr += '%s,'%(dates[i])
    outstr += '%0.0f,'%(initialAmount)

    outstr += '%0.0f,'%(results[0][i]) # S&P 500 is first list

    limit = fundsToDisplay
    for j in range(len(performance)):
        index = performance[j][1]
        totalValue = results[index]
        outstr += '%0.0f,'%(totalValue[i])
        limit -= 1
        if limit == 0:
            break

    outstr += '\n'

print outstr

outfile = open(inputFilePath + 'results.csv','w')
outfile.write(outstr)
outfile.close()


