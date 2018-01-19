'''
即時與盤後統一抓取 TWSE，由時間判斷

Created on 2018年1月14日
@author: rocky.wang
'''
import datetime, requests, csv, os, time, bs4, lineTool, json
from textwrap import indent

now = datetime.datetime.now()

isToday = False # 是否為當日資料
isFinal = False # 是否為盤後資料

def fetchStock(stockId):

    s = requests.Session()
    s.get("http://mis.twse.com.tw/stock/index.jsp")
    url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stockId}.tw&_={time}".format(stockId=stockId, time=int(time.time()) * 1000)
    print("---\nGET %s\n---" %(url))
    r = s.get(url)

    try:
        return r.json()
    except json.decoder.JSONDecodeError:
        return {'rtmessage': 'json decode error', 'rtcode': '5000'}
    
# 抓取大盤資料    
j = fetchStock("t00")
print(json.dumps(j, indent=4))

''' 防止還有新的資料，等兩秒再抓一次 '''
if j.get("msgArray")[0].get("t") == '13:30:00':
    print("13:30:00，睡兩秒再重新抓一次資料")
    time.sleep(2)
    j = fetchStock("t00")
    print(json.dumps(j, indent=4))

if now.strftime("%Y%m%d") == j.get("msgArray")[0].get("d"):
    isToday = True

if not isToday:
    print("查無今日資料，程式中止")
    exit()

# 判斷是否為盤後資料
if j.get("msgArray")[0].get("t") >= "13:30:00":
    isFinal = True
    
    

h = j.get("msgArray")[0].get("h") # 最高價
l = j.get("msgArray")[0].get("l") # 最低價
z = j.get("msgArray")[0].get("z") # 收盤價
    

maxList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最高價清單
minList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最低價清單
k9 = None
rowList = []

# 取得目前 py 檔的資料夾路徑   (os.getwcd() 會取得執行 bat 的目錄，不能用它)
ph = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(ph, "0000.csv")

# 打開 0050.csv 讀取最近九天的資料
with open(filename, "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for i in range(len(row)):
            row[i] = row[i].replace(",", "") # 把所有千分位去掉，以免影響 float 轉型

        rowList.append(row)
        maxList.pop(0)
        maxList.append(float(row[2])) # 最高價
        minList.pop(0)
        minList.append(float(row[3])) # 最低價

        k9 = row[6]
        if row[0] == now.strftime("%Y%m%d"):
            print("今日資料已存在 0000.csv 檔，不繼續執行")
            exit()

maxList.pop(0)
maxList.append(float(h)) # 最高價
minList.pop(0)
minList.append(float(l)) # 最低價


# 算出今日的 RSV 值
rsv = round((100 * (float(z) - min(minList)) / (max(maxList) - min(minList))), 2)
# 更新，發現 yahoo 的算法應該是先四捨五入後再相加
v1 = round(rsv / 3, 2)
v2 = round(float(k9) * 2 / 3, 2)
k9 = round(v1 + v2, 2) # 兩個都已經四捨五入，但相加還是可能會有無限小數，python 太奧妙了
k9 = format(k9, ".2f") # 在 linux 上跑 round 會無效

# 日期，開，高，低，收
rowToday = [now.strftime("%Y%m%d"), h, l, z, format(rsv, ".2f"), k9]

rowList.pop(0) # 移除最舊的資料 (目前 MARK 代表不移除)
rowList.append(rowToday)


# time.sleep(1)
# j = fetchStock("2890")
# print(j)
# print(json.dumps(j, indent=4))
# print(j.get("msgArray")[0].get("d"))
# print(j.get("msgArray")[0].get("t"))


# print(now.strftime("%Y-%m-%d %H:%M:%S"))
# print(now.strftime("%Y%m%d"))
# print(now.strftime("%H:%M:%S"))

#"t": "12:28:09",
#"d": "20180117",


t1 = "12:31:00"
t2 = "12:31:00"

print(t1 <= t2)


