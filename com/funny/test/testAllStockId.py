'''

Created on 2018年1月23日
@author: rocky.wang
'''
import datetime, time, requests



def fetchAllStockFinalPrice(dt):
    # 不包含牛市xxx 的
    url = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=" + dt + "&type=ALLBUT0999&_=" + str(int(time.time() * 1000))
    print("GET " + url)
    
    stat = requests.get(url).json().get("stat")
    if stat == "OK":
        return requests.get(url).json()["data5"]    
    else:
        print("no data found")
        return None
    
dt = datetime.datetime.now().strftime("%Y%m%d")
dt = "20180123"
datas = fetchAllStockFinalPrice(dt)
if datas != None:
    for data in datas:
        if (data[0] == '0056'):
            print(data)
