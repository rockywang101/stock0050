'''
取得所有個股的盤後資料

Created on 2018年2月22日
@author: rocky.wang
'''
import time, datetime, requests, json
from dateutil.relativedelta import relativedelta

def fetch_all_stock_final_data(dt=None):

    if dt==None:
        now = datetime.datetime.now()
        if now.strftime("%H%M") < "1330":
            now += relativedelta(days = -1)
        dt = now.strftime("%Y%m%d")    
        
    t = int(time.time()*1000)
    url = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=%s&type=ALLBUT0999&_=%s" %(dt, t)
    r = requests.get(url)
    print("GET %s" %(url))
    print("Response => %s" %(r.text))
    
    js = json.loads(r.text)
    if js.get("stat") == "很抱歉，沒有符合條件的資料!":
        print("無資料，再往前一天的資料查詢")
        time.sleep(1)
        now += relativedelta(days = -1) # 再往前一天
        dt = now.strftime("%Y%m%d") 
        fetch_all_stock_final_data(dt)
    else:
        print(js.get("fields5"))
        for i in range(3):
            print(js.get("data5")[i])

if __name__ == "__main__":
    fetch_all_stock_final_data()