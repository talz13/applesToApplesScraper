class UtilityRecord:
    supplier = None
    rate = None
    rateType = None
    introPrice = None
    termLength = None
    earlyTermFee = None
    monthlyFee = None
    yearlySavings = None

    def __init__(self, supplier, rate, rateType, introPrice, termLength, earlyTermFee, monthlyFee, yearlySavings=None):
        self.supplier = supplier
        self.rate = rate
        self.rateType = rateType
        self.introPrice = introPrice
        self.termLength = termLength
        self.earlyTermFee = earlyTermFee
        self.monthlyFee = monthlyFee
        self.yearlySavings = yearlySavings
    
    def print(self):
        print('%s - %s - %s - %s - %s - %s - %s - %s' % (self.supplier, self.rate, self.rateType, self.introPrice, self.termLength, self.earlyTermFee, self.monthlyFee, self.yearlySavings))
    
    def getTabulateFormatted(self):
        return [self.supplier, self.rate, self.rateType, self.introPrice, self.termLength, self.earlyTermFee, self.monthlyFee, self.yearlySavings]
    
    def getTableHeaders(self):
        return ['Supplier', 'Rate', 'Rate Type', 'Intro Price', 'Term Length', 'Early Term Fee', 'Monthly Fee', 'Yearly Savings']
