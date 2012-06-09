import urllib
import os.path


def pullSymbols(symbols, destPath = '', granularity = 'm'):
    if granularity != 'm': # default to monthly
        granularity = 'd' # otherwise, get daily prices
        
    for symbol in symbols:
        path = os.path.join(destPath,'zz_' + symbol + '.csv')
        symbolUrl = 'http://ichart.finance.yahoo.com/table.csv'
        symbolUrl += '?s='+symbol+'&g=%s&ignore=.csv'%(granularity)
        urllib.urlretrieve(symbolUrl, path)

if __name__ == '__main__':
    paychex  = [ 'FSTBX', 'FDBAX', 'FEDEX', 'VSFAX', 'FGSSX', 'RIMAX',
                 'FGFAX', 'ISCAX', 'KAUAX', 'FKASX', 'FMXSX', 'QAACX',
                 'QALGX', 'FSTKX', 'BEARX', 'SVAAX', 'FTRFX', 'FIGIX' ]
    
    pullSymbols(paychex)
