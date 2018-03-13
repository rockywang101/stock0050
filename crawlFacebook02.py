'''
Created on 2018年3月13日
@author: rocky.wang
'''

import requests
import json

fanPageId = "arsin168"
fanPageId = "imDataMan" # 資料視覺化
fields = "id,posts"
token = "EAACEdEose0cBADQ4x4shsQMGnUgC1uonbvfiT1JMoBAWcv5ItPFBRZCMN0fae08d1Ho4avA56qiSpDfFHJn3ej7dCGgBp4gmDjHXnvMZCRoaxXC8lFQAzogQywhjUwgSx1ARbSRCq6TYSixai0PQC2uzbpQtfAFcV1UfiaIBwfcB5tjzpv5EColld3np2YiI48Yzm7KgZDZD"

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
    