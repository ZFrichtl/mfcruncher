import urllib

baseUrl = 'http://fundresearch.fidelity.com/mutual-funds/'

url = urllib.urlopen(baseUrl + 'fund-families-no-transaction-fee')

page = url.read()

find = 0
oldfind = 0

while (find is not  -1) and oldfind <= find:
    oldfind = find
    find = page.find('funds-by-family', find)

    familyUrl = page[find:page[find:].find('"')+find]

    familyObj = urllib.urlopen(baseUrl + familyUrl)
    familyPage = familyObj.read()
    print familyUrl
    

    familyfind = 0
    oldfamilyfind = 0

    while (familyfind is not  -1) and oldfamilyfind <= familyfind:
        oldfamilyfind = familyfind
        familyfind = familyPage.find('"summary', familyfind)
        familyfind = familyfind+1

        fundUrl = familyPage[familyfind:familyPage[familyfind:].find('"')+familyfind]

        print fundUrl

        familyfind = familyfind+1
    find = find+1
