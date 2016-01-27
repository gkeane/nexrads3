import dateutil.parser as parser
import boto
import boto.s3
import sys, os
import re
import sys
import astral
import csv
import pytz
import argparse
from datetime import datetime
from datetime import date, timedelta



LOCAL_PATH = './aws/'

def get_s3_files(radar,year,month,day):
    with open('input/radar_sites.csv', 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)

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

    loc=astral.Location( ('','',lat,long,elev,'') )

    PATH=LOCAL_PATH+filepath
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    conn = boto.s3.connect_to_region('us-east-2')
    conn = boto.connect_s3(anon=True)
    bucket = conn.get_bucket('noaa-nexrad-level2')
    get_files=[]
    dawn=loc.sunset(dt,local=False)
    start=dawn.strftime('%Y%m%d%H%M%S')
    print("Start Time: "+str(dawn))
    dusk=dawn+timedelta(hours=4)
    end=dusk.strftime('%Y%m%d%H%M%S')
    print("End Time: "+str(dusk))
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
    for folderl in folderlist:
        for folder in folderl:
            if folder.name.find(".gz")>0:
                filename= folder.name
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
    args = aparser.parse_args()
    radar = args.radar_site
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
    get_s3_files(radar,year,month,day)
