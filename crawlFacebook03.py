'''
Created on 2018年3月13日
@author: rocky.wang
'''

import requests
import pandas as pd
from dateutil.parser import parse

group_id = '361804473860062'
token = "EAACEdEose0cBADQ4x4shsQMGnUgC1uonbvfiT1JMoBAWcv5ItPFBRZCMN0fae08d1Ho4avA56qiSpDfFHJn3ej7dCGgBp4gmDjHXnvMZCRoaxXC8lFQAzogQywhjUwgSx1ARbSRCq6TYSixai0PQC2uzbpQtfAFcV1UfiaIBwfcB5tjzpv5EColld3np2YiI48Yzm7KgZDZD"

#獲取API內容

res = requests.get('https://graph.facebook.com/v2.12/{}/feed?access_token={}'.format(group_id, token))

#使用迴圈爬取並放到list

posts = []

print(res.json())

for post in res.json()['data']:
    posts.append([parse(post.get('updated_time')), post.get('id'), post.get('message'), post.get('story')])

#輸出內容

df = pd.DataFrame(posts)
df.columns = ['貼文時間', '貼文ID', '貼文內容', '分享內容']
df.to_csv('台灣資料科學同好交流區.csv', index=False)    
