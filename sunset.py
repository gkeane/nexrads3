import astrallib
import json
import time
import requests
import dateutil.parser as parser
#import datetime
from datetime import datetime
def sunset(lat,long,dt):
    indate=dt.strftime('%Y-%m-%d')
    #print(indate)
    resp=requests.get('http://api.sunrise-sunset.org/json?lat='+lat+'&lng='+long+'&formatted=0&date='+indate)
    json_data = json.loads(resp.text)
    #print(resp.text)
    #print(json_data['results']['sunset'])
    date=parser.parse(json_data['results']['sunset'])
    return date
