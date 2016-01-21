import dateutil.parser as parser
import argparse
import csv
import datetime
import nexrad_s3
aparser = argparse.ArgumentParser()
aparser.add_argument('infile', help='File to parse and load')
args = aparser.parse_args()
infile=args.infile
with open(infile, 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if (len(str(row[0]).strip())==4 and str(row[3]).strip().lower()=='y'):
            date=parser.parse(row[1])
            #print(date)
            radar=row[0]
            y=(date.strftime('%Y'))
            m=(date.strftime('%m'))
            d=(date.strftime('%d'))
            print('Loading '+radar+ ' '+str(date))
            nexrad_s3.get_s3_files(radar,y,m,d)
