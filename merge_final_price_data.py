'''
Created on 2018年2月27日
@author: rocky.wang
'''
import os, sys, csv, datetime

dt = datetime.datetime.now()

#dt = datetime.datetime(2018, 3, 1)

filename = "daily_price/{}.csv".format(dt.strftime("%Y%m%d"))

print(filename)

with open(filename, "r", encoding="utf-8") as f1:
    csvReader = csv.reader(f1)
    for row in csvReader:
        print(row)
        
        for i in range(len(row)):
            row[i] = row[i].replace(",", "")
        
        sign = " "
        if "green" in row[9]:
            sign = "-"
        elif "red" in row[9]:
            sign = "+"
        sign += row[10]
        
        ymd = str(int(dt.strftime("%Y")) - 1911) + "/" + dt.strftime("%m/%d")
        newRow = [ymd, row[2], row[4], row[5], row[6], row[7], row[8], sign, row[3]]
        
        with open("data/{}.csv".format(row[0]), "a", newline="\n", encoding="utf-8") as f2:
            csvWriter = csv.writer(f2)
            csvWriter.writerow(newRow)
        
        print("end %s" %(row[0]))