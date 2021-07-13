import re
from datetime import datetime
from os import getenv
import requests
from dotenv import load_dotenv
from lxml import html
from requests.exceptions import Timeout
from prometheus_client import Gauge

load_dotenv()
print(getenv('HOST'))
now = datetime.now()  # current date and tim

def energy():
    """W trakcie przygotowywania ."""
    url = f"{getenv('HOST')}/index.php/realtimedata/old_energy_graph"
    dzisiaj = now.strftime("%m/%d")
    print("date and time:", dzisiaj)
    try:
        x = requests.get(url, timeout=2)
    except Timeout:
        print('The request timed out')
    else:
        print('The request did not time out')
        print(x.json())


def power():
    """W trakcie przygotowywania ."""
    url = f"{getenv('HOST')}/index.php/realtimedata/old_power_graph"
    dzisiaj = now.strftime("%m/%d")
    print("date and time:", dzisiaj)
    try:
        x = requests.get(url, timeout=2)
    except Timeout:
        print('The request timed out')
    else:
        print('The request did not time out')
        print(x.json())


def text(elt):
    """Formatowanie danych z tabelki."""
    obiekt = elt.text_content().replace(u'\xa0', u' ')
    a = ""
    if len(re.findall("\d+-\d", obiekt)) == 1:
        a = re.findall("\d+-\d+", obiekt)[0]
        return a

    if obiekt.find("W") != -1:
        a = re.findall("\d+", obiekt)[0]
    if obiekt.find("V") != -1:
        a = re.findall("\d+", obiekt)[0]
        # obiekt = (f"Voltage:{a}")
    if (obiekt.find("C") != -1):
        a = re.findall("\d+", obiekt)[0]
        # obiekt = (f"Temperature:{a}")
    if (obiekt.find("Hz") != -1):
        a = re.findall("\d+", obiekt)[0]
        obiekt = (f"Frequency:{a}")
    if len(re.findall("\d+-\d+-\d+", obiekt)) == 1:
        a = obiekt.replace('\n', '')
        # obiekt = (f"data:{a}")
    if len(re.findall("-.", obiekt)) == 1:
        return 0

    return a


def tablica():
    """Pobieranie danych z tablicy."""
    urlHtml = f"{getenv('HOST')}/index.php/realtimedata"
    tabl = []
    try:
        x = requests.get(urlHtml, timeout=3)
    except Timeout:
        print('The request timed out')
        return tabl
    except requests.exceptions.MissingSchema:
        print('bład połaczenia')        
        return tabl
    else:
        print(f'mamy strone tablica')
    return converttab(x)

def converttab(x):
    tabl=[]
    root = html.fromstring(x.content)
    lista = ['falowing-panel', 'Power', 'Frequency', 'Voltage', 'Temperature', 'data']
    listb = ['falowing-panel', 'Power', 'Voltage']
    for table in root.xpath('//table/tbody'):
        i = 0
        for tr in table.xpath('//tr[count(*) > 2]'):
            if (len(tr) == 6):
                dane = list(text(td) for td in tr.xpath('td'))
                if len(dane) == 6:
                    tabl.append(dict(zip(lista, dane)))
            if (len(tr) == 3):
                dane = list(text(td) for td in tr.xpath('td'))
                if len(dane) == 3:
                    tabl.append(dict(zip(listb, dane)))
    return tabl


def basesite():
    urlStart = f"{getenv('HOST')}/index.php/home"
    a,b,d=0,0,0
    try:
        x = requests.get(urlStart, timeout=3)
    except Timeout:
        print('The request timed out')
        return a,b,d
    except requests.exceptions.MissingSchema:
        print('bład połaczenia')
        return a,b,d
    else:
        print(f'mamy basesite')
        root = html.fromstring(x.content)
        LifetimeGeneration = root.xpath(
            '//table[@class="table table-condensed table-striped table-bordered"]/tr[2]/td[1]/text()')[0]
        LastSystemPower = \
            root.xpath('//table[@class="table table-condensed table-striped table-bordered"]/tr[3]/td[1]/text()')[0]
        GenerationCurrentDay = root.xpath(
            '//table[@class="table table-condensed table-striped table-bordered"]/tr[4]/td[1]/text()')[0]
        a = re.findall("\d+", LastSystemPower)[0]
        b = re.findall("^(\d+(?:[\.\,]\d{1,2})?)", GenerationCurrentDay)[0]
        d = re.findall("^(\d+(?:[\.\,]\d{1,2})?)", LifetimeGeneration)[0]
        return a, b, d


def stronaglowna(registry):
    a, b, d = basesite()
    e = Gauge(name="panele_lifetimegeneration", documentation="Lifetime Generation", registry=registry)
    e.set(d)
    c = Gauge(name="panele_generationcurrentday", documentation="Generation Current of Day", registry=registry)
    c.set(b)
    g = Gauge('panele_LastSystemPower', 'Last System Power', registry=registry)
    g.set(a)  # Set to a given value
    nap = Gauge('panele_Voltage', 'Voltage na panelu', ['Inverter', 'panel'], registry=registry)
    Power = Gauge('panele_Power', 'Power na panelu', ['Inverter', 'panel'], registry=registry)
    temp = Gauge('panele_Temp', 'Temperature na panelu', ['Inverter'], registry=registry)
    czest = Gauge('panele_Frequency', 'Frequency na panelu', ['Inverter'], registry=registry)

    for wpis in tablica():
        if wpis['falowing-panel'] != '' and len(wpis) == 6:
            fal = wpis['falowing-panel'].split("-")[0]
            pan = wpis['falowing-panel'].split("-")[1]
            nap.labels(Inverter=fal, panel=pan).set(wpis['Voltage'])
            Power.labels(Inverter=fal, panel=pan).set(wpis['Power'])
            temp.labels(Inverter=fal).set(wpis['Temperature'])
            czest.labels(Inverter=fal).set(wpis['Frequency'])
        if wpis['falowing-panel'] != '' and len(wpis) == 3:
            fal = wpis['falowing-panel'].split("-")[0]
            pan = wpis['falowing-panel'].split("-")[1]
            nap.labels(Inverter=fal, panel=pan).set(wpis['Voltage'])
            Power.labels(Inverter=fal, panel=pan).set(wpis['Power'])
    return registry


# basesite()
