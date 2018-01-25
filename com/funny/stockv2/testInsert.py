'''
Created on 2018年1月23日
@author: rocky.wang
'''
from com.funny.stockv2.StockEntity import StockPrice
import requests

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker


sid = "0056"

url = "http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20180101&stockNo=" + sid

r = requests.get(url)
j = r.json()

print(j.get("data"))

stockList = []
for d in j.get("data"):
    
    stockPrice = StockPrice(stockId=sid, txDate=d[0], txCount=d[8], txAmount=d[1], txMoney=d[2], openPrice=d[3], highPrice=d[4], lowPrice=d[5], closePrice=d[6], diffPrice=d[7])
    print(stockPrice)
    
    stockList.append(stockPrice)
    
''' write to db '''
    
Base = declarative_base()

engine = create_engine('sqlite:///stock.sqlite', echo=True)

Base.metadata.create_all(engine)
   
Session = sessionmaker(bind=engine)
session = Session()

for stockPrice in stockList:
    session.add(stockPrice)

session.commit()
    
        