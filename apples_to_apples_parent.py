import requests
from lxml import html
from tabulate import tabulate
from utilityRecord import UtilityRecord

response = requests.get("http://www.energychoice.ohio.gov/ApplesToApplesComparision.aspx?Category=NaturalGas&TerritoryId=8&RateCode=1")
tree = html.fromstring(response.content)

tbody = tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody')

suppliers = tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[2]/span/text()')
rates = list(map(str.strip, tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[3]/text()')))
rateTypes = list(filter( lambda x: len(x) > 0, list(map(str.strip, tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[4]/text()')))))
introPrices = list(filter(lambda x: x == 'Yes' or x == 'No', tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[6]/p/text()')))
termLengths = list(map(str.strip, tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[7]/text()')))
earlyTermFees = list(map(str.strip, tree.xpath('(//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[8]/p | //*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[8][not(p)])/text()')))
monthlyFees = list(map(str.strip, tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[9]/text()')))

records = []
for i in range(0, len(suppliers) - 1):
    newUtilityRecord = UtilityRecord(suppliers[i], rates[i], rateTypes[i], introPrices[i], termLengths[i], earlyTermFees[i], monthlyFees[i])
    records.append(newUtilityRecord)

print('debug breakpoint')

currentUtilityContract = UtilityRecord('Santanna Energy Services', '0.355700', 'Fixed', 'No', '6 mo.', 'No', '$0')

print('Checking for rates better than or comparable to current rate:')
print(tabulate([currentUtilityContract.getTabulateFormatted()], headers=currentUtilityContract.getTableHeaders()))

goodDeals = []

for record in records:
    if record.rate <= currentUtilityContract.rate and record.monthlyFee == '$0' and record.rateType == 'Fixed':
        # if (len(goodDeals) == 0):
        #     print('Good deals found!')
        #record.print()
        goodDeals.append(record)
print()
if len(goodDeals) > 0:
    print('Found {0} good deals!'.format(len(goodDeals)))
    goodDeals.sort(key=lambda x: x.rate)
    print(tabulate((record.getTabulateFormatted() for record in goodDeals), headers=currentUtilityContract.getTableHeaders()))
else:
    print('Didn\'t find any good deals!')

