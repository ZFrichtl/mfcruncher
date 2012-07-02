import urllib
import os.path
import datetime
import fund


def pullSymbols(symbols, destPath = '', granularity = 'm'):
    if granularity != 'm': # default to monthly
        granularity = 'd' # otherwise, get daily prices
        
    for symbol in symbols:
        path = os.path.join(destPath,'zz_' + symbol + '.csv')
        symbolUrl = 'http://ichart.finance.yahoo.com/table.csv'
        symbolUrl += '?s='+symbol+'&g=%s&ignore=.csv'%(granularity)
        urllib.urlretrieve(symbolUrl, path)

def pullHistoricalData(funds):
    for f in funds:
        symbolUrl = 'http://ichart.finance.yahoo.com/table.csv'
        symbolUrl += '?s='+f.symbol+'&g=d&ignore=.csv'

        url = urllib.urlopen(symbolUrl)
        lines = url.readlines()
        url.close()

        for line in lines[1:]:
            datecode = line.split(',')[0]
            date = datetime.datetime.strptime(datecode,'%Y-%m-%d')

            price = float(line.split(',')[-1].strip())
            f.HistoricalPrices.append(fund.HistoricalPrice(date,price))
    

if __name__ == '__main__':
    paychex  = [ 'FSTBX', 'FDBAX', 'FEDEX', 'VSFAX', 'FGSSX', 'RIMAX',
                 'FGFAX', 'ISCAX', 'KAUAX', 'FKASX', 'FMXSX', 'QAACX',
                 'QALGX', 'FSTKX', 'BEARX', 'SVAAX', 'FTRFX', 'FIGIX' ]
    
    pullSymbols(paychex)
