import urllib
symbols = [ 'fftyx', 'aapl' ]

for symbol in symbols:
    symbolUrl = 'http://ichart.finance.yahoo.com/table.csv?s='+symbol+'&g=m&ignore=.csv'
    urllib.urlretrieve(symbolUrl, 'zz_'+symbol+'.csv')
