import pandas as pd
import datetime
import pylab as pl
import pickle

df = pd.read_csv("./data/Basin.EP.ibtracs_all.v03r09.csv", header=1)
storms = df.groupby("Serial_Num")

stormdata = {}
for idnum, data in storms:
    name = data.Name.values[0]
    if name not in stormdata.keys():
        stormdata[name] = {}
    latitude = data.Latitude[data.Longitude != -999].values
    longitude = data.Longitude[data.Longitude != -999].values
    longitude = np.array(map(float,longitude))
    longitude[longitude < 0] += 360
    pressure = data["Pres(WMO)"][data.Longitude != -999].values
    date = datetime.datetime.strptime(data.ISO_time.values[0], '%Y-%m-%d %H:%M:%S')
    year = date.year
    if year >= 2001:
        stormdata[name][year] = {"latitude":latitude, "longitude":longitude, "pressure":pressure}

damagingstorms = pd.read_csv("./data/data_pacific_hurricane_losses.csv")
damagingstorms["Name"] = map(lambda x: x.upper().split("-")[0], damagingstorms["Storm  name"].values)

damagingstorms = damagingstorms[(damagingstorms["Areas affected"] != "Hawaii") & (damagingstorms["Name"] != "IOKE")]

losscausingtracks = {}
idnum = 0
for i in damagingstorms.index:
    Name = damagingstorms["Name"].loc[i]
    Year = damagingstorms["Year"].loc[i]
    Loss = damagingstorms["Damage  (millions  USD  )"].loc[i]
    try:
        storm = stormdata[Name][Year]
    except:
        print "no track found for storm %s in %d"%(Name,Year)
        continue
    storm["Loss"] = Loss
    losscausingtracks[idnum] = storm
    idnum += 1


with open("./data/losscausingtracks.pkl","w") as f:
    pickle.dump(losscausingtracks, f)


