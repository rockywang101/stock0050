'''
取得所有個股的盤後資料

改到根目錄下的 crawl_all_final_price，這隻是還可以往前爬，先保留著

Created on 2018年2月22日
@author: rocky.wang
'''
import time, datetime, requests, json
from dateutil.relativedelta import relativedelta

def fetch_all_stock_final_data(dt=None):
    # 沒傳入日期，預設為今日，且若還沒超過下午一點半，取昨日
    if dt==None:
        dt = datetime.datetime.now()
        if dt.strftime("%H%M") < "1330":
            print("未到一點半，取前一天日期")
            dt += relativedelta(days = -1)
        
    t = int(time.time()*1000)
    url = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=%s&type=ALLBUT0999&_=%s" %(dt.strftime("%Y%m%d"), t)
    r = requests.get(url)
    print("GET %s" %(url))
    print("Response => %s" %(r.text))
    
    js = json.loads(r.text)
    if js.get("stat") == "很抱歉，沒有符合條件的資料!":
        print("%s 無資料，再往前一天的資料查詢\n " %(dt.strftime("%Y%m%d")))
        time.sleep(2) # 其實睡一秒就夠了，但我怕過年時連休較多會被擋
        dt += relativedelta(days = -1) # 再往前一天
        fetch_all_stock_final_data(dt)
    else:
        print(js.get("subtitle1"))
        print(js.get("fields5"))
        for i in range(3):
            print(js.get("data5")[i])
#         for i in js.get("data5"):
#             print(i)            

if __name__ == "__main__":
    fetch_all_stock_final_data()