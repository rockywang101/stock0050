'''
爬取當日所有的價格，記錄到 csv 檔

Created on 2018年2月27日
@author: rocky.wang
'''
import time, datetime, requests, json, os, logging, csv, sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-10s %(levelname)-6s %(message)s',
                handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(datetime.datetime.now().strftime("%Y-%m-%d.log"), encoding='utf-8')])
logger = logging.getLogger(__name__)

FOLDER = "daily_price"

def crawl_all_stock_final_data(dt, retry=2):
    t = int(time.time()*1000)
    url = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=%s&type=ALLBUT0999&_=%s" %(dt.strftime("%Y%m%d"), t)
    logger.info("GET %s" %(url))
    try:
        r = requests.get(url)
        logger.info("Response => %s" %(r.text))
        
        js = json.loads(r.text)
        if js.get("stat") == "OK":
            # 保險起見，多加判斷而已
            if js.get("date") != dt.strftime("%Y%m%d"):
                raise Exception("取得資料日期不符")
            
            # 寫入 csv 檔
            #rowList = [js.get("fields5")] # header
            rowList = []    
            for data in js.get("data5"):
                
                ymd = str(int(dt.strftime("%Y")) - 1911) + "/" + dt.strftime("%m/%d") # 民國年格式 107/02/27
                
                rowList.append(data)
                
            with open("{}/{}.csv".format(FOLDER, dt.strftime("%Y%m%d")), "w", encoding="utf-8", newline="\n") as f1:
                writer = csv.writer(f1)
                for row in rowList:
                    writer.writerow(row)
        # 其他異常，重試三次
        else:
            if retry > 0:
                time.sleep(5)
                crawl_all_stock_final_data(dt, retry-1)
            else:
                logger.info("查無資料，程式中止")
                os._exit(1)
    except Exception as e:
        logger.exception(e)
        if retry > 0:
            time.sleep(30)
            crawl_all_stock_final_data(dt, retry-1)
        else:
            logger.error("錯誤次數過多，程式中止")
            # line notify
            os._exit(1)


if __name__ == "__main__":
    
    if not os.path.isdir(FOLDER):
        os.mkdir(FOLDER)

    dt = datetime.datetime.now()
    
#     dt = datetime.datetime(2018, 2, 26)

    crawl_all_stock_final_data(dt)
