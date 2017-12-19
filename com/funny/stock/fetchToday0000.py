'''
抓取今天的大盤資料並計算 RSA/K9 值，發 Line 到群組

因為一開始是用歷史資料，且這個資料是在公平交易所，應該比在 google 或 yahoo 更精準
後來發現有 http://mis.twse.com.tw/stock/fibest.jsp?stock=t00 可以查即時資料，應該 13:30 過後就變盤後資料
後續會再修正

Created on 2017年12月1日
@author: rocky.wang
'''
import datetime, requests, csv, os, time, lineTool, json


def fetchStock(stockId):

    req = requests.Session()
    req.get("http://mis.twse.com.tw/stock/index.jsp")
    url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stockId}.tw&_={time}".format(stockId=stockId, time=int(time.time()) * 1000)
    r = req.get(url)

    try:
        return r.json()
    except json.decoder.JSONDecodeError:
        return {'rtmessage': 'json decode error', 'rtcode': '5000'}
    

now = datetime.datetime.now()
print("--------------------------------------------------")        
print("執行時間 %s" %(now.strftime("%Y-%m-%d %H:%M:%S")))
print("--------------------------------------------------")        

# 取今天民國年的字串 => 106/12/01
dt = datetime.date.today()
today = str(int(now.strftime("%Y")) - 1911) + now.strftime("/%m/%d")


"""
取得今日的價格資料 
"""
def fetchTodayPrice():
    # 抓取這個月的歷史資料
    url = "http://www.twse.com.tw/indicesReport/MI_5MINS_HIST?response=json&date=" + datetime.date.today().strftime('%Y%m%d')
    print("GET " + url)
    
    jData = requests.get(url).json()["data"]
    rowToday = None
    # 取得今日的價格資料
    for item in jData:
        if item[0] == today:
            rowToday = item
    # 清除千分位並回傳
    if rowToday != None:
        for i in range(len(rowToday)):
            rowToday[i] = rowToday[i].replace(",", "")
        return rowToday        

# 取得今天的大盤資料
rowToday = fetchTodayPrice()

if rowToday == None:
    print("查無今日資料，不繼續執行")
    exit()

maxList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最高價清單
minList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最低價清單
k9 = None
rowList = []
isExist = False

# 取得目前 py 檔的資料夾路徑   (os.getwcd() 會取得執行 bat 的目錄，不能用它)
ph = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(ph, "0000.csv")

# 打開 0050.csv 讀取最近九天的資料
with open(filename, "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for i in range(len(row)):
            row[i] = row[i].replace(",", "") # 把所有千分位去掉，以免影響 float 轉型

        # 因 yahoo 數值不對，刻意修正成與 yahoo 一致
#         if row[0] == "106/11/29":
#             row[2] = "10759.44"

        rowList.append(row)
        maxList.pop(0)
        maxList.append(float(row[2])) # 最高價
        minList.pop(0)
        minList.append(float(row[3])) # 最低價

        k9 = row[6]
        if row[0] == today:
            isExist = True

if isExist:
    print("今日資料已存在，不繼續執行")
    exit()

maxList.pop(0)
maxList.append(float(rowToday[2])) # 最高價
minList.pop(0)
minList.append(float(rowToday[3])) # 最低價

# 算出今日的 RSV 值
rsv = round((100 * (float(rowToday[4]) - min(minList)) / (max(maxList) - min(minList))), 2)
# 更新，發現 yahoo 的算法應該是先四捨五入後再相加
v1 = round(rsv / 3, 2)
v2 = round(float(k9) * 2 / 3, 2)
k9 = round(v1 + v2, 2) # 兩個都已經四捨五入，但相加還是可能會有無限小數，python 太奧妙了
k9 = format(k9, ".2f") # 在 linux 上跑 round 會無效

rowToday.append(format(rsv, ".2f"))
rowToday.append(k9)

rowList.pop(0) # 移除最舊的資料 (目前 MARK 代表不移除)
rowList.append(rowToday)

# 把含最新的資料再寫回檔案，供下次使用
with open(filename, "w", newline="\n") as csvfile:
    writer = csv.writer(csvfile)
    for item in rowList:
        writer.writerow(item)
            
# 準備發通知的文字
dd = datetime.date.today().strftime('%Y/%m/%d')
msg = dd + " K 值 %s" %(k9)
if float(k9) <= 20:
    msg += "  ## 建議買進 ##"
elif float(k9) >= 80:
    msg += "  ## 建議賣出 ##"    


# 加上 0050 0056 股價
j = fetchStock("0050")
z = j.get("msgArray")[0].get("z")
msg += "\n\n0050價格 %s" %(z)

j = fetchStock("0056")
z = j.get("msgArray")[0].get("z")
msg += "\n0056價格 %s" %(z)

print(msg)


# 發 LINE 通知
lineTool.lineNotify(os.environ["LINE_0050_TOKEN"], msg)
time.sleep(2)   # delays for n seconds
lineTool.lineNotify(os.environ["LINE_0050_TOKEN2"], msg)

print("run completed.")