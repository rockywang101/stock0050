'''
使用 pandas

至 http://isin.twse.com.tw/isin/C_public.jsp?strMode=2

抓取所有股票代號與上市日期

Created on 2018年1月22日
@author: rocky.wang
'''

import pandas, re
import csv

url = "http://isin.twse.com.tw/isin/C_public.jsp?strMode=2"

table = pandas.read_html(url)[0]

idx = 0
dataCnt = 0
for item in table[0]:
    
    tokens = item.split("　")
    
    r = re.search(r"^[0-9]{4}$", tokens[0])
    
    if r != None:
        print("stockId: %s, date: %s" %(tokens[0], table[2][idx]))
        dataCnt += 1

    idx += 1
    
print("total cnt => %s" %(dataCnt))


with open("all.csv", "a", newline="\n") as csvfile:
    writer = csv.writer(csvfile)
    idx = 0
    for item in table[0]:
        tokens = item.split("　")
        sid = tokens[0]
        row = [sid, table[2][idx]]
        writer.writerow(row)
        idx += 1
