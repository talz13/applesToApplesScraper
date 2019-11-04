import requests
from lxml import html
from tabulate import tabulate

class utilityRecord:
    supplier = None
    rate = None
    rateType = None
    introPrice = None
    termLength = None
    earlyTermFee = None
    monthlyFee = None

    def __init__(self, supplier, rate, rateType, introPrice, termLength, earlyTermFee, monthlyFee):
        self.supplier = supplier
        self.rate = rate
        self.rateType = rateType
        self.introPrice = introPrice
        self.termLength = termLength
        self.earlyTermFee = earlyTermFee
        self.monthlyFee = monthlyFee
    
    def print(self):
        print('%s - %s - %s - %s - %s - %s - %s' % (self.supplier, self.rate, self.rateType, self.introPrice, self.termLength, self.earlyTermFee, self.monthlyFee))
    
    def getTabulateFormatted(self):
        return [self.supplier, self.rate, self.rateType, self.introPrice, self.termLength, self.earlyTermFee, self.monthlyFee]
    
    def getTableHeaders(self):
        return ['Supplier', 'Rate', 'Rate Type', 'Intro Price', 'Term Length', 'Early Term Fee', 'Monthly Fee']

response = requests.get("http://www.energychoice.ohio.gov/ApplesToApplesComparision.aspx?Category=Electric&TerritoryId=7&RateCode=1")
tree = html.fromstring(response.content)

tbody = tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody')

suppliers = tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[2]/span/text()')
rates = list(map(str.strip, tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[3]/text()')))
rateTypes = list(filter( lambda x: len(x) > 0, list(map(str.strip, tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[4]/text()')))))
introPrices = list(filter(lambda x: x == 'Yes' or x == 'No', tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[6]/p/text()')))
termLengths = list(map(str.strip, tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[7]/text()')))
#earlyTermFee = list(map(str.strip, tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[8]/text()')))
#earlyTermFee = list(map(str.strip, tree.xpath('(//tbody/tr/td[8]/p | //tbody/tr/td[8][not(p)])/text()')))
earlyTermFees = list(map(str.strip, tree.xpath('(//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[8]/p | //*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[8][not(p)])/text()')))
monthlyFees = list(map(str.strip, tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_upOffers"]/div[4]/table/tbody/tr[*]/td[9]/text()')))

records = []
for i in range(0, len(suppliers) - 1):
    newUtilityRecord = utilityRecord(suppliers[i], rates[i], rateTypes[i], introPrices[i], termLengths[i], earlyTermFees[i], monthlyFees[i])
    records.append(newUtilityRecord)

print('debug breakpoint')

currentUtilitySignupDate = '2019-11-04'
currentUtilityStartDate = '2019-12-04' # maybe?
currentUtilityEndDate = '2020-06-04' # maybe?
currentUtilityContract = utilityRecord('New Wave Energy Corp', '0.0430', 'Fixed', 'No', '6 mo.', '$99', '$0')

print('Checking for rates better than or comparable to current rate:')
print(tabulate([currentUtilityContract.getTabulateFormatted()], headers=currentUtilityContract.getTableHeaders()))

goodDeals = []

for record in records:
    if record.rate <= currentUtilityContract.rate and record.monthlyFee == '$0':
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

