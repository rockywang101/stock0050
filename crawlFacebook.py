'''
用 facebook 提供的 SDK 抓取粉絲頁

Created on 2018年3月13日
@author: rocky.wang
'''
import facebook

token = "EAACEdEose0cBADQ4x4shsQMGnUgC1uonbvfiT1JMoBAWcv5ItPFBRZCMN0fae08d1Ho4avA56qiSpDfFHJn3ej7dCGgBp4gmDjHXnvMZCRoaxXC8lFQAzogQywhjUwgSx1ARbSRCq6TYSixai0PQC2uzbpQtfAFcV1UfiaIBwfcB5tjzpv5EColld3np2YiI48Yzm7KgZDZD"


graph = facebook.GraphAPI(access_token = token) #套件會用你的token連接到facebook
fanpage_info = graph.get_object('pyladies.tw', field = 'id')  #指定拿pyladies.tw 這個粉專的id和讚數
print(fanpage_info)  #印出來看看長什麼樣子，會是JSON格式的資料
print("Fanpage id = %s" %(fanpage_info['id']))


posts = graph.get_connections(id = fanpage_info['id'], connection_name = 'posts', summary = True)
print(posts)   #這行會印出一大堆貼文的資料
print ("共有", len(posts), "篇PO文")
