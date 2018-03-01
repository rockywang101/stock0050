'''
由 test001 改，判斷 0050 成份股，排序殖利率

Created on 2018年2月28日
@author: rocky.wang
'''
import csv, datetime
from _collections import deque
import os, lineTool

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
    z = get_final_price_by_file(stockId)
#     print("%s [%s] " %(stockId, z))

    try:
        price = float(z)
    except:
        price = 100000
    
    dt = datetime.datetime.now()
    # 初使
    dict = {}
    for i in range(0, 50):
        year = dt.year - i
        dict[str(year)] = [0.0, 0.0]

    with open("dataDividend/{}_dividendSchedule.csv".format(stockId)) as f1:
        csvReader = csv.reader(f1)
        for row in csvReader:
            dict[row[1]][0] += float(row[10])
            dict[row[1]][1] += float(row[13])
    
    dict.pop('2018')
    cnt = 1
    m = 0.0
    s = 0.0
    li = []
    for key, value in dict.items():
        m += value[0]
        s += value[1]
        avg_m = m / float(cnt)
        avg_s = s / float(cnt)
        x = calRate(price, avg_m, avg_s)
        li.append(x)
#         print("%s year %s" %(cnt, x))
        cnt += 1
        pass
    
    return li

# li = open_file("2891")

if __name__ == '__main__':
    
    with open("0050composition.csv", "r", encoding="utf-8") as f1:
        reader = csv.reader(f1)
        msg = ""
        for row in reader:
            stockId = row[0]
        
            li = open_file(stockId)
            
            cond = 8
            if li[2] > cond and li[4] > cond:
                msg += "\n%s %s  平均殖利率  三年  %.2f 五年  %.2f" %(stockId, row[1], li[2], li[4])
                
        
        print(msg)        
#         lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], msg)
    
