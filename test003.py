'''

I wnat test
    
    * get 0056 amount realtime
    
    * log 

Created on 2018年2月26日
@author: rocky.wang
'''
import logging
import datetime, requests, csv, os, time, bs4, lineTool, json, sys

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-10s %(levelname)-6s %(message)s',
                handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(datetime.datetime.now().strftime("tk%Y-%m-%d.log"), encoding='utf-8')])
logger = logging.getLogger(__name__)

def fetchStock(stockId):
    
    req = requests.Session()
    req.get("http://mis.twse.com.tw/stock/index.jsp")
    url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stockId}.tw&_={time}".format(stockId=stockId, time=int(time.time()) * 1000)
    r = req.get(url)
    try:
        logger.info(r.text.strip())
        return r.json()
    except json.decoder.JSONDecodeError:
        return {'rtmessage': 'json decode error', 'rtcode': '5000'}
    
    
if __name__ == "__main__":
    j = fetchStock("0056")
    
    msg = ""
    zStr = j.get("msgArray")[0].get("z")
    msg += "\n0056價格 %s" %(zStr)

    z = float(j.get('msgArray')[0].get('z'))
    y = float(j.get('msgArray')[0].get('y'))    
    diff = z - y
    diffStr = "%.2f" %(diff)
    if diff > 0:
        diffStr = "▲" + diffStr
        precentDiff = diff / y * 100
        preDiffStr = "%.2f" %(precentDiff) + "%"
        diffStr = diffStr + " (" + preDiffStr + ")"
        msg += " " + diffStr
    elif diff < 0:
        diffStr = "▼" + diffStr
        precentDiff = diff / y * 100
        preDiffStr = "%.2f" %(precentDiff) + "%"
        diffStr = diffStr + " (" + preDiffStr + ")"
        msg += " " + diffStr    
    
    v = j.get("msgArray")[0].get("v") # 累積成交量
    msg += "\n累積成交量 %s" %(v)
        
    logger.info(msg)
    
    