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
    # "passportPageOpened",
    "passportVerificationPassed",
    # "addressConfirmationPageOpened",
    "regAddressConfirmed",
    # "workInfoPageOpened",
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
    # "Клиент перешёл к вводу паспорта<br>[passportPageOpened]",
    "ОК → Паспорт<br>[passportVerificationPassed]",
    # "Клиент перешёл к подтверждению адрес<br>[addressConfirmationPageOpened]",
    "ОК → Адрес<br>[regAddressConfirmed]",
    # "Клиент перешёл к вводу дохода и стажа<br>[workInfoPageOpened]",
    "Данные о работе и доходе введены<br>[workDetailsSubmitted]",
    "ОК → Подписали БКИ<br>[bkiAgreementSigned]",
    "Клиент указал реквизиты<br>[accountParamsSubmitted]",
    "Заявка заведена в Siebel<br>[appInSiebelCreated]",
    "ОК → Заявка одобрена скорингом<br>[appApproved]",
    "ОК → Ознакомился с кредитом<br>[offerPageOpened]",
    "ОК → Клиент подписал договор<br>[documentSigned]",
    "Риск контролер (Регистратор ГО) подтвердил выдачу<br>[appExecuted]",
]

print("# CLEAR-PROJECT")  # CLEAR - PROJECT
if os.path.exists(filename):
    os.remove(filename)
    print('REMOVE OK: ' + filename)
else:
    print('File does not exists: ' + filename)

print("# DOWNLOAD")  # DOWNLOAD
print('WGET: Beginning file download with wget module')
ssl._create_default_https_context = ssl._create_unverified_context
wget.download(url, filename)

print("# JSON")  # JSON
with open('get-dashboard.json', 'r') as f:
    distros_dict = json.load(f)

print("# ARRAY")  # ARRAY
values = list()
for distro in distros_dict:
    values.append([distro[key] for key in array_json])

print(values)

print("# PLOTLY")  # PLOTLY
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
    # textposition="outside",
    textinfo="value+percent previous"))

fig.add_trace(go.Funnel(
    name='Today',
    # name='Yesterday',
    # name='Week',
    orientation="h",
    y=name_json,
    # x=values[2],
    x=values[0],
    # textposition="inside",
    textposition="outside",
    textinfo="value+percent previous"))

print('SHOW № 1: fig.show')
fig.show()

fig2 = go.Figure()

fig2.add_trace(go.Funnelarea(
    scalegroup="first",
    values=values[3],
    textinfo="value",
    # textinfo=name_json,
    title={"position": "top center", "text": "Current Week"},
    domain={"x": [0, 0.5], "y": [0, 0.5]}))

fig2.add_trace(go.Funnelarea(
    scalegroup="first",
    values=values[0],
    textinfo="value",
    # textinfo=name_json,
    title={"position": "top center", "text": "Today"},
    domain={"x": [0, 0.5], "y": [0.55, 1]}))

fig2.add_trace(go.Funnelarea(
    scalegroup="second",
    values=values[3],
    textinfo="value",
    # textinfo=name_json,
    title={"position": "top left", "text": "Previous Week"},
    domain={"x": [0.55, 1], "y": [0, 0.5]}))

fig2.add_trace(go.Funnelarea(
    scalegroup="second",
    values=values[1],
    textinfo="value",
    # textinfo=name_json,
    title={"position": "top left", "text": "Yesterday"},
    domain={"x": [0.55, 1], "y": [0.55, 1]}))

fig2.update_layout(
    margin={"l": 400, "r": 400},
    shapes=[
        {"x0": 0, "x1": 0.5, "y0": 0, "y1": 0.5},
        {"x0": 0, "x1": 0.5, "y0": 0.55, "y1": 1},
        {"x0": 0.55, "x1": 1, "y0": 0, "y1": 0.5},
        {"x0": 0.55, "x1": 1, "y0": 0.55, "y1": 1}])

print('SHOW № 2: fig2.show')
fig2.show()

print("# CLEAR-PROJECT")  # CLEAR - PROJECT
if os.path.exists(filename):
    os.remove(filename)
    print('REMOVE OK: ' + filename)
else:
    print('File does not exists: ' + filename)

# perc = [values[i + 1]/values[i] for i in range(len(values)) if i < len(values) - 1]


week_current = values[2]  # current week
week_previous = values[3]  # previous week

week_current_perc = [week_current[i + 1] / week_current[i] if week_current[i] else 0 for i in range(len(week_current))
                     if i < len(week_current) - 1]
week_previous_perc = [week_previous[i + 1] / week_previous[i] if week_previous[i] else 0 for i in
                      range(len(week_previous)) if i < len(week_previous) - 1]

week_sprint = [l1 + l2 for l1, l2 in zip(week_current, week_previous)]
week_sprint_perc = [week_sprint[i + 1] / week_sprint[i] if week_sprint[i] else 0 for i in range(len(week_sprint)) if
                    i < len(week_sprint) - 1]
week_sprint_perc_norm = [round(l1, 5) * 7000 for l1 in week_sprint_perc]

name_json_minus = name_json[1:]
name_json_norm = ["<b>%s%%</b> → %s<br>%s" % (round(spl1, 2) * 100, spl2, spl3) for spl1, spl2, spl3 in
                  zip(week_sprint_perc, week_sprint[1:], name_json_minus)]

# SAMPLE: https://plot.ly/python/graphing-multiple-chart-types/
fig3 = go.Figure()

# max(week_sprint)
fig3.add_trace(
    go.Scatter(
        # x = week_sprint,
        # x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        # x=name_json[1:],
        x=name_json_norm,
        # x = [0, 1, 2, 3, 4, 5],
        # y = [20000, 15000, 10000, 5000, 0]
        y=week_sprint[1:],
        name="absolute",
        #line_shape='absolute',
        #plot_bgcolor='white',
    ))

fig3.add_trace(
    go.Bar(
        # x=week_sprint_perc,
        # x=[0, 1, 2, 3, 4, 5],
        # x=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        # x=name_json[1:],
        x=name_json_norm,
        # y=[100, 75, 50, 25, 0]
        y=week_sprint_perc_norm,
        name="100% relative",
        #line_shape='100% relative',
        #plot_bgcolor='white',
    ))

fig3.show()

'''
print('======================')
print("week_current")
print(week_current)

print("week_previous")
print(week_previous)

print("week_current_perc")
print(week_current_perc)

print("week_previous_perc")
print(week_previous_perc)

print("week_sprint")
print(week_sprint)

print("week_sprint_perc")
print(week_sprint_perc)

print("week_sprint_perc_norm")
print(week_sprint_perc_norm)
print('======================')
'''

print('=== END ===')
