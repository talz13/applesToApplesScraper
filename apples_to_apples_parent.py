import requests
import json
from decimal import Decimal
from collections import namedtuple
from json import JSONEncoder
from lxml import html
from tabulate import tabulate
from utilityRecord import UtilityRecord
from currentUtilityRecord import CurrentUtilityRecord

class ApplesToApplesParent:
    @staticmethod
    def CheckRates(url, currentContractFile):
        response = requests.get(url)
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

        jsonFile = open(currentContractFile)
        cd = json.load(jsonFile)
        contract = CurrentUtilityRecord(supplier=cd['supplier'], rate=cd['rate'], rateType=cd['rateType'], introPrice=cd['introPrice'], termLength=cd['termLength'], earlyTermFee=cd['earlyTermFee'], monthlyFee=cd['monthlyFee'], signupDate=cd['signupDate'], startDate=cd['startDate'], endDate=cd['endDate'], yearlyUsage=cd['yearlyUsage'])

        records = []
        bestCurrentDeal = None

        for i in range(0, len(suppliers) - 1):
            newUtilityRecord = UtilityRecord(suppliers[i], Decimal(rates[i]), rateTypes[i], introPrices[i], int(termLengths[i].strip(' mo.')), Decimal(earlyTermFees[i][1:]), Decimal(monthlyFees[i][1:]), (Decimal(contract.rate) - Decimal(rates[i])) * contract.yearlyUsage)
            records.append(newUtilityRecord)
            if newUtilityRecord.monthlyFee == 0 and newUtilityRecord.rateType == 'Fixed':
                if bestCurrentDeal == None or newUtilityRecord.rate < bestCurrentDeal.rate:
                    bestCurrentDeal = newUtilityRecord

        print('Checking for rates better than or comparable to current rate:')
        print(tabulate([contract.getTabulateFormatted()], headers=contract.getTableHeaders()))

        goodDeals = []

        for record in records:
            if record.rate <= contract.rate and record.monthlyFee == 0 and record.rateType == 'Fixed' and record.termLength >= 6 and record.earlyTermFee < 99 :
                goodDeals.append(record)
        print()
        if len(goodDeals) > 0:
            print('Found {0} good deals!'.format(len(goodDeals)))
            goodDeals.sort(key=lambda x: x.rate)
            print(tabulate((record.getTabulateFormatted() for record in goodDeals), headers=contract.getTableHeaders()))
        else:
            print('Didn\'t find any good deals!')
            print('Here\'s the best current deal found:')
            print(tabulate([bestCurrentDeal.getTabulateFormatted()], headers=bestCurrentDeal.getTableHeaders()))

