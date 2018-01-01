'''
Created on 2018年1月1日
@author: rocky.wang
'''
import requests, json, time

def fetchStock(stockId):

    req = requests.Session()
    req.get("http://mis.twse.com.tw/stock/index.jsp")
    url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stockId}.tw&_={time}".format(stockId=stockId, time=int(time.time()) * 1000)
    r = req.get(url)

    try:
        return r.json()
    except json.decoder.JSONDecodeError:
        return {'rtmessage': 'json decode error', 'rtcode': '5000'}
    
j = fetchStock("3045")
print(j)   

print(j.get('msgArray')[0].get('c')) # stockId => 2891 
print(j.get('msgArray')[0].get('z')) # 今日收盤價
print(j.get('msgArray')[0].get('y')) # 昨日價格
 
z = float(j.get('msgArray')[0].get('z'))
y = float(j.get('msgArray')[0].get('y'))

diff = z - y
diffStr = "%.2f" %(diff)

if diff > 0:
    diffStr = "▲" + diffStr
elif diff < 0:
    diffStr = "▼" + diffStr

print(diffStr)    


precentDiff = diff / y * 100
preDiffStr = "%.2f" %(precentDiff) + "%"

print(preDiffStr)

print()

diffStr = diffStr + " (" + preDiffStr + ")"
print(diffStr)
    
