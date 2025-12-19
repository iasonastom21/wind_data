import requests
import csv
import pandas as pd
from io import StringIO

#Input

Latitude=32.1, -20.6
Longitude=-78.5, 35.1
SiteTimezone=-8, 5
DataTimezone=-8, 5


newheight=150

CSV="https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/55.0997222%2C%2011.8444444/2024-01-01/2025-01-01?unitGroup=metric&elements=add:winddir100,add:winddir50,add:windspeed100,add:windspeed50&include=hours&key=NCGJ4EZNZERK7SXYPKG5AWSNY&contentType=csv"


response = requests.get(CSV)
response.raise_for_status()
df = pd.read_csv(StringIO(response.text))
df = df.head(8760)

df["windspeed"]=df["windspeed"]/3.6 #covert km/h to m/s
df["sealevelpressure"]=df["sealevelpressure"]*100

df["windspeed100"]=df["windspeed100"]/3.6 #covert km/h to m/s
df["windspeed50"]=df["windspeed50"]/3.6 #covert km/h to m/s

alpha=0.15


windspeedat150=df["windspeed100"]*(newheight/100)**alpha

df['windspeedat150']=windspeedat150


#IMPORTANT - change values in the titles as well, otherwise, SAM will not know what height the values are provided at
avgatchose=windspeedat150.mean()
windspeed100s=df["windspeed100"]
avgat100=windspeed100s.mean()
with open("N%C3%A6sbjerg.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["lat",Latitude, "long",Longitude, "site timezone", SiteTimezone,"data timezone", DataTimezone])
    writer.writerow(["air pressure at 0m","wind speed at 50m","wind direction at 50m","wind speed at 100m","wind direction at 100m","wind speed at 150m","wind direction at 150m","air temperature at 100m"])
    df[["sealevelpressure","windspeed50","winddir50","windspeed100","winddir100", "windspeedat150", "winddir","temp"]].to_csv(file, index=False, header=False)
    
print('Average wind speed at chosen height',avgatchose)
print('Average wind speed at 100 m', avgat100)
