import dateutil.parser as parser
import argparse
import csv
import datetime
import nexrad_s3
import mysql.connector
import config
import time
from quicklock import singleton

singleton('awsdb')
try:
    cnx = mysql.connector.connect(user=config.user, database=config.database,password=config.password)
    cursor = cnx.cursor()
    inscursor = cnx.cursor()
    query = ("SELECT ID_SCREEN,RADAR,DATE FROM screening_master WHERE Download=1 and Downloaded IS NULL ")
    cursor.execute(query)
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))

for (id_screen,radar,date) in cursor:
        y=(date.strftime('%Y'))
        m=(date.strftime('%m'))
        d=(date.strftime('%d'))
        print('Loading '+radar+ ' '+str(date))
        nexrad_s3.get_s3_files(radar,y,m,d)
        try:
            inscursor.execute("UPDATE screening_master set downloaded=%s WHERE ID_SCREEN=%s" % ('now()',id_screen))
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
print "done"
cnx.commit();
inscursor.close()
cursor.close()
cnx.close()