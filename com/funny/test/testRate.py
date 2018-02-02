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



# test plurk api
# appKey = "blswXF6v9puA"
# appSecret = "NoHtYOWxcG5baUx7nEWojvicMYbdl7Tx"

