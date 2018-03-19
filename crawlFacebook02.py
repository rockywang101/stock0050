'''
Created on 2018年3月13日
@author: rocky.wang
'''

import requests
import json

fanPageId = "arsin168"
fanPageId = "imDataMan" # 資料視覺化
fields = "id,posts"
token = "EAACEdEose0cBAILvHoEj5KHv5ZCytVALZA2jB9ynIlRFA3xroOGRqnYREofPbhCUNvnwWZAwyMaE7R5J2WrSvyZCLHbrh2IZBHW4v1tnlObnTgfoY176nd3ePo5kykMZCaodK9j63u4u6oWZCQWA4ZCM78qkNudNevZB3lHZAVYzGuR2B3LtED5GfK0N437PIXX4h5nAvcbXZB4xwZDZD"

url = 'https://graph.facebook.com/v2.10/{}?fields={}&access_token={}'.format(fanPageId, fields, token)

response = requests.get(url)

js = json.loads(response.text)

print(js)

cnt = 0
for data in js["posts"]["data"]:
    try:
        cnt += 1
        message = data['message']
        print(cnt)
        print(message)
    except:
        print(data)
    
print("-------------------------")
nextUrl = js["posts"]["paging"]["next"] 
# print(nextUrl)


response = requests.get(nextUrl)
response.encoding = "utf-8"
 
js = json.loads(response.text)
 
print(js)
 
for data in js["data"]:
    message = data['message']
    print(cnt)
    print("ID: {}, created_time: {} Begin".format(data["id"], data["created_time"]))
    print(message)
    print("End -------------------------------------------------\n")
    cnt += 1
     

nextUrl = js["paging"]["next"] 
# print(nextUrl)


# response = requests.get(nextUrl)
# response.encoding = "utf-8"
# 
# js = json.loads(response.text)
# 
# print(js)
# 
# for data in js["data"]:
#     message = data['message']
#     print(cnt)
#     print(message)
#     cnt += 1
    