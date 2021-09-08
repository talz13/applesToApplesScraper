from apples_to_apples_parent import ApplesToApplesParent

url = "http://www.energychoice.ohio.gov/ApplesToApplesComparision.aspx?Category=NaturalGas&TerritoryId=8&RateCode=1"
currentContractFile = "current_gas.json"

ApplesToApplesParent.CheckRates(url, currentContractFile)