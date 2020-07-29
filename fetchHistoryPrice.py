'''
抓取個股全部歷史股價

Created on 2017年12月22日
@author: rocky.wang
'''
import collections
import datetime
import csv
import time
from dateutil.relativedelta import relativedelta
from com.funny.stock.TWSEFetcher import TWSEFetcher


sid = "1264"

beginDate = datetime.date(1999, 1, 1)
today = datetime.date.today()

list1 = []

while (beginDate <= today):
    list1.append(beginDate.strftime('%Y%m'))
    beginDate += relativedelta(months = 1)   # 月份 +1

fetcher = TWSEFetcher() 

info = {}
conti = True

cnt = 1
while conti:
    print("第 %s 次執行 " %(cnt))
    cnt += 1
    
    print(list1)
    # 最後一筆
    if len(list1) == 1:
        ym = list1[0]
        data = fetcher.fetch(ym, sid)
        info[ym] = data
        conti = False
        break
    elif len(list1) == 0:
        conti = False
        break
    
    pos = int(len(list1) / 2)
    ym = list1[pos]
    data = fetcher.fetch(ym, sid)
    
    # 沒有值，向前移除全部
    if data == None:
        # 把自己和更之前的全移除掉
        list1 = list1[pos+1: len(list1)]
        print("no data, short list1 size => %s" %(len(list1)))
        print(list1)
        time.sleep(5)
        continue

    # 有值，向後逐月取股票資訊
    info[ym] = data
    
    for i in range(pos+1, len(list1)):
        ym = list1[i]
        data = fetcher.fetch(ym, sid)
        info[ym] = data
        time.sleep(5)
    
    # 把自己和後面的移除掉
    list1 = list1[0: pos]
    print("移除已抓取過的月份 list1 siez => %s" %(len(list1)))
    print(list1)


od = collections.OrderedDict(sorted(info.items()))

with open(sid+".csv", "a", newline="\n") as csvfile:
    writer = csv.writer(csvfile)
    for key in od: 
        if od[key] == None:
            pass
        else:
            for row in od[key]:
                writer.writerow(row)
            
            
print("completed")
