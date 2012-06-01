import urllib

symbols = [ 'FSTBX', 'FDBAX', 'FEDEX', 'VSFAX', 'FGSSX', 'RIMAX',
        'FGFAX', 'ISCAX', 'KAUAX', 'FKASX', 'FMXSX', 'QAACX',
        'QALGX', 'FSTKX', 'BEARX', 'SVAAX', 'FTRFX', 'FIGIX' ]

for symbol in symbols:
    symbolUrl = 'http://ichart.finance.yahoo.com/table.csv?s='+symbol+'&g=m&ignore=.csv'
    urllib.urlretrieve(symbolUrl, 'zz_'+symbol+'.csv')
