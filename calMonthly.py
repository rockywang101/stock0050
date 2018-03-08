'''
試算定期定額會怎樣

Created on 2018年3月9日
@author: Rocky
'''
import datetime, csv
from dateutil.relativedelta import relativedelta 

stockId = "2891"
salary = 10000


''' 拿股票價格 '''
priceMap = {}
with open("data/{}.csv".format(stockId)) as f1:
    reader = csv.reader(f1)
    for row in reader:
        priceMap[row[0]] = float(row[6])



# 現金 / 股數 / 當日股價 / 股票帳面價值 / 帳面總資產 / 投入總成本 / 目前總獲利 / 投報率
li = [0, 0, 0.0, 0, 0, 0, 0, 0.0]

dt = datetime.date(2015, 1, 10)

for i in range(36):
    
    dtKey = str(int(dt.strftime('%Y')) - 1911) + dt.strftime('/%m/%d')
    print(dt.strftime('%Y/%m/%d'))
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
    
    print(li)
    ''' step 2 買股'''
    # step 2 買股
    
    buyNum = int(li[0] / li[2]) # 可買股數
    money = int(buyNum * li[2])
    print("買入 %s 股，金額 %s" %(buyNum, money))
    li[0] = li[0] - money # 現金
    li[1] = li[1] + buyNum # 股數
    li[3] = int(li[1] * li[2]) # 股票帳面價值
    li[4] = li[0] + li[3] # 帳面上總資產
    li[6] = li[4] - li[5] # 目前總獲利
    li[7] = li[6] / li[5] # 投報率
    print(li)
    
    # 往下個月
    dt = dt + relativedelta(months=1)
    print()
    
    
    
