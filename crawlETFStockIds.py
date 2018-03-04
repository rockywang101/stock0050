'''
抓取 0050 成份股資料

http://www.yuantaetfs.com/#/Orders/1066

Created on 2018年3月2日
@author: rocky.wang
'''
import csv, requests

url = "http://www.yuantaetfs.com/api/Composition?date=20180302&fundid=1066"

r = requests.get(url)
js = r.json()

with open("0050composition.csv", "w", newline="\n", encoding="utf-8") as f1:
    writer = csv.writer(f1)
    for i in range(len(js)):
        print(js[i])
        writer.writerow([js[i].get("stkcd"), js[i].get("name"), js[i].get("qty")])
        