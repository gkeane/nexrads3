import dateutil.parser as parser
import boto
import boto.s3
import sys, os
import re
import sunset
import sys
import astral
import csv
import pytz
import argparse
from datetime import datetime
from astral import Astral
from datetime import date, timedelta



LOCAL_PATH = './aws/'

def get_s3_files(radar,year,month,day,sstray=-2,estray=4,sunrise=False,dir=LOCAL_PATH):
    with open('./input/radar_sites.csv', 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    lat=0
    long=0
    for i in your_list:
        if i[0]==radar:
            lat=i[1]
            long=i[2]
            elev=i[3]
    if (lat==0 and long==0):
        print("Radar Location not found in input")
        return False

    ymd=year+month+day
    filepath = '/'+radar+'/'+year+'/'
    dt = date_object = datetime.strptime(ymd,'%Y%m%d')
    dt_path=dt.strftime('%Y')+'/'+dt.strftime('%m')+'/'+dt.strftime('%d')+'/'+radar+'/'
    dt_y=dt-timedelta(days=1)
    dt_path_y=dt_y.strftime('%Y')+'/'+dt_y.strftime('%m')+'/'+dt_y.strftime('%d')+'/'+radar+'/'
    dt_t=dt+timedelta(days=1)
    dt_path_t=dt_t.strftime('%Y')+'/'+dt_t.strftime('%m')+'/'+dt_t.strftime('%d')+'/'+radar+'/'
    ast = Astral()
    loc=astral.Location( ('','',lat,long,elev,'EST') )
    timezone = loc.timezone
    #print('Timezone: %s' % timezone)
    #sun2=ast.dawn_utc(dt,lat,long)
    #print(sun2)
    PATH=dir+filepath
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    conn = boto.s3.connect_to_region('us-east-2')
    conn = boto.connect_s3(anon=True)
    bucket = conn.get_bucket('noaa-nexrad-level2')
    get_files=[]
    if sunrise:
        print "sunrise"
        sunsets=sunset.sunrise(lat,long,dt)
    else:
        sunsets=sunset.sunset(lat,long,dt)
    #print(sunsets.utcoffset())
    star=sunsets.strftime('%Y%m%d%H%M%S')
    interval_type = 'hours'
    delta=timedelta(**{interval_type: sstray})
    delta2=timedelta(**{interval_type: estray})
    #print("delta2"+(str(delta2)))
    start_dt=sunsets+delta
    start=start_dt.strftime('%Y%m%d%H%M%S')
    equal = True
    #print start_dt.day;
    #print dt.day;
    if (start_dt.day!=dt.day): #does start date happen tomorrow, if so download one from today
        print "Start happens tomorrow!!!!!!"
        equal = False
    print("Start Time: "+str(start_dt))
    sunset2=sunsets+delta2
    end=sunset2.strftime('%Y%m%d%H%M%S')
    print("End Time: "+str(sunset2))
    folderlist=[]
    #print(dt_path)
    #print(dt_path_y)
    #print(dt_path_t)
    folders = bucket.list(dt_path,"/")
    folders_y = bucket.list(dt_path_y,"/")
    folders_t= bucket.list(dt_path_t,"/")
    folderlist.append(folders_y)
    folderlist.append(folders)
    folderlist.append(folders_t)
    if (equal==False):                  #add last one from today to download
        getapp_name = "00000"
        getapp_key = min(folders).key
        for folder in folders:
            if (folder.name.find(".gz")>0 or folder.name.find("_V0")>0):
                if (folder.name>getapp_name):
                    #print folder.name
                    getapp_name = folder.name
                    getapp_key = folder.key
        get_files.append(getapp_key)
    for folderl in folderlist:
	#print folderl;
        for folder in folderl:
	    #print folder.name
            if (folder.name.find(".gz")>0 or folder.name.find("_V0")>0):
                #print "inif"
		filename= folder.name
		#print filename;
                year=folder.name[20:24]
                month=folder.name[24:26]
                day=folder.name[26:28]
                time=folder.name[29:35]
                #print folder.name[16:42]
                date_str = folder.name[20:35]
                date_str = re.sub('_', '', date_str)
                #print folder.key
                if (date_str>start and date_str<end):
                    #print "match"
                    get_files.append(folder.key)

    for l in get_files:
        keyl=bucket.get_key(l)
        keyString = keyl.name[16:42]
        if not os.path.exists(PATH+keyString):
            print("Downloading: "+keyl.key)
            keyl.get_contents_to_filename(PATH+keyString)


if __name__ == '__main__':
    # test1.py executed as script
    # do something

    radar=''
    year=''
    month=''
    day=''
    total = len(sys.argv)
    cmdargs = str(sys.argv)
    #print("The total numbers of args passed to the script: %d " % total)
    #print("Args list: %s " % cmdargs)
    # Pharsing args one by one
    aparser = argparse.ArgumentParser()
    aparser.add_argument('radar_site',type=str, help='4 char radar site')
    aparser.add_argument('year',type=str, help='4 char year')
    aparser.add_argument('month', type=str,help='2 char zero padded month ex: 02')
    aparser.add_argument('day', type=str,help='2 char zero padded day ex:09')
    aparser.add_argument('-s','--sstray', type=int,default=0,help='start stray from sunset(or sunrise) negative for before')
    aparser.add_argument('-e','--estray', type=int,default=4,help='end stray from sunset (or sunrise)')
    aparser.add_argument('--sunrise', dest='sunrise', action='store_true', help='enable calculations based on sunrise')
    aparser.set_defaults(sunrise=False)
    args = aparser.parse_args()
    radar = args.radar_site
    sstray = args.sstray
    estray = args.estray
    sunrise = args.sunrise
    #print(sunrise)
    if (len(radar)<4):
        sys.exit("radar value too short")
    year = args.year
    if (len(year)<4):
        sys.exit("year value too short")
    month = args.month
    if (len(month)<2):
        sys.exit("month value too short (zero padded?)")
    day = args.day
    if (len(day)<2):
        sys.exit("day value too short (zero padded?)")
    lat = 0
    long = 0
    elev = 0
    get_s3_files(radar,year,month,day,sstray,estray,sunrise)
