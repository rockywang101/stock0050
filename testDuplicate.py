'''
Created on 2018年2月27日
@author: rocky.wang
'''

dict = {}

dict["2017"] = "Hello 2017"

dict["2017"] = "Hello World 2017"

dict["2017"] = "Hell 2017"

print(dict)

import datetime

dt = datetime.datetime.now()

ymd = str(int(dt.strftime("%Y")) - 1911) + "/" + dt.strftime("%m/%d")

print(ymd)