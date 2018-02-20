'''
通知我自己今天的天氣  

留存而已，後來覺得通知有點白痴，什麼都通知就等於沒通知，應該重要或很難查到的東西再通知就好

Created on 2018年1月31日
@author: rocky.wang
'''
import xml.etree.ElementTree as ET
import requests, os
import lineTool

apikey = os.environ["OPEN_DATA_CWB_TOKEN"]

dataid = "F-C0032-029"
url = "http://opendata.cwb.gov.tw/opendataapi?dataid=" + dataid + "&authorizationkey=" + apikey

xml = ET.fromstring(requests.get(url).text)

msg = xml[8][2][1][0].text + "\n\n" + xml[8][2][2][0].text
# msg = xml[8][2][1][0].text + "\n\n" + xml[8][2][2][0].text + "\n\n" + xml[8][2][3][0].text

print(msg)
lineTool.lineNotify(os.environ["LINE_STUPID_TOKEN"], msg)

