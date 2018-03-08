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


if __name__ == '__main__':
        
    comp0050list = []
    with open("0050composition.csv", "r", encoding="utf-8") as f1:
        reader = csv.reader(f1)
        for row in reader:
            comp0050list.append(row[0])
        
    filenames = os.listdir("data")
 
    for filename in filenames:
        if not filename.endswith(".csv"):
            continue
          
        stockId = filename.split(".")[0]
        stockName = filename.split(".")[1]
  
        if not stockId in comp0050list:
#             print("ignore stockId %s" %(stockId))
            continue
            
        price_list = []
        with open("data/{}".format(filename), "r") as f1:
            reader = csv.reader(f1)
            for row in reader:
                price_list.append(row[6])
         
        max_price = max(price_list[-1080:])
        if price_list[-1] == '--':
            diff = -1
        else:
            diff = float(max_price) - float(price_list[-1])
        
        if diff > 0:
            rate = diff / float(price_list[-1])
            if rate > 0.5:
                print("%s max %s, now %s, rate: %.2f" %(stockId, max_price, price_list[-1], rate))
        
        
#     datas = [1, 2, 3, 4, 5, 6]
#     print(datas[-3:])
#     
#     print(max(datas))
                
            
            


