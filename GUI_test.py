import PySimpleGUI as sg
from tkinter import *
#naa = dt.datetime.now().strftime("%Y%m%d")


import datetime as dt
import time


def getDateRangeFromWeek(p_year,p_week):
    firstdayofweek = dt.datetime.strptime(f'{p_year}-W{int(p_week )- 1}-1', "%Y-W%W-%w").date()
    d = []
    for i in range(1, 8):
        d.append((str(firstdayofweek + dt.timedelta(days=i - 1))).replace('-', ''))
    return d


sg.theme('sandyBeach')
s = 0
aa = 0

layout = [
    [sg.Checkbox('Område 1', default=False, key="-1-")],
    [sg.Checkbox('Område 2', default=False, key="-2-")],
    [sg.Checkbox('Molde. Ålesund, Trondheim', default=True, key="-3-")],
    [sg.Checkbox('Område 4', default=False, key="-4-")],
    [sg.Checkbox('Område 5', default=False, key="-5-")],
    [sg.Radio('2021', "Raar", value ='2021' )],
    [sg.Radio('2020', "Raar", default='2020')],
    [sg.Radio('2019', "Raar", default='2019')],
    [sg.Radio('2018', "Raar", default='2018')],
    [sg.Text('Uke nr:', size=(30, 1)), sg.InputText()],
    [sg.Submit('Finn priser'), sg.Cancel('Exit')]
]

#window = sg.Window('Strømpriser', layout)
window = sg.Window('Visning av strømpriser', layout, size=(500,500))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if values["-1-"] == True:
        s = 1
    if values["-2-"] == True:
        s = 2
    if values["-3-"] == True:
        s = 3
    if values["-4-"] == True:
        s = 4
    if values["-5-"] == True:
        s = 5
    print(s, values[0], values[1])


window.close()

#firstdate = getDateRangeFromWeek(values[1], values[2])
#print(event, values[0], values[1], values[2], values[3])
