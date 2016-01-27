
import datetime  
import sunrise  
s = sunrise.sun(lat=49,long=3)
print('sunrise at '+s.sunrise(when=datetime.datetime.now()))