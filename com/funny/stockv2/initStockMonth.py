'''
Created on 2018年1月23日
@author: rocky.wang
'''
import requests

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref, sessionmaker

from com.funny.stock.TWSEFetcher import TWSEFetcher

Base = declarative_base()

class stockInsertRecord(Base):
    
    __tablename__ = 'stock_insert_record'
    
    id = Column(Integer, primary_key=True)
    stockId = Column(String) # 股票代號
    dt = Column(String) # 交易日期
    result = Column(Integer)
    
    __table_args__ = (
            UniqueConstraint('stockId', 'dt', name='_customer_location_uc'),
            )

import csv

dateDict = {}
with open("all.csv") as f1:
    reader = csv.reader(f1)
    for row in reader:
        dt = row[1].replace("/", "")
        if dt < "19920101":
            dt = "19920101" # twse 歷史資料最早只能查到這裡
        dateDict[row[0]] = dt

import datetime, time

# 為了可以抓出所有不含牛市的股票代號
def fetchAllStockFinalPrice(dt=datetime.datetime.now().strftime("%Y%m%d")):
    # 不包含牛市xxx 的
    dt = "20180124"
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

# 測試所有的 stockId 都能拿到日期
cnt = 1
for id in allStockIds:
    dt = dateDict.get(id)
    #print("%s\t%s\t%s" %(cnt, id, dt))
    cnt += 1

''' write to db '''
def insertDB(stockInsertRecordList):
    engine = create_engine('sqlite:///stock.sqlite', echo=False)
      
    Base.metadata.create_all(engine)
         
    Session = sessionmaker(bind=engine)
    session = Session()
      
    for stockInsertRecord in stockInsertRecordList:
        session.add(stockInsertRecord)
      
    session.commit()

from dateutil.relativedelta import relativedelta

'''
從開始日期一直取最新資料
'''
def fetchAllMonth(sid, startDate):
    
    y = int(startDate[0:4])
    m = int(startDate[4:6])
    
    beginDate = datetime.date(y, m, 1)
    today = datetime.datetime.now().strftime("%Y%m%d")

    stockInsertRecordList = []    
    while (beginDate.strftime('%Y%m%d') <= today):
        dt = beginDate.strftime('%Y%m')
        s = stockInsertRecord(stockId=sid, dt=dt, result=0)
        stockInsertRecordList.append(s)
        beginDate += relativedelta(months = 1)   # 月份 +1
        
    insertDB(stockInsertRecordList)
    
tatalCnt = len(allStockIds)
cnt = 1
print(allStockIds)
for sid in allStockIds:
    print("run %s ||| %s of %s stocks" %(sid, cnt, tatalCnt))
    cnt += 1
    startDate = dateDict[sid]
    
    beginTime = int(time.time()*1000)
    fetchAllMonth(sid, startDate)
    endTime = int(time.time()*1000)

    spentTime = int((endTime - beginTime) / 1000)
    print("執行花費時間 %s (秒)" %(spentTime))
    print("run %s of %s stocks end" %(cnt, tatalCnt))
