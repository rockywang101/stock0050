'''
Created on 2018年2月27日
@author: rocky.wang
'''

data = {}
data["2017"] = "Hello 2017"

data["2017"] = "Hello World 2017"

data["2017"] = "Hell 2017"

# print(data)

import datetime, csv

dt = datetime.datetime.now()

ymd = str(int(dt.strftime("%Y")) - 1911) + "/" + dt.strftime("%m/%d")

# print(ymd)





from dateutil.relativedelta import relativedelta 

# 取得該月最後一天的收盤價
def fetchLastDayPrice(ym, stockId):
    price = None
    with open("data/{}.csv".format(stockId)) as f1:
        reader = csv.reader(f1)
        for row in reader:
            if row[0].startswith(ym):
                price = row[6]
    return price

def getDayPrice(ymd, stockId):
    price = None
    with open("data/{}.csv".format(stockId)) as f1:
        reader = csv.reader(f1)
        for row in reader:
            if int(row[0].replace("/", "")) > int(ymd.replace("/", "")):
                return price
            else:
                price = row[6]

ym = "106/12"
stockId = "0050"
price = fetchLastDayPrice(ym, stockId)
print("%s %s Price %s" %(stockId, ym, price))

print(getDayPrice("107/02/05", stockId))


yearNum = 2
dt = datetime.date.today()
# dt = dt + relativedelta(years=-1)
beginDate = datetime.date(dt.year-yearNum, 1, 1)
endDate = datetime.date(dt.year-1, 12, 31)
print("form %s to %s" %(beginDate, endDate))

while beginDate < endDate:
#     print(beginDate)
    beginDate += relativedelta(months=1)



