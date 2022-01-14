import datetime as dt
from calendar import monthrange
#from datetime import date
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as psg
import requests
from PIL import Image
import json       # Eksporterings ting
import config
import layout1
from twython import Twython, TwythonError
import os
#matplotlib.use('TkAgg')

firstdate = []
x = []
y = []
dato = []
p_max = 0
continious = True

def getDateRangeFromWeek(p_year,p_week):
    firstdayofweek = dt.datetime.strptime(f'{p_year}-W{int(p_week) - 1}-1', "%Y-W%W-%w").date()
    d = []
    for i in range(1, 8):
        d.append((str(firstdayofweek + dt.timedelta(days=i - 1))).replace('-', ''))
    return d

def getDateRangeFromMonth(p_year, p_month):
    print(p_year, p_month)
    d = []
    m = monthrange(int(p_year), int(p_month))
    n = int(m[1])
    for i in range(0, n):
        #d.append(str(int(firstday)+i))
        d.append(((dt.date(int(p_year), int(p_month), 1)) + dt.timedelta(days=i)).strftime("%Y%m%d"))
    return d

def getDateRangeFrom_Today():
    d = []
    d.append((dt.datetime.today() + dt.timedelta(days=-2)).strftime("%Y%m%d"))
    d.append((dt.datetime.today() + dt.timedelta(days=-1)).strftime("%Y%m%d"))
    d.append(dt.datetime.today().strftime("%Y%m%d"))
    d.append((dt.datetime.today() + dt.timedelta(days=1)).strftime("%Y%m%d"))
    return d

u_a = layout1.App_GUI_B()

def decide_out():
    global continious
    global firstdate
    if int(u_a[1]) > 0:
        print('get Month')
        firstdate = getDateRangeFromMonth(u_a[3], u_a[1])
    elif u_a[3] == 'dagens':
        print('Dagens energipriser')
        firstdate = getDateRangeFrom_Today()
        print(firstdate)
        continious = False
    else:
        print('get week')
        firstdate = getDateRangeFromWeek(u_a[3], u_a[0])
        continious = False

print(u_a)
decide_out()

tokenkey = str(Twython(config.api_key)).replace('<Twython: ','').replace('>','')
place = u_a[2]  # Region code


def getentsoe(day, s):      # Requests response form Entso API
    try:
        url_entso = 'https://transparency.entsoe.eu/api?documentType=A44&in_Domain=' + place + '&out_Domain=' + place + '&periodStart=' + day + '0000&periodEnd=' + day + '2300&securityToken=' + tokenkey
        ele = str(requests.Session().get(url=url_entso).text)
        klipp = ele.split("<Period>")[1].split("</Period>")[0]
        skriv_fil(day, klipp, s)
    except:
        print('Prisene for', day,'har ikke kommet enda')
        klipp = 'nan'
    return klipp

def geteurnok():            # Fetch price of EUR in NOK
    url_nb = 'https://data.norges-bank.no/api/data/EXR/M.EUR.NOK.SP?lastNObservations=1'
    eurnok = str(requests.Session().get(url=url_nb).text)
    outeur = eurnok.split('OBS_VALUE="')[1].split('"/></S')[0]
    eurprice = (100 / (float(outeur)))
    return eurprice

def les_fil(yyyymmdd, s):
    yyyymmdds = yyyymmdd+s
    min_fil = open('tgdata/%s.txt' % yyyymmdds, 'r')
    innhold = min_fil.read()
    min_fil.close()     # Close file to allow other to access file
    return innhold

def fil_eksisterer(yyyymmdd, s):
    yyyymmdds = yyyymmdd + s
    if (os.path.isfile('tgdata/%s.txt' % yyyymmdds))==True:
        print('Finnes lokalt.')
        return les_fil(yyyymmdd,s)
    else:
        print('Må hente fra Entso-E')
        return getentsoe(yyyymmdd, s)

def skriv_fil(yyyymmdd, data, s):
    yyyymmdds = yyyymmdd + s
    # Skriver til en fil til, men med et mer standard format...
    with open('tgdata/%s.txt' % yyyymmdds, 'w') as filehandle:
        json.dump(data, filehandle)
    # 'with' construct --> you won't have to worry about closing the file.

def bygg_data(euro, epris):
    global p_max
    # Create list of NOK prices in p and a list of hours of day in t
    t = []
    p = []
    i = 1   # The data has a lot of rubbish around runs through each days dataset.
    while i < 25:
        try:
            timenr = epris.split("<position>" + str(i))[1].split("</price.amount>")[0]
            timepris = float(timenr.split("<price.amount>")[1].split("</price.amount>")[0])
            p_vat = round(timepris * 1.25 * euro / 1000, 2)
            p.append(p_vat)  # · 1.25 = 25% VAT
            t.append(i)
            if p_vat > p_max:
                p_max = p_vat
        except:
            print(i, end=' ')
        i = i + 1
    # x and y is arrays of arrays of matching time and price
    print('')
    x.append(t)
    y.append(p)     # All prices for first day in first instance

def plot_many_days(xer, yer, weeknr, p_max):
    cx = []
    a = 1
    for i in xer:   # Just making a list for x-values 1 pr hour
        cx.append(a)
        a = a+1

    plt.ylim(0, p_max)  # Max 250 øre på y-akse
    plt.bar(cx, yer, color='green')
    plt.yscale('linear')  # Defines log/linear scale
    plt.ylabel('Pris pr kWh i NOK')
    plt.xlabel('En pris for hver time hele måneden')


def plot_one_day(xer, yer, m, p_max):
    d = ['  Mandag  ', '  Tirsdag  ', '  Onsdag  ', '  Torsdag  ', '  Fredag  ', '  Lørdag  ', '  Søndag  ']
    global testbilde
    # Draw first subplot using plt.subplot
    #          row, col, pos.aktuell
    plt.subplot(1, len(x), m + 1)
    # plt.imshow(testbilde, zorder=1)
    plt.ylim(0, p_max)  # Max "høyeste pris i datasettet" øre på yakse
    plt.bar(xer, yer, color='green')
    plt.yscale('linear')  # Defines log/linear scale
    plt.xlabel(dato[m])   # Dato på formen: yyyymmdd
    daynr = dt.datetime(year=int(dato[m][0:4]), month=int(dato[m][4:6]), day=int(dato[m][6:8])).weekday()
    plt.title(str(d[daynr]),
              fontsize='14',
              backgroundcolor='khaki',
              color='blue')
    # Starts building data to plot
    # title dag: str(d[m]

eur_rate = geteurnok()


def what_area(place):  # Returns place name according to region code
    area = ['Oslo', 'Arendal', 'Ålesund', 'Narvik', 'Bergen']
    if place == '10YNO-1--------2':
        return area[0]
    elif place == '10YNO-2--------T':
        return area[1]
    elif place == '10YNO-3--------J':
        return area[2]
    elif place == '10YNO-4--------9':
        return area[3]
    else:
        return area[4]

region = what_area(place)

print('Antall dager: ', len(firstdate))
for n in range(0, len(firstdate)):
    day = str(firstdate[n])
    print('Henter priser for ' + region + ' dato:', day, end=". ")
    dagens_priser = fil_eksisterer(day, region) # sjekk om filer finnes, i såfall bruk dem.. Sjekk_om_fil(day)
    bygg_data(eur_rate, dagens_priser)
    dato.append(day)

# Make canvas with settings (w,h) in inches
figure(num=None, figsize=(16, 6))  # len(x)*7
font = {'family': 'Times New Roman',
        'weight': 'bold',
        'size': 12}
plt.rc('font', **font)
plt.suptitle('Strømprisene i perioden: ' + str(dato[0]) + ' - ' + str(dato[len(firstdate)-1]) + ' for '+ region)
# testbilde = Image.open('entso.png')

# Make one plot pr day
def seperate_days():
    for m in range(0, len(x)):
        print('Lager søylediagram for dag:', m+1)
        plot_one_day(x[m], y[m], m, p_max)

def continious_days():
    plot_many_days(flatten(x), flatten(y), 1, p_max)    # 1 is not used...

def flatten(t):
    return [item for sublist in t for item in sublist]

if continious:
    continious_days()
else:
    seperate_days()

# When the plot "plt" is finished constructed:
plt.show()