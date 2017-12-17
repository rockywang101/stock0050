'''
Created on 2017年12月17日
@author: Rocky
'''
import requests, bs4, lineTool, os
import datetime

ph = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(ph, "myip.txt")

ip = None
with open(filename, "r") as f1:
    ip = f1.read()

url = "http://www.seocheckpoints.com/my-ip-address"

r = requests.get(url)
soup = bs4.BeautifulSoup(r.text, "html.parser")

elem = soup.find("span", {"class": "badge bg-green"})

todayIP = elem.text

with open(filename, "w") as f1:
    f1.write(todayIP)

now = datetime.datetime.now()
print()
print("執行時間 %s" %(now.strftime("%Y-%m-%d %H:%M:%S")))

# 若不同，發通知
if ip != todayIP:
    token = os.environ["LINE_TEST_TOKEN"]
    msg = "IP change from %s to %s" %(ip, todayIP)
    lineTool.lineNotify(token, msg)
    print(msg)
else:
    print("ip not change")
