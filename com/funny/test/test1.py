'''
抓取今天的大盤資料並計算 RSA/K9 值，發 Line 到群組

因為一開始是用歷史資料，且這個資料是在公平交易所，應該比在 google 或 yahoo 更精準
後來發現有 http://mis.twse.com.tw/stock/fibest.jsp?stock=t00 可以查即時資料，應該 13:30 過後就變盤後資料
後續會再修正

Created on 2017年12月1日
@author: rocky.wang
'''
import datetime, requests, csv, os, time, json


def fetchStock(stockId):

    req = requests.Session()
    req.get("http://mis.twse.com.tw/stock/index.jsp")
    url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stockId}.tw&_={time}".format(stockId=stockId, time=int(time.time()) * 1000)
    r = req.get(url)

    try:
        return r.json()
    except json.decoder.JSONDecodeError:
        return {'rtmessage': 'json decode error', 'rtcode': '5000'}
    

now = datetime.datetime.now()
print("--------------------------------------------------")        
print("執行時間 %s" %(now.strftime("%Y-%m-%d %H:%M:%S")))
print("--------------------------------------------------")        

# 取今天民國年的字串 => 106/12/01
dt = datetime.date.today()
today = str(int(now.strftime("%Y")) - 1911) + now.strftime("/%m/%d")

print(today)

msg = ""

# 加上 0050 0056 股價
j = fetchStock("0050")
zStr = j.get("msgArray")[0].get("z")

dt = j.get("msgArray")[0].get('tk1').split(sep='_')[2]
print(dt)



j = fetchStock("t00")

dt = j.get("msgArray")[0].get('tk1').split(sep='_')[2]
print(dt)

zStr = j.get("msgArray")[0].get("z")
msg += "\n0056價格 %s" %(zStr)

z = float(j.get('msgArray')[0].get('z'))
y = float(j.get('msgArray')[0].get('y'))    

print("run completed.")