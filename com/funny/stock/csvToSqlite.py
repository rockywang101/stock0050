'''
Created on 2017年12月23日
@author: rocky.wang
'''
import csv, sqlite3

def insertRow(stockId, row):
    conn = sqlite3.connect("stock.sqlite")
    cursor = conn.cursor()
    print(row[0])
    sql = "insert into STOCK_DAILY (STOCK_ID, TX_DATE, OPEN_PRICE) VALUES (%s, %s, %s) " %(stockId, row[0], row[3])

    cursor.execute(sql)
    conn.commit()
    conn.close()
    
    pass




# with open("2897.csv") as fi:
#     reader = csv.reader(fi)
#     for row in reader:
#         insertRow("2897", row)



def ins():
    conn = sqlite3.connect("stock.sqlite")
    cursor = conn.cursor()
    sql = "insert into STOCK_DAILY (STOCK_ID, TX_DATE, OPEN_PRICE) VALUES (%s, %s, %s) " %("1234", '2017/08/12', 80.23)

    cursor.execute(sql)
    conn.commit()
    conn.close()
    
ins()