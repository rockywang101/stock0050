'''
Demo Line Notify 發圖片 (on Linux)

Created on 2017年12月19日
@author: rocky.wang
'''
import requests, os

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


token = os.environ["LINE_TEST_TOKEN"]
msg = "Hello Python"
picURI = "/data/data/com.termux/files/home/girlfriend.jpg"


lineNotify(token, msg, picURI)
