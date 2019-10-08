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
    name='Yesterday',
    # name='Week',
    orientation="h",
    y=name_json,
    # x=values[2],
    x=values[1],
    textposition="inside",
    #textposition="outside",
    textinfo="value+percent previous"))

fig.add_trace(go.Funnel(
    name='Today',
    # name='Yesterday',
    # name='Week',
    orientation="h",
    y=name_json,
    # x=values[2],
    x=values[0],
    #textposition="inside",
    textposition="outside",
    textinfo="value+percent previous"))

print('SHOW № 1: fig.show')
fig.show()


fig2 = go.Figure()

fig2.add_trace(go.Funnelarea(
    scalegroup = "first",
    values = values[3],
    textinfo = "value",
    #textinfo=name_json,
    title = {"position": "top center", "text": "Current Week"},
    domain = {"x": [0, 0.5], "y": [0, 0.5]}))

fig2.add_trace(go.Funnelarea(
    scalegroup = "first",
    values = values[0],
    textinfo = "value",
    #textinfo=name_json,
    title = {"position": "top center", "text": "Today"},
    domain = {"x": [0, 0.5], "y": [0.55, 1]}))

fig2.add_trace(go.Funnelarea(
    scalegroup = "second",
    values = values[3],
    textinfo = "value",
    #textinfo=name_json,
    title = {"position": "top left", "text": "Previous Week"},
    domain = {"x": [0.55, 1], "y": [0, 0.5]}))

fig2.add_trace(go.Funnelarea(
    scalegroup = "second",
    values = values[1],
    textinfo = "value",
    #textinfo=name_json,
    title = {"position": "top left", "text": "Yesterday"},
    domain = {"x": [0.55, 1], "y": [0.55, 1]}))

fig2.update_layout(
    margin = {"l": 400, "r": 400},
    shapes = [
            {"x0": 0, "x1": 0.5, "y0": 0, "y1": 0.5},
            {"x0": 0, "x1": 0.5, "y0": 0.55, "y1": 1},
            {"x0": 0.55, "x1": 1, "y0": 0, "y1": 0.5},
            {"x0": 0.55, "x1": 1, "y0": 0.55, "y1": 1}])

print('SHOW № 2: fig2.show')
fig2.show()

print("# CLEAR-PROJECT") # CLEAR - PROJECT
if os.path.exists(filename):
    os.remove(filename)
    print('REMOVE OK: ' + filename)
else:
    print('File does not exists: ' + filename)
print('=== END ===')