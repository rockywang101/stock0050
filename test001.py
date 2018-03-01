'''
Created on 2018年2月28日

@author: Rocky
'''
import csv, datetime
from _collections import deque

def get_final_price_by_file(stockId):
    filename = "data/{}.csv".format(stockId)
    with open(filename, 'r') as f:
        try:
            lastrow = deque(csv.reader(f), 1)[0]
            return lastrow[6]
        except IndexError:  # empty file
            return None


def calRate(price:float, m:float, s:float):
    t = m * 1000 + s * 100 * price # 總獲利
    x = t / (price * 1000) * 100 # 總獲利 / 總成本
    return x
    #return format(x, ".2f")

def open_file(stockId):

    # i want to get final stock price by open csv file
    fname = "data/{}.csv".format(stockId)
    price = float(get_final_price_by_file(stockId))
    print("%s Price %s" %(stockId, price))
    
    dt = datetime.datetime.now()
    # 初使
    dict = {}
    for i in range(0, 30):
        year = dt.year - i
        dict[str(year)] = [0.0, 0.0]

    with open("dataDividend/{}_dividendSchedule.csv".format(stockId)) as f1:
        csvReader = csv.reader(f1)
        for row in csvReader:
            print(row)
            dict[row[1]][0] += float(row[10])
            dict[row[1]][1] += float(row[13])
    
    dict.pop('2018')
    print(dict)
    cnt = 1
    m = 0.0
    s = 0.0
    for key, value in dict.items():
        m += value[0]
        s += value[1]
        avg_m = m / float(cnt)
        avg_s = s / float(cnt)
        x = calRate(price, avg_m, avg_s)
        print("%s year %s" %(cnt, x))
        cnt += 1
        pass
    

open_file("2891")


