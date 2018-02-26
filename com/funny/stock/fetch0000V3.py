'''
即時與盤後統一抓取 TWSE，由時間判斷

改 return bean，尚未改完

Created on 2018年1月14日
@author: rocky.wang
'''
import datetime, requests, csv, os, time, bs4, lineTool, json
from textwrap import indent
from com.funny.bean.StockDiary import StockDairy


now = datetime.datetime.now()

print("--------------------------------------------------")        
print("程式啟動時間 %s" %(now.strftime("%Y-%m-%d %H:%M:%S")))
print("--------------------------------------------------")   

prettyPrint = False
k9High = 80
k9Low = 20
finalTime = "13:30:00"

isToday = False # 是否為當日資料
isFinal = False # 是否為盤後資料
isNotify = True # 是否要發通知

def fetchStock(stockId):

    s = requests.Session()
    s.get("http://mis.twse.com.tw/stock/index.jsp")
    url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stockId}.tw&_={time}".format(stockId=stockId, time=int(time.time()) * 1000)
    print("GET %s" %(url))
    r = s.get(url)

    try:
        if prettyPrint:
            print("%s\n" %(json.dumps(r.json(), indent=4)))
        else:
            print("%s\n" %(r.json()))
            
        return StockDairy(r.json())
    except json.decoder.JSONDecodeError:
        isNotify = False
        return {'rtmessage': 'json decode error', 'rtcode': '5000'}
    
stockDairy = fetchStock("2897")
h = stockDairy.get("h")
print(h)

stockDairy.myPrint(True)

