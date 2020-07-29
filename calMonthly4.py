'''
試算定期定額會怎樣

copy from calMonthly.py

因為除權息日程的表格欄位應該是有異動，如果抓新資料的話，舊程式應該也會有問題

因為沒有 1264 的價格資料，爬的時候好像也已經有點問題，改用 yahoo 的價格來試算看看

Created on 2018年3月9日
@author: Rocky
'''
import csv, datetime
from dateutil.relativedelta import relativedelta 
import yfinance as yf
from pandas_datareader import data as web
import time
 
stockId = '2884'

''' 拿歷年配股配息資料 '''

data = {}
rowList = list(csv.reader(open(f'dataDividend/{stockId}_dividendSchedule.csv', encoding='utf-8')))
for row in rowList:
    try:
        data[row[0]] = [float(row[14]), float(row[17])] # year => [money, stock]
    except:
        data[row[0]] = [float(row[10]), float(row[13])] # year => [money, stock]
print(data)


''' 拿股票價格 '''
priceMap = {}
ystockId = f'{stockId}.TW'

yf.pdr_override()
df = web.get_data_yahoo(ystockId, datetime.datetime.now() - relativedelta(years=10))
df.drop(['Adj Close'], axis=1, inplace=True)
for index, row in df.iterrows(): 
    dt = index.strftime('%Y/%m/%d')
    priceMap[dt] = round(row['Open'], 2)

time.sleep(1)
print(priceMap)
print('--------------')


salary = 20000
dt = datetime.date(2015, 1, 1)

# 現金/股數/當日股價/股票帳面價值/帳面總資產/投入總成本/目前總獲利/投報率/年化報酬率
li = [0, 0, 0.0, 0, 0, 0, 0, 0.0, 0.0]

#for i in range(36):
conti = True
i = 0
while conti:
    i += 1
    year = int((i) // 12) + 1
    print("投資年數 %s " %(year))
    
    dtKey = dt.strftime('%Y/%m/%d')
    print("%s 投入現金 %s 準備進行投資" %(dt.strftime('%Y/%m/%d'), salary))
    # step 1 領薪水 n 元
    li[0] += salary
    
    price = None
    cnt = 1
    while price == None:
        price = priceMap.get(dtKey)
        newD = str(int(dt.strftime('%d')) + cnt)
        dtKey = str(int(dt.strftime('%Y'))) + dt.strftime('/%m/') + newD.zfill(2)
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
    
    if (dt.strftime("%Y%m") == "202007"):
        conti = False
    
