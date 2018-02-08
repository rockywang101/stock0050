'''

查詢 stock_insert_record 還未有資料的

Created on 2018年1月23日
@author: rocky.wang
'''
import requests, os

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append("/data/data/com.termux/files/home/stock0050")
from com.funny.stockv2.TWSEFetcher import TWSEFetcherEx

Base = declarative_base()
engine = create_engine('sqlite:///stock.sqlite', echo=False)
Base.metadata.create_all(engine)
         

class StockPrice(Base):
    
    __tablename__ = 'STOCK_PRICE'
    
    id = Column(Integer, primary_key=True)
    stockId = Column(String) # 股票代號
    txDate = Column(String) # 交易日期
    txCount = Column(Integer) # 成交筆數
    txAmount = Column(Integer) # 成交股數
    txMoney = Column(Integer) # 成交金額
    openPrice = Column(Float)
    highPrice = Column(Float)
    lowPrice = Column(Float)
    closePrice = Column(Float)
    diffPrice = Column(String) # 漲跌價差
    
    def __repr__(self):
        return "StockPrice ('{}', '{}', {}, {})".format(
            self.id,
            self.stockId,
            self.txDate,
            self.txCount
        )
        

class StockInsertRecord(Base):
    
    __tablename__ = 'stock_insert_record'
    
    id = Column(Integer, primary_key=True)
    stockId = Column(String) # 股票代號
    dt = Column(String) # 交易日期
    result = Column(Integer) # 成交筆數
    
    def __repr__(self):
        return "StockInsertRecord ('{}', '{}', {}, {})".format(
            self.id,
            self.stockId,
            self.dt,
            self.result
        )
        
import csv

# 取得目前 py 檔的資料夾路徑   (os.getwcd() 會取得執行 bat 的目錄，不能用它)
ph = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(ph, "all.csv")

dateDict = {}
with open(filename) as f1:
    reader = csv.reader(f1)
    for row in reader:
        dt = row[1].replace("/", "")
        if dt < "19920101":
            dt = "19920101" # twse 歷史資料最早只能查到這裡
        dateDict[row[0]] = dt

import datetime, time

def fetchAllStockFinalPrice(dt=datetime.datetime.now().strftime("%Y%m%d")):
    # 不包含牛市xxx 的
    url = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=" + dt + "&type=ALLBUT0999&_=" + str(int(time.time() * 1000))
    print("GET " + url)
    
    stat = requests.get(url).json().get("stat")
    if stat == "OK":
        return requests.get(url).json()["data5"]    
    else:
        print("no data found")
        return None


allStockIds = []
datas = fetchAllStockFinalPrice()
if datas != None:
    for data in datas:
        allStockIds.append(data[0])

print("sleep 2 seconds to be continue...")
time.sleep(2)
print()

# 測試所有的 stockId 都能拿到日期
cnt = 1
for id in allStockIds:
    dt = dateDict.get(id)
    cnt += 1


''' write to db '''
def insertDB(stockList, stockId, dt, test=False):
    
    Session = sessionmaker(bind=engine)
    session = Session()
      
    for stockPrice in stockList:
        session.add(stockPrice)
        
    if test:
        raise Exception
    
    rows = session.query(StockInsertRecord).filter_by(stockId=stockId).filter_by(dt=dt)

    if rows.count() != 1:
        raise Exception("month record not one")
    
    rows[0].result = 1
      
    session.commit()

def fetchMonthPrice(stockId, dt):
    
    fetcher = TWSEFetcherEx()
    data = fetcher.fetch(dt, stockId)
     
    stockList = []
    for d in data:
        dd = d[0].strip().split("/")
        d0 = str(int(dd[0]) + 1911) + dd[1] + dd[2]
        stockPrice = StockPrice(stockId=stockId, txDate=d0, txCount=d[8], txAmount=d[1], txMoney=d[2], openPrice=d[3], highPrice=d[4], lowPrice=d[5], closePrice=d[6], diffPrice=d[7])
        stockList.append(stockPrice)
        
    insertDB(stockList, stockId, dt)

from dateutil.relativedelta import relativedelta

'''
從開始日期一直取最新資料
'''
def fetchAllPrice(sid, startDate):
    
    y = int(startDate[0:4])
    m = int(startDate[4:6])
    
    beginDate = datetime.date(y, m, 1)
    today = datetime.datetime.now().strftime("%Y%m%d")
    
    while (beginDate.strftime('%Y%m%d') <= today):
        
        dt = beginDate.strftime('%Y%m')
        
        fetchMonthPrice(sid, dt)
        
        time.sleep(15)
        beginDate += relativedelta(months = 1)   # 月份 +1
    


Session = sessionmaker(bind=engine)
session = Session()

stockId = "2897"
rows = session.query(StockInsertRecord).filter_by(result=0).order_by("id")

for row in rows:
    fetchMonthPrice(row.stockId, row.dt)
    print("\n%s %s completed, sleep 5 to continue...\n" %(row.stockId, row.dt), flush=True)
    time.sleep(5)
    

# 從 testInsert4 改，不以個檔，改以 stock_insert_record 去 for loop
# sid = "2897"
# startDate = dateDict[sid]
# beginTime = int(time.time()*1000)
# fetchAllPrice(sid, startDate)
# endTime = int(time.time()*1000)
# spentTime = int((endTime - beginTime) / 1000)
# print("執行花費時間 %s (秒)" %(spentTime))
