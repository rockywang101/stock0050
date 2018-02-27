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

from com.funny.stockv2.StockEntity import StockInsertRecord, StockPrice
import csv

Base = declarative_base()

def queryDB():
    engine = create_engine('sqlite:///stock.sqlite', echo=False)
      
    Base.metadata.create_all(engine)
         
    Session = sessionmaker(bind=engine)
    session = Session()
      
    # 取所有在 db 裡的 stockId
    rows = session.query(StockInsertRecord.stockId).from_statement('SELECT distinct(stockId) FROM stock_insert_record')
#     rows = session.query(StockInsertRecord.stockId).from_statement('SELECT distinct(stockId) FROM stock_insert_record WHERE stockId = :stockId').params(stockId='9958')
    for r in rows:
        print(r[0])

        rows2 = session.query(StockPrice).filter_by(stockId=r[0]).order_by(text("id"))
        
        # a append, w write
        with open("data/"+r[0]+".csv", "w", newline="\n") as csvfile:
            writer = csv.writer(csvfile)
            for row2 in rows2:
                ym = int(row2.txDate[0:4]) - 1911
                ymd = str(ym) + "/" +  row2.txDate[4:6] + "/" + row2.txDate[6:8]
                newRow = [ymd, row2.txAmount, row2.txMoney, row2.openPrice, row2.highPrice, row2.lowPrice, row2.closePrice, row2.diffPrice, row2.txCount]
                writer.writerow(newRow)
      
    session.commit()
    
if __name__ == '__main__':
    queryDB()


