import boto
import boto.s3
import sys, os
import re
import sys
import astral
import pytz
from datetime import datetime
from datetime import date, timedelta


LOCAL_PATH = './aws/'
PATH=LOCAL_PATH+'/2012/05/13/KYUX/'

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

ymd=year+month+day
dt = date_object = datetime.strptime(ymd,'%Y%m%d')
dt_path=dt.strftime('%Y')+'/'+dt.strftime('%m')+'/'+dt.strftime('%d')+'/'+radar+'/'
dt_y=dt-timedelta(days=1)
dt_path_y=dt_y.strftime('%Y')+'/'+dt_y.strftime('%m')+'/'+dt_y.strftime('%d')+'/'+radar+'/'
dt_t=dt+timedelta(days=1)
dt_path_t=dt_t.strftime('%Y')+'/'+dt_t.strftime('%m')+'/'+dt_t.strftime('%d')+'/'+radar+'/'
if radar == 'KYUX':
    loc=astral.Location( ('Yuma','Arizona',32.4953,-114.6558,53,'') )
elif radar=='KTLX':
    loc=astral.Location( ('Oklahoma City','Oklahoma',35.3331,-97.2275,338,'') )
else:
    sys.exit("Can't find radar site")

PATH=LOCAL_PATH+dt_path
if not os.path.exists(PATH):
    os.makedirs(PATH)
conn = boto.s3.connect_to_region('us-east-2')
conn = boto.connect_s3(anon=True)
bucket = conn.get_bucket('noaa-nexrad-level2')
get_files=[]
print(loc.dawn(dt,local=False))
dawn=loc.dawn(dt,local=False)
sunrise=dawn.strftime('%Y%m%d%H%M%S')
print sunrise
print(loc.dusk(dt,local=False))
dusk=loc.dusk(dt,local=False)
sunset=dusk.strftime('%Y%m%d%H%M%S')
print sunset
folderlist=[]
print dt_path
print dt_path_y
print dt_path_t
folders = bucket.list(dt_path,"/")
folders_y = bucket.list(dt_path_y,"/")
folders_t= bucket.list(dt_path_t,"/")
folderlist.append(folders_y)
folderlist.append(folders)
folderlist.append(folders_t)
for folderl in folderlist:
    for folder in folderl:
        if folder.name.find(".gz")>0:
            filename= folder.name
            year=folder.name[20:24]
            month=folder.name[24:26]
            day=folder.name[26:28]
            time=folder.name[29:35]
            print folder.name[16:42]
            date_str = folder.name[20:35]
            date_str = re.sub('_', '', date_str)
            #print folder.key
            if (date_str>sunrise and date_str<sunset):
                #print "match"
                get_files.append(folder.key)

for l in get_files:
    keyl=bucket.get_key(l)
    keyString = keyl.name[16:42]
    if not os.path.exists(PATH+keyString):
        print "getting"+keyl.key
        keyl.get_contents_to_filename(PATH+keyString)
