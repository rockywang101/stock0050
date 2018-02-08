'''

查詢 stock_insert_record 還未有資料的

Created on 2018年1月23日
@author: rocky.wang
'''
import requests

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker
from com.funny.stock.TWSEFetcher import TWSEFetcher
from com.funny.stockv2.TWSEFetcher import TWSEFetcherEx

Base = declarative_base()
engine = create_engine('sqlite:///stock.sqlite', echo=False)
Base.metadata.create_all(engine)

class StockInsertRecord(Base):
    
    __tablename__ = 'stock_insert_record'
    
    id = Column(Integer, primary_key=True)
    stockId = Column(String) # 股票代號
    dt = Column(String) # 交易日期
    result = Column(Integer) # 成交筆數
    
    def __repr__(self):
        return "StockInsertRecord {}, {}, {}".format(
            self.stockId,
            self.dt,
            self.result
        )
        

      
    
Session = sessionmaker(bind=engine)
session = Session()

stockId = "2897"
rows = session.query(StockInsertRecord).filter_by(result=0).order_by("id")

# for row in rows:
#     print(row)

