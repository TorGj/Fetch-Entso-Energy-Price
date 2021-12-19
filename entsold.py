import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import PySimpleGUI as psg
import requests
from PIL import Image
import json       # Eksporterings ting
import config
from twython import Twython, TwythonError


x = []
y = []
p_max = 0

def getDateRangeFromWeek(p_year,p_week):
    firstdayofweek = dt.datetime.strptime(f'{p_year}-W{int(p_week) - 1}-1', "%Y-W%W-%w").date()
    d = []
    for i in range(1, 8):
        d.append((str(firstdayofweek + dt.timedelta(days=i - 1))).replace('-', ''))
    return d


def App_GUI():
    psg.theme('TealMono')
    #define layout
    layout=[[psg.Text('Velg område', size=(20, 1), font='Lucida', justification='left')],
           [psg.Radio('Ålesund (3)', 'area', key ='10YNO-3--------J'),
            psg.Radio('Oslo (1)', 'area',     key='10YNO-1--------2'),
            psg.Radio('Arendal (2)', 'area',  key='10YNO-2--------T'),
            psg.Radio('Narvik (4)', 'area',   key='10YNO-4--------9'),
            psg.Radio('Bergen (5)', 'area',   key='10Y1001A1001A48H')],
           [psg.Text('Velg år', size=(20, 1), font='Lucida', justification='left')],
           [psg.Radio('2021', 'aar', key='2021'),
            psg.Radio('2020', 'aar', key='2020'),
            psg.Radio('2019', 'aar', key='2019'),
            psg.Radio('2018', 'aar', key='2018'),
            psg.Radio('2017', 'aar', key='2017'),
            psg.Radio('2016', 'aar', key='2016')],
           [psg.Text('Velg uke',size=(20, 1), font='Lucida', justification='left')],
           [psg.InputText(size=(10))],
           [psg.Button('Vis priser', font=('Times New Roman',14)), psg.Button('Glem det', font=('Times New Roman',14))]]
    #Define Window
    win =psg.Window('Hent strømpriser',layout)
    e,v=win.read()
    win.close()
    u_a = []
    for val in v:
      if win.find_element(val).get()==True:
            u_a.append(val)
    u_a.append(v[0])
    return u_a


u_a = App_GUI()
firstdate = getDateRangeFromWeek(u_a[1],u_a[2])


# create a Twython object by passing the necessary secret passwords
tokenkey = str(Twython(config.api_key)).replace('<Twython: ','').replace('>','')

place = u_a[0]

#naa = dt.datetime.now().strftime("%Y%m%d")
# Fetch price of EUR in NOK
def getentsoe(day):
    url_entso = 'https://transparency.entsoe.eu/api?documentType=A44&in_Domain=' + place + '&out_Domain=' + place + '&periodStart=' + day + '0000&periodEnd=' + day + '2300&securityToken=' + tokenkey
    ele = str(requests.Session().get(url=url_entso).text)
    klipp = ele.split("<Period>")[1].split("</Period>")[0]
    skriv_fil(day,klipp)
    return klipp

def geteurnok():
    url_nb = 'https://data.norges-bank.no/api/data/EXR/M.EUR.NOK.SP?lastNObservations=1'
    eurnok = str(requests.Session().get(url=url_nb).text)
    outeur = eurnok.split('OBS_VALUE="')[1].split('"/></S')[0]
    eurprice = (100 / (float(outeur)))
    return eurprice


def les_fil(yyyymmdd):
    min_fil.close()


def skriv_fil(yyyymmdd, data):
    # Skriver til en fil til, men med et mer standard format...
    with open('%s.txt' % yyyymmdd, 'w') as filehandle:
        json.dump(data, filehandle)


def bygg_data(euro,epris):
    global p_max
    # Create list of NOK prices in p and a list of hours of day in t
    t = []
    p = []
    i = 1
    while i < 24:
        timenr = epris.split("<position>" + str(i))[1].split("</price.amount>")[0]
        timepris = float(timenr.split("<price.amount>")[1].split("</price.amount>")[0])
        p_vat = round(timepris * 1.25 * euro / 1000, 2)
        p.append(p_vat)  # · 1.25  ... VAT
        t.append(i)
        if p_vat > p_max:
            p_max = p_vat
        i = i + 1
    # x and y is arrays of arrays of matching time and price
    # print(p)
    x.append(t)
    y.append(p)
    # Create one plot for one day


def plotter(xer, yer, m, p_max):
    global testbilde
    # Draw first subplot using plt.subplot
    #          row, col, pos.aktuell
    plt.subplot(1, len(x), m + 1)
    # plt.imshow(testbilde, zorder=1)
    plt.ylim(0, p_max)  # Max 250 øre på yakse
    plt.bar(xer, yer, color='green')
    plt.yscale('linear')  # Defines log/linear scale
    plt.xlabel(dato[m])
    plt.title("Priser i NOK",
              fontsize='13',
              backgroundcolor='navy',
              color='white')
    # Starts building data to plot


eur_rate = geteurnok()
dato = []
for n in range(0, 7):
    # print('n',n)
    day = str(firstdate[n])
    print('Henter priser for dato:', day)
    dagens_priser = getentsoe(day)
    bygg_data(eur_rate, dagens_priser)
    dato.append(day)
# Make canvas with settings
figure(num=None, figsize=(10, 6))  # len(x)*7
font = {'family': 'Times New Roman',
        'weight': 'bold',
        'size': 12}
plt.rc('font', **font)
# testbilde = Image.open('entso.png')
# Make one plot pr day
for m in range(0, len(x)):
    print('Lager søylediagram for dag:', m)
    plotter(x[m], y[m], m, p_max)
# When the plot "plt" is finished constructed:
plt.show()