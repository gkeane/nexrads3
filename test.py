#!/usr/bin/python
__author__ = 'nixCraft'
import sys
import astral
import pytz
from datetime import datetime

radar=''
year=''
month=''
day=''
total = len(sys.argv)
cmdargs = str(sys.argv)
print ("The total numbers of args passed to the script: %d " % total)
print ("Args list: %s " % cmdargs)
# Pharsing args one by one
radar=str(sys.argv[1])
year=str(sys.argv[2])
month=str(sys.argv[3])
day=str(sys.argv[4])

print radar
print year
print month
print day
ymd=year+month+day
dt = date_object = datetime.strptime(ymd,'%Y%m%d')
if radar == 'KYUX':
    loc=astral.Location( ('Yuma','Arizona',32.4953,-114.6558,53,'') )
elif radar=='KTLX':
    loc=astral.Location( ('Oklahoma City','Oklahoma',35,3331,-97.2275,338,'') )
else:
    sys.exit("Can't find radar site")

#print(loc.longitude)
print(loc.dawn(dt,local=False))
dawn=loc.dawn(dt,local=False)
dawn_str=dawn.strftime('%Y%m%d%H%M%S')
print dawn_str
print(loc.dusk(dt,local=False))
dusk=loc.dusk(dt,local=False)
dusk_str=dusk.strftime('%Y%m%d%H%M%S')
print dusk_str
