'''
抓取所有各股 (不含牛市，權證)收盤價

應用：列出價格低於 5 元的水餃股

Created on 2018年2月7日
@author: rocky.wang
'''
import time, datetime, requests, json

now = datetime.datetime.now()

t = int(time.time()*1000)
dt = now.strftime("%Y%m%d")
url = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=%s&type=ALLBUT0999&_=%s" %(dt, t)
print(url)
r = requests.get(url)
print(r.text)
js = json.loads(r.text)
print(js.get("fields5"))

''' 列出價格低於 5 元的水餃股 '''
for data in js.get("data5"):
    try:        
        if float(data[8]) < 5:
            print("%s %s 價格 %s" %(data[0], data[1], data[8]))
    except:
        #print(data)
        pass
