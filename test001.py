'''
Created on 2018年2月28日

@author: Rocky
'''
import csv, datetime

def fetch(stockId):
    
    dt = datetime.datetime.now()
    # 初使
    dict = {}
    for i in range(0, 30):
        year = dt.year - i
        dict[str(year)] = [0.0, 0.0]
    print(dict)
    with open("dataDividend/{}_dividendSchedule.csv".format(stockId)) as f1:
        csvReader = csv.reader(f1)
        for row in csvReader:
            print(row)
            dict[row[1]][0] += float(row[10])
            dict[row[1]][1] += float(row[13])
    
    print(dict)

fetch("0050")





