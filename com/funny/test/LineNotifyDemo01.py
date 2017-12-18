'''
Demo Line Notify 發表情符號

Created on 2017年12月19日
@author: rocky.wang
'''
import requests, os

"""
發送 Line Notify 訊息 + 表情符號
"""
def lineNotify(token, msg, stickerPackageId, stickerId):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token
    }
   
    payload = {"message": msg, "stickerPackageId": stickerPackageId, 'stickerId': stickerId}
    r = requests.post(url, headers = headers, params = payload)
    return r.status_code


token = os.environ["LINE_TEST_TOKEN"]
msg = "Hello Python"
stickerPackageId = 2
stickerId = 38

lineNotify(token, msg, stickerPackageId, stickerId)
