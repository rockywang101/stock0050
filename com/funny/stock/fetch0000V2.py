'''
即時與盤後統一抓取 TWSE，由時間判斷

Created on 2018年1月14日
@author: rocky.wang
'''
import datetime, requests, csv, os, time, bs4, lineTool, json
from textwrap import indent

now = datetime.datetime.now()

prettyPrint = False
k9High = 80
k9Low = 20
finalTime = "13:30:00"

isToday = False # 是否為當日資料
isFinal = False # 是否為盤後資料
isNotify = True # 是否要發通知


def fetchStock(stockId):

    s = requests.Session()
    s.get("http://mis.twse.com.tw/stock/index.jsp")
    url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stockId}.tw&_={time}".format(stockId=stockId, time=int(time.time()) * 1000)
    print("\nGET %s" %(url))
    r = s.get(url)

    try:
        if prettyPrint:
            print(json.dumps(r.json(), indent=4))
        else:
            print(r.json())
            
        return r.json()
    except json.decoder.JSONDecodeError:
        isNotify = False
        return {'rtmessage': 'json decode error', 'rtcode': '5000'}
    
def fetchStockAndComposeMessage(stockId):
    j = fetchStock(stockId)
    z = j.get("msgArray")[0].get("z") # 現價
    y = j.get("msgArray")[0].get("y") # 昨日收盤價
    
    rtmsg = "%s價格 %s" %(stockId, z)
    diff = float(z) - float(y)
#     diff = 0
    precentDiff = diff / float(y) * 100
    preDiffStr = "%.2f" %(precentDiff) + "%"
    if diff > 0:
        dstr = " ▲" + "%.2f" %(diff) + " (" + preDiffStr + ")"
        rtmsg = rtmsg + dstr
    elif diff < 0:
        dstr = " ▼" + "%.2f" %(diff) + " (" + preDiffStr + ")"
        rtmsg = rtmsg + dstr
    
    return rtmsg
    
# 抓取大盤資料    
j = fetchStock("t00")

''' 防止還有新的資料，等兩秒再抓一次 '''
if j.get("msgArray")[0].get("t") == '13:30:00':
    print("13:30:00，睡三分鐘再重新抓一次資料，以免沒抓到最終的資料") # 大盤好像都會是超過 13:30:00，今天看是 13:31:00 昨天看是 13:33:00
    time.sleep(180)
    j = fetchStock("t00")
    print(json.dumps(j, indent=4))

if now.strftime("%Y%m%d") == j.get("msgArray")[0].get("d"):
    isToday = True

if not isToday:
    print("查無今日資料，程式中止")
    exit()

# 判斷是否為盤後資料
if j.get("msgArray")[0].get("t") >= finalTime:
    isFinal = True

d = j.get("msgArray")[0].get("d") # 日期
t = j.get("msgArray")[0].get("t") # 時間
o = j.get("msgArray")[0].get("o") # 開盤價
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
rowToday = [now.strftime("%Y%m%d"), o, h, l, z, format(rsv, ".2f"), k9]

rowList.pop(0) # 移除最舊的資料 (目前 MARK 代表不移除)
rowList.append(rowToday)

# 把含最新的資料再寫回檔案，供下次使用
if isFinal:
    with open(filename, "w", newline="\n") as csvfile:
        writer = csv.writer(csvfile)
        for item in rowList:
            writer.writerow(item)


# 判斷盤中，並且 k9 值不達標，則不發通知
if not isFinal:
    if float(k9) > k9Low and float(k9) < k9High:
        isNotify = False

# 準備發通知的文字
msg = ""
if isFinal:
    msg = datetime.date.today().strftime('%Y/%m/%d') + " K 值 %s" %(k9)
else:
    msg = "盤中 K 值 %s" %(k9)

if float(k9) <= k9Low:
    msg += "  ## 建議買進 ##"
elif float(k9) >= k9High:
    msg += "  ## 建議賣出 ##"

# 有需要發通知才繼續查 0050 / 0056 價格
if isNotify:
    
    time.sleep(1)
    msg += "\n\n" + fetchStockAndComposeMessage("0050")
    
    time.sleep(1)
    msg += "\n" + fetchStockAndComposeMessage("0056")
    
    print("\n%s" %(msg))
else:
    print("\n%s" %(msg))
    print("不發通知")
    


