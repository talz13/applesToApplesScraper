from utilityRecord import UtilityRecord


class CurrentUtilityRecord(UtilityRecord):
    signupDate = None
    startDate = None
    endDate = None
    yearlyUsage = None
    active = False
    territoryId = None

    def __init__(self, supplier, rate, rateType, introPrice, termLength, earlyTermFee, monthlyFee, signupDate, startDate, endDate, territoryId, yearlyUsage, yearlySavings=None):
        self.signupDate = signupDate
        self.startDate = startDate
        self.endDate = endDate
        self.yearlyUsage = yearlyUsage
        self.territoryId = territoryId

        UtilityRecord.__init__(self, supplier, rate, rateType, introPrice, termLength, earlyTermFee, monthlyFee)
    
    def print(self):
        print('%s - %s - %s - %s - %s - %s - %s - %s' % (self.supplier, self.rate, self.rateType, self.introPrice, self.termLength, self.earlyTermFee, self.monthlyFee, self.startDate, self.endDate, self.yearlyUsage))
    
    def getTabulateFormatted(self):
        return [self.supplier, self.rate, self.rateType, self.introPrice, self.termLength, self.earlyTermFee, self.monthlyFee, self.startDate, self.endDate, self.yearlyUsage]
    
    def getTableHeaders(self):
        return ['Supplier', 'Rate', 'Rate Type', 'Intro Price', 'Term Length', 'Early Term Fee', 'Monthly Fee', 'Start Date', 'End Date', 'Yearly Usage']
