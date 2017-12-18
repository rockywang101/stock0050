'''
Demo Line Notify 發圖片 (on Windows)

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
    
    r = requests.post(url, headers = headers, params = payload, files=files)
    return r.status_code


token = os.environ["LINE_TEST_TOKEN"]
msg = "Hello Python"
#picURI = "C:\\Users\\Rocky\\git\\stock0050\\com\\funny\\test\\girlfriend.jpg" # 用下面的相對路徑也行 
picURI = "girlfriend.jpg"


lineNotify(token, msg, picURI)
