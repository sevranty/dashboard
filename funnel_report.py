import os
import wget
import ssl
import json
import configparser

print('=== START ===')

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')
url = config.get('setup', 'url')
filename = config.get('setup', 'filename')

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

name_json = [
    "ОК → Переход на сайт<br>[siteLoaded]",
    "Клиент ввел аутентификационные данные<br>[auth1Submitted]",
    "Клиент ввел корректные аутентификационные данные<br>[auth2Passed]",
    "ОК → Параметры кредита<br>[loanParamsSubmitted]",
    "Клиент перешёл к вводу паспорта<br>[passportPageOpened]",
    "ОК → Паспорт<br>[passportVerificationPassed]",
    "Клиент перешёл к подтверждению адрес<br>[addressConfirmationPageOpened]",
    "ОК → Адрес<br>[regAddressConfirmed]",
    "Клиент перешёл к вводу дохода и стажа<br>[workInfoPageOpened]",
    "Данные о работе и доходе введены<br>[workDetailsSubmitted]",
    "ОК → Подписали БКИ<br>[bkiAgreementSigned]",
    "Клиент указал реквизиты<br>[accountParamsSubmitted]",
    "Заявка заведена в Siebel<br>[appInSiebelCreated]",
    "ОК → Заявка одобрена скорингом<br>[appApproved]",
    "ОК → Ознакомился с кредитом<br>[offerPageOpened]",
    "ОК → Клиент подписал договор<br>[documentSigned]",
    "Риск контролер (Регистратор ГО) подтвердил выдачу<br>[appExecuted]",
]


print("# CLEAR-PROJECT") # CLEAR - PROJECT
if os.path.exists(filename):
    os.remove(filename)
    print('REMOVE OK: ' + filename)
else:
    print('File does not exists: ' + filename)

print("# DOWNLOAD") # DOWNLOAD
print('WGET: Beginning file download with wget module')
ssl._create_default_https_context = ssl._create_unverified_context
wget.download(url, filename)

print("# JSON") # JSON
with open('get-dashboard.json', 'r') as f:
    distros_dict = json.load(f)

print("# ARRAY") # ARRAY
values = list()
for distro in distros_dict:
    values.append([distro[key] for key in array_json])

print(values)

print("# PLOTLY") # PLOTLY
from plotly import graph_objects as go
fig = go.Figure()
fig.add_trace(go.Funnel(
    # name='Today',
    # name='Yesterday',
    # name='Week',
    orientation="h",
    y=name_json,
    x=values[2],
    #textposition="inside",
    textposition="outside",
    textinfo="value+percent previous"))

print('SHOW: fig.show')
fig.show()

print("# CLEAR-PROJECT") # CLEAR - PROJECT
if os.path.exists(filename):
    os.remove(filename)
    print('REMOVE OK: ' + filename)
else:
    print('File does not exists: ' + filename)
print('=== END ===')