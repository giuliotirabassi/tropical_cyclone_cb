import urllib
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

years = range(2001,2017)

datalosses = []
for year in years:
    webpage = urllib.urlopen("https://en.wikipedia.org/wiki/%d_Pacific_hurricane_season" % year)
    soup = BeautifulSoup(webpage, "lxml")
    tables = soup.find_all("table",class_="wikitable")
    table = tables[-1] if year != 2011 else tables[-2]
    annoyinghiddenstuff = tables[-1].select( '[style~="display:none;"]' ) + tables[-1].select( '[style~="display:none"]' )
    for element in annoyinghiddenstuff:
        element.replaceWith("")
    df = pd.read_html(table.prettify(), header=0)[0]

    if year == 2008:
        del df["Refs"]
        pressure = [value.encode("utf-8").split("\xc2")[0] if type(value) == unicode else value for value in df.Pressure.values]
        df.Pressure = pressure
        losses = [value.encode("utf-8").split("\xc2")[0][1:]  if type(value) == unicode else value  for value in df['Damage  (USD)'].values]
        df['Damage  (USD)'] = losses
        df = pd.DataFrame(columns = [u'Storm  name', u'Dates active', u'Storm  category  at peak intensity',u'Max 1-min  wind  mph (km/h)', u'Min.  press.  (  mbar  )',u'Areas affected', u'Damage  (millions  USD  )', u'Deaths'], data = df.values)
    df["Year"] = [year] * len(df)
    datalosses.append(df)

datalosses = pd.concat(datalosses)

datalosses = datalosses[(datalosses['Storm  name'] != "Season Aggregates") & np.array(map(lambda x: type(x) == str, datalosses['Areas affected'].values)) ]
    
datalosses =  datalosses[map(lambda x: x[0].isdigit() if type(x) != float else False,datalosses["Damage  (millions  USD  )"].values)]

datalosses.to_csv("./data/data_pacific_hurricane_losses.csv", index=False, encoding="utf-8")


