'''
因為 sqlite 檔案太大，termux 裝 git-lfs 目前還有問題，加上後來思考也沒一定要資料庫複雜的 select 功能
寫隻把資料庫裡的個股價格轉成一個個 csv 檔案

Created on 2018年2月22日
@author: rocky.wang
'''

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.sql.expression import text

from com.funny.stockv2.StockEntity import StockPrice


Base = declarative_base()

def queryDB(stockId):
    engine = create_engine('sqlite:///stock.sqlite', echo=False)
      
    Base.metadata.create_all(engine)
         
    Session = sessionmaker(bind=engine)
    session = Session()
      
#     rows = session.query(StockPrice)
    
#     stat = text('select * from STOCK_PRICE where stockId = :stockId')
#     rows = session.query(StockPrice).from_statement(stat).params(stockId=stockId)
    
    #rows = session.query(StockInsertRecord).filter(StockInsertRecord.stockId=='2897').filter(StockInsertRecord.dt.like('2017%'))
    #rows = session.query(StockInsertRecord).filter(StockInsertRecord.stockId=='2897').filter(StockInsertRecord.result== 1).limit(3)
    
    #rows = session.query(StockInsertRecord).filter_by(stockId='2897').filter_by(dt='2017')
    
    # only order by id 不會有警告，但 id desc 就會
    #rows = session.query(StockPrice).filter_by(stockId='2897').order_by("id").limit(3)
    
    rows = session.query(StockPrice).filter_by(stockId=stockId).order_by(text("id desc")).limit(3)
    
    print("----")
    for row in rows:
        print(row)
      
#     for stockPrice in stockList:
#         session.add(stockPrice)
      
    session.commit()
    
if __name__ == '__main__':
    queryDB("0050")


