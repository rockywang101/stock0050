'''
拿取氣象的 open data 通知 line notify

Created on 2018年1月31日
@author: rocky.wang
'''
import xml.etree.ElementTree as ET
import requests, os
import lineTool

apikey = os.environ["OPEN_DATA_CWB_TOKEN"]

dataid = "F-C0032-029" # 雲林縣天氣小幫手
url = "http://opendata.cwb.gov.tw/opendataapi?dataid=" + dataid + "&authorizationkey=" + apikey

xml = ET.fromstring(requests.get(url).text)

msg = xml[8][2][1][0].text + "\n\n" + xml[8][2][3][0].text

print(msg)

# msg = xml[8][2][1][0].text + "\n\n" + xml[8][2][2][0].text + "\n\n" + xml[8][2][3][0].text
# print(msg)

lineTool.lineNotify(os.environ["LINE_STUPID_TOKEN"], msg)

