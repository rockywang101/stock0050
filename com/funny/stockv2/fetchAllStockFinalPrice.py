'''
抓取所有各股 (不含牛市，權證)收盤價

Created on 2018年2月7日
@author: rocky.wang
'''
import time, datetime, requests, json

now = datetime.datetime.now()

t = int(time.time()*1000)
dt = now.strftime("%Y%m%d")
dt = 20180206
# http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=20180206&type=ALLBUT0999&_=1517935437237
url = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=%s&type=ALLBUT0999&_=%s" %(dt, t)
print(url)
r = requests.get(url)
print(r.text)

js = json.loads(r.text)

for data in js.get("data5"):
    print(data)
    
'''
  "subtitle1": "107年02月06日 大盤統計資訊",
  "fields5": [
    "證券代號",
    "證券名稱",
    "成交股數",
    "成交筆數",
    "成交金額",
    "開盤價",
    "最高價",
    "最低價",
    "收盤價",
    "漲跌(+/-)",
    "漲跌價差",
    "最後揭示買價",
    "最後揭示買量",
    "最後揭示賣價",
    "最後揭示賣量",
    "本益比"
  ],
  '''
    

