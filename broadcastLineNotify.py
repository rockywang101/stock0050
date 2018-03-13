'''
六個群太累，群發訊息

Created on 2018年3月12日
@author: rocky.wang
'''
import os, requests
import time


"""
發送 Line Notify 訊息
"""
def lineNotify(token, msg, picURI):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token
    }
   
    payload = {'message': msg}
    files = {'imageFile': open(picURI, 'rb')}
    r = requests.post(url, headers = headers, params = payload, files = files)
    return r.status_code

donotNotify = True # 避免誤按，發完請改回 True

tokenList = [os.environ["LINE_0050_TOKEN"], os.environ["LINE_0050_TOKEN2"], os.environ["LINE_0050_TOKEN3"], os.environ["LINE_0050_TOKEN4"], os.environ["LINE_0050_TOKEN5"], os.environ["LINE_0050_TOKEN6"]]

for token in tokenList:
    
    if donotNotify:
        continue
    
    print(token)
    msg = "分享覺得不錯的 app 給大家，目前正新跟亞泥都在相對低價，可自行參考 app"
    picURI = "Screenshot_20180312-132319.jpg"

    lineNotify(token, msg, picURI)
    
    time.sleep(2)
    