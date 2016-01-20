import csv
with open('input/radar_sites.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)

for i in your_list:
    if i[0]=='TJFK':
        lat=i[1]
        long=i[2]
        elev=i[3]

print lat
print long
print elev