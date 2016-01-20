import csv
import datetime
with open('KAKQ_example.csv', 'rb') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if (len(row[0])==4 and str(row[3]).lower()=='y'):
            print row[0]
            print row[1]
            date=datetime.datetime.strptime(row[1],'%m/%d/%Y')
            print date
            print date.year
            print date.month
            print date.day
            print str(row[3]).lower()