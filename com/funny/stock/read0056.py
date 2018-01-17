'''
我想知道買賣時機點有多少

Created on 2018年1月16日
@author: Rocky
'''
import collections
import datetime
import csv
import time

low = 23.0
hight = 25.0

buyCnt = 0
saleCnt = 0

haveStock = False

with open("0056.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        
        if (float(row[6]) <= low):
            print("%s 買，價格 %s" %(row[0], row[6]))
            buyCnt += 1
            haveStock = True
        elif (float(row[6]) >= hight):
            if haveStock:
                print("\n======%s 賣，價格 %s=====\n" %(row[0], row[6])) 
            saleCnt += 1
            haveStock = False
