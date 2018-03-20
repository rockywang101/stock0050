'''
試算定期定額會怎樣

Created on 2018年3月9日
@author: Rocky
'''
import datetime, csv
from dateutil.relativedelta import relativedelta 

stockId = "5871"
salary = 20000
dt = datetime.date(2008, 1, 10)

''' 拿歷年配股配息資料 '''
def open_file(stockId):

    dt = datetime.datetime.now()
    # 初使
    data = {}
    for i in range(0, 50):
        year = dt.year - i
        data[str(year)] = [0.0, 0.0]

    with open("dataDividend/{}_dividendSchedule.csv".format(stockId)) as f1:
        csvReader = csv.reader(f1)
        for row in csvReader:
            data[row[1]][0] += float(row[10])
            data[row[1]][1] += float(row[13])
    
    data.pop('2018')
    return data
    
data = open_file(stockId)
print(data)



''' 拿股票價格 '''
priceMap = {}
with open("data/{}.csv".format(stockId)) as f1:
    reader = csv.reader(f1)
    for row in reader:
        priceMap[row[0]] = float(row[6])



# 現金/股數/當日股價/股票帳面價值/帳面總資產/投入總成本/目前總獲利/投報率/年化報酬率
li = [0, 0, 0.0, 0, 0, 0, 0, 0.0, 0.0]

#for i in range(36):
conti = True
i = 0
while conti:
    i += 1
    year = int((i) // 12) + 1
    print("投資年數 %s " %(year))
    
    dtKey = str(int(dt.strftime('%Y')) - 1911) + dt.strftime('/%m/%d')
    print("%s 投入現金 %s 準備進行投資" %(dt.strftime('%Y/%m/%d'), salary))
    # step 1 領薪水 n 元
    li[0] += salary
    
    price = None
    cnt = 1
    while price == None:
        price = priceMap.get(dtKey)
        dtKey = str(int(dt.strftime('%Y')) - 1911) + dt.strftime('/%m/') + str(int(dt.strftime('%d')) + cnt)
        cnt += 1
        
    li[2] = price # 當日股價
    li[3] = int(li[1] * li[2]) # 股票帳面價值
    li[4] = li[0] + li[3] # 帳面上總資產
    li[5] = li[5] + salary # 投入總成本
    li[6] = li[4] - li[5] # 目前總獲利
    li[7] = li[6] / li[5] # 投報率
    li[8] = (li[4] / li[5]) ** (1/year) - 1 # 年化報酬率
    li[7] = str(round(li[7] * 100, 2)) + "%"
    li[8] = str(round(li[8] * 100, 2)) + "%"
    
    print("現金/股數/當日股價/股票帳面價值/帳面總資產/投入總成本/目前總獲利/投報率/年化報酬率")
    print(li)
    ''' step 2 買股'''
    
    buyNum = int(li[0] / li[2]) # 可買股數
    money = int(buyNum * li[2])
    print("買入 %s 股，金額 %s" %(buyNum, money))
    li[0] = li[0] - money # 現金
    li[1] = li[1] + buyNum # 股數
    li[3] = int(li[1] * li[2]) # 股票帳面價值
    li[4] = li[0] + li[3] # 帳面上總資產
    li[6] = li[4] - li[5] # 目前總獲利
    li[7] = li[6] / li[5] # 投報率
    li[8] = (li[4] / li[5]) ** (1/year) - 1 # 年化報酬率
    li[7] = str(round(li[7] * 100, 2)) + "%"
    li[8] = str(round(li[8] * 100, 2)) + "%"
    
    print(li)
    
    ''' step 3 七月時進行配股配息 '''
    if dt.strftime("%m") == '07':
        
        m = data.get(dt.strftime("%Y"))[0]
        s = data.get(dt.strftime("%Y"))[1]
        
        addMoney = int(li[1] * m)
        addStock = int(li[1] / 10 * s)
        print("配息 %s, 配股 %s，金額 %s 股數 %s" %(m, s, addMoney, addStock))
        li[0] += addMoney
        li[1] += addStock
        # recal
        li[3] = int(li[1] * li[2]) # 股票帳面價值
        li[4] = li[0] + li[3] # 帳面上總資產
        li[6] = li[4] - li[5] # 目前總獲利
        li[7] = li[6] / li[5] # 投報率
        li[8] = (li[4] / li[5]) ** (1/year) - 1 # 年化報酬率
        li[7] = str(round(li[7] * 100, 2)) + "%"
        li[8] = str(round(li[8] * 100, 2)) + "%"
    
        print(li)
    
    # 往下個月
    dt = dt + relativedelta(months=1)
    print()
    
    if (dt.strftime("%Y%m") == "201803"):
        conti = False
    
