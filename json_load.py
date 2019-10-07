import json

array_json = [
    "siteLoaded",
    "auth1Submitted",
    "auth2Passed",
    "loanParamsSubmitted",
    "passportPageOpened",
    "passportVerificationPassed",
    "addressConfirmationPageOpened",
    "regAddressConfirmed",
    "workInfoPageOpened",
    "workDetailsSubmitted",
    "bkiAgreementSigned",
    "accountParamsSubmitted",
    "appInSiebelCreated",
    "appApproved",
    "offerPageOpened",
    "documentSigned",
    "appExecuted",
]

with open('get-dashboard.json', 'r') as f:
    distros_dict = json.load(f)

for distro in distros_dict:
    values = [distro[key] for key in array_json]
    print(values)
