# applesToApplesScraper
Highlight better deals found on the Ohio Apples-to-Apples energy comparison site

Create a currentUtilityRecord JSON file to allow comparisons to be made (`current_electric.json` or `current_gas.json`), formatted as follows

```
{
    "supplier" : "Supplier Name",
    "rate" : 0.123, 
    "rateType" : "Fixed", 
    "introPrice" : "No", 
    "termLength" : 12, 
    "earlyTermFee" : 0, 
    "monthlyFee" : 0,
    "signupDate": "2021-01-01",
    "startDate" : "2021-01-01",
    "endDate" : "2022-01-01",
    "yearlyUsage" : 12345
}
```