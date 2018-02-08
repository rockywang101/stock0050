'''
通知我自己今天的天氣  

留存而已，後來覺得通知有點白痴，什麼都通知就等於沒通知，應該重要或很難查到的東西再通知就好

Created on 2018年1月31日
@author: rocky.wang
'''
import xml.etree.ElementTree as ET
import requests, os
import lineTool

dataid = "F-C0032-010"
url = "http://opendata.cwb.gov.tw/opendataapi?dataid=" + dataid + "&authorizationkey=" + os.environ["OPEN_DATA_CWB_TOKEN"]

xml = ET.fromstring(requests.get(url).text)

msg = xml[8][2][1][0].text + "\n\n" + xml[8][2][2][0].text + "\n\n" + xml[8][2][3][0].text


print(xml[8][2][1][0].text)
print()
print(xml[8][2][2][0].text)
print()
print(xml[8][2][3][0].text)

lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], msg)
