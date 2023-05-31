import requests
import json
import locale
import sys
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
        jsonFile = open(currentContractFile)
        cd = json.load(jsonFile)
        activeCd = [x for x in cd if x['active'] == True]
        if (len(activeCd) != 1):
            print ('Multiple active records found! Please check your contract file %s' % (currentContractFile))
            sys.exit()
        contract = CurrentUtilityRecord(
                        supplier=activeCd[0]['supplier'], 
                        rate=activeCd[0]['rate'], 
                        rateType=activeCd[0]['rateType'], 
                        introPrice=activeCd[0]['introPrice'], 
                        termLength=activeCd[0]['termLength'], 
                        earlyTermFee=activeCd[0]['earlyTermFee'], 
                        monthlyFee=activeCd[0]['monthlyFee'], 
                        signupDate=activeCd[0]['signupDate'],
                        startDate=activeCd[0]['startDate'], 
                        endDate=activeCd[0]['endDate'], 
                        yearlyUsage=activeCd[0]['yearlyUsage'],
                        territoryId=activeCd[0]['territoryId']
                    )
        
        url = url.format(contract.territoryId)
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

        records = []
        bestCurrentDeal = None
        bestDealByLength = {}

        locale.setlocale(locale.LC_ALL, '')

        for i in range(0, len(suppliers) - 1):
            newUtilityRecord = UtilityRecord(suppliers[i], Decimal(rates[i]), rateTypes[i], introPrices[i], int(termLengths[i].strip(' mo.')), Decimal(earlyTermFees[i][1:]), Decimal(monthlyFees[i][1:]), locale.currency((Decimal(contract.rate) - Decimal(rates[i])) * contract.yearlyUsage))
            records.append(newUtilityRecord)
            if newUtilityRecord.monthlyFee == 0 and newUtilityRecord.earlyTermFee < 25 and newUtilityRecord.rateType == 'Fixed' and newUtilityRecord.termLength >= 6:
                if bestCurrentDeal == None or newUtilityRecord.rate < bestCurrentDeal.rate:
                    bestCurrentDeal = newUtilityRecord

        print('Checking for rates better than or comparable to current rate:')
        print(tabulate([contract.getTabulateFormatted()], headers=contract.getTableHeaders()))

        goodDeals = []

        for record in records:
            if record.rate <= contract.rate and record.monthlyFee == 0 and record.rateType == 'Fixed' and record.termLength >= 6 and record.earlyTermFee <= 25 :
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

