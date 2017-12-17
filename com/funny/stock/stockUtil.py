'''
Created on 2017年12月15日
@author: rocky.wang
'''
import requests, time, json


def fetchStock(stockId):

    req = requests.Session()
    req.get("http://mis.twse.com.tw/stock/index.jsp")
    url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stockId}.tw&_={time}".format(stockId=stockId, time=int(time.time()) * 1000)
    r = req.get(url)

    try:
        return r.json()
    except json.decoder.JSONDecodeError:
        return {'rtmessage': 'json decode error', 'rtcode': '5000'}
    
    
j = fetchStock("0056")

rtcode = j.get("rtcode")
msgArray = j.get("msgArray")[0]

print(msgArray.get("c") + " " + msgArray.get("n"))
print("開盤價：" + msgArray.get("o"))
print("最高價：" + msgArray.get("h"))
print("最低價：" + msgArray.get("l"))
print("最近成交價：" + msgArray.get("z")) # z or pz
print("累積成交量：" + msgArray.get("v"))


