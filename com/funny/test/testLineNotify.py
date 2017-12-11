'''
測試 Line Notify

Created on 2017年12月11日
@author: rocky.wang
'''
import os
import lineTool

token = os.environ["LINE_TEST_TOKEN"]
msg = "Notify from Python \nHave a nice day"

lineTool.lineNotify(token, msg)

