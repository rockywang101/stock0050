'''

Created on 2018年2月27日
@author: rocky.wang
'''
import csv, datetime

def string_to_time(string):
    print(string)
    year, month, day = string.split('/')
    return datetime(int(year) + 1911, int(month), int(day))

dict_row = {}
with open("9958.csv", "r") as f1:
    reader = csv.reader(f1)
    for row in reader:
        print(row[0])
        dict_row[row[0]] = row
        
# Sort by date
rows = [row for date, row in sorted(dict_row.items(), key=lambda x: string_to_time(x[0]))]

for row in rows:
    print(row)


