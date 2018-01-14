'''
即時與盤後統一抓取 TWSE，由時間判斷

Created on 2018年1月14日
@author: rocky.wang
'''
import datetime, requests, csv, os, time, bs4, lineTool, json
from textwrap import indent

def fetchStock(stockId):

    s = requests.Session()
    s.get("http://mis.twse.com.tw/stock/index.jsp")
    url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stockId}.tw&_={time}".format(stockId=stockId, time=int(time.time()) * 1000)
    print("GET " + url)
    r = s.get(url)

    try:
        return r.json()
    except json.decoder.JSONDecodeError:
        return {'rtmessage': 'json decode error', 'rtcode': '5000'}
    
j = fetchStock("t00")
print(j)
print(json.dumps(j, indent=4))

time.sleep(1)

j = fetchStock("2891")
print(j)
print(json.dumps(j, indent=4))


