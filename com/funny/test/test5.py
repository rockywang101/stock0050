'''
Created on 2017年12月22日
@author: rocky.wang
'''

import datetime
import requests
import json
import csv
import time

from dateutil.relativedelta import relativedelta

beginDate = datetime.date(2017, 10, 1)
#beginDate = datetime.date(2017, 11, 1)
today = datetime.date.today()


list1 = []

while (beginDate <= today):
    list1.append(beginDate.strftime('%Y%m%d'))
    beginDate += relativedelta(months=1)   # 月份 +1

# for dt in list1:
#     print(dt.strftime('%Y%m%d'))

bingo = "20171001"
continueFind = True

print('total leng %s' %(len(list1)))
print(list1)

cnt = 0
while continueFind:
    cnt += 1
    print("%s times \n" %(cnt))
    pos = (int) (len(list1) / 2)
    print('get pos %s' %(pos))
    dt = list1[pos]
    
    print('get pos %s, dt %s' %(pos, dt))
    
    if bingo == dt:
        continueFind = False
        print('find it %s' %(dt))
    else:
        list1 = list1[0 : pos]
        print(list1)
        
        print('list1 size => %s' %(len(list1)))
        
    
def fetchData(): 
    list = []
    
    
li = []

di = {}

di["a1"] = [0, 2, 4]

print(di)

li.append([0, 2, 4])

print(li)










    
