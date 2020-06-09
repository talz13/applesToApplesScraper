import requests
from lxml import html
from tabulate import tabulate
from utilityRecord import UtilityRecord

response = requests.get("http://www.energychoice.ohio.gov/ApplesToApplesComparision.aspx?Category=NaturalGas&TerritoryId=8&RateCode=1")
tree = html.fromstring(response.content)

tbody = tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody')

xpathTemplate = '//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[{0}]{1}'

suppliers = tree.xpath(xpathTemplate.format('2', '/span/text()'))
rates = list(map(str.strip, tree.xpath(xpathTemplate.format('3', '/text()'))))
rateTypes = list(filter( lambda x: len(x) > 0, list(map(str.strip, tree.xpath(xpathTemplate.format('4', '/text()'))))))
introPrices = list(filter(lambda x: x == 'Yes' or x == 'No', tree.xpath(xpathTemplate.format('6', '/p/text()'))))
termLengths = list(map(str.strip, tree.xpath(xpathTemplate.format('7', '/text()'))))
earlyTermFees = list(map(str.strip, tree.xpath('({0} | {1}'.format(xpathTemplate.format('8', '/p'), xpathTemplate.format('8', '[not(p)])/text()')))))
monthlyFees = list(map(str.strip, tree.xpath(xpathTemplate.format('9', '/text()'))))

#currentUtilityContract = UtilityRecord('Santanna Energy Services', '0.355700', 'Fixed', 'No', '6 mo.', 'No', '$0')
# Contract starting in July 2020? expiring in July 2021?
currentUtilityContract = UtilityRecord('New Wave Energy Corp', '0.295', 'Fixed', 'No', '12 mo.', '$99', '$0')
yearlyUsage = 576

records = []
for i in range(0, len(suppliers) - 1):
    newUtilityRecord = UtilityRecord(suppliers[i], rates[i], rateTypes[i], introPrices[i], termLengths[i], earlyTermFees[i], monthlyFees[i], (float(currentUtilityContract.rate) - float(rates[i])) * yearlyUsage)
    records.append(newUtilityRecord)

print('Checking for rates better than or comparable to current rate:')
print(tabulate([currentUtilityContract.getTabulateFormatted()], headers=currentUtilityContract.getTableHeaders()))

goodDeals = []

for record in records:
    if record.rate <= currentUtilityContract.rate and record.monthlyFee == '$0' and record.rateType == 'Fixed':
        goodDeals.append(record)
print()
if len(goodDeals) > 0:
    print('Found {0} good deals!'.format(len(goodDeals)))
    goodDeals.sort(key=lambda x: x.rate)
    print(tabulate((record.getTabulateFormatted() for record in goodDeals), headers=currentUtilityContract.getTableHeaders()))
else:
    print('Didn\'t find any good deals!')

