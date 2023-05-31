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
    "yearlyUsage" : 12345,
    "territoryId" : 1
}
```

## Notes on territoryId
The current territoryIds from the energychoice site are as follows:

### Electric
Company | Territory ID
--- | ---
AES Ohio | 9
American Electric Power | 2
Duke Energy Ohio | 4
Ohio Edison | 7
The Illuminating Company | 6
Toledo Edison | 3

### Gas
Company | Territory ID
--- | ---
CenterPoint Energy Ohio (Vectren) | 11
Columbia Gas of Ohio | 8
Dominion Energy Ohio | 1
Duke Energy Ohio | 10