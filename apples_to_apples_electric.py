from apples_to_apples_parent import ApplesToApplesParent

url = "http://www.energychoice.ohio.gov/ApplesToApplesComparision.aspx?Category=Electric&TerritoryId=7&RateCode=1"
currentContractFile = "current_electric.json"

ApplesToApplesParent.CheckRates(url, currentContractFile)