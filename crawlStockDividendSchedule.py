'''
爬配股配息

Created on 2018年2月28日
@author: rocky.wang
'''
import os, csv
import requests
from bs4 import BeautifulSoup
import time, logging, sys, datetime
from pathlib import Path

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-10s %(levelname)-6s %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(datetime.datetime.now().strftime("tk%Y-%m-%d.log"), encoding='utf-8')])
logger = logging.getLogger(__name__)

def fetch(stockId):
    
    url = "https://goodinfo.tw/StockInfo/StockDividendSchedule.asp?STOCK_ID=" + stockId
    print(url)
    
    headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
                    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }
    
    r = requests.get(url, headers = headers)
    r.encoding = 'UTF-8'
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    elem = soup.find("p", {"style": "line-height:240px;font-size:14pt;color:red;font-weight:bold"})
    if not elem == None and elem.text == '查無除權息日程訊息':
        logger.info("查無除權息日程訊息")
        with open("dataDividend/{}_dividendSchedule.csv".format(stockId), "w", newline="\n") as f1:
            csvWriter = csv.writer(f1)
        return

    elem = soup.find("table", {"class": "solid_1_padding_3_3_tbl"}).findAll("tr", {"height": "23px"})
    with open("dataDividend/{}_dividendSchedule.csv".format(stockId), "w", newline="\n") as f1:
        csvWriter = csv.writer(f1)
        for tr in elem:
            tds = tr.findAll("td")
            row = []
            for td in tds:
                row.append(td.text)
            csvWriter.writerow(row)
            

if __name__ == '__main__':
        
    filenames = os.listdir("data")
 
    for filename in filenames:
        if not filename.endswith(".csv"):
            continue
        
        stockId = filename.split(".")[0]
        
        # 避免重抓，但真正要重新更新時，這段要拿掉
        if Path("dataDividend/{}_dividendSchedule.csv".format(stockId)).is_file():
            logger.info("%s 已存在" %(stockId))
            continue
        
        fetch(stockId)
        print("end. continue next... ")
        time.sleep(5)
    












