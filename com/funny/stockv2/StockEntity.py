'''
Created on 2018年1月23日
@author: rocky.wang
'''

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker

Base = declarative_base()

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
        
if __name__ == '__main__':
    
    ''' 此時只有建立 SQLAlchemy Engine 實例，還沒在記憶體內建立資料，
        只有第一個 SQL 指令被下達時，才會真正連接到資料庫內執行 '''
    #engine = create_engine('sqlite:///:memory:', echo=True)
    engine = create_engine('sqlite:///stock.sqlite', echo=True)
    #engine = create_engine('sqlite:////home/cookiemonster/cookies.db')
    #engine = create_engine('sqlite:///c:\Users\cookiemonster\cookies.db')

    
    ''' 真正建立表格是使用 Base.metadata.create_all(engine) '''
    Base.metadata.create_all(engine)
    

    # 資料庫還未沒有 user_1 的資料，此時的狀態被稱為 pending (事實上，共有 4 種狀態 Transient, Pending, Persistent, Detached)
    # 那甚麼時候這些資料才會被新增到資料庫內呢？只有進行 QUERY, COMMIT, FLUSH 時才會被寫入資料庫內。