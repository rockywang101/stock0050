'''
抓取今天的大盤資料並計算 RSA/K9 值，發 Line 到群組

Created on 2017年12月1日
@author: rocky.wang
'''
import datetime, requests, csv, os, time, bs4, lineTool

"""
取得今日盤中即時價格
"""
def fetchTodayPriceRealtime():
    
    url = "http://finance.google.com.hk/finance?q=TPE:TAIEX"
    print("GET " + url)
    
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    
    # 取得現在指數
    now = soup.find("div", id="price-panel").find("span", {"class": "pr"}).find("span").text
    now = float(now.replace(",", ""))

    # 取得最高與最低
    c = soup.find("table", {"class": "snap-data"}).find("td", {"class": "val"})
    minPrice = float(c.text.split(" - ")[0].replace(",", ""))
    maxPrice = float(c.text.split(" - ")[1].replace(",", ""))

    return [now, minPrice, maxPrice]


maxList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最高價
minList = [0, 0, 0, 0, 0, 0, 0, 0, 0] # 9 天的最低價
k9 = None
oldK9 = None
rowList = []

isExist = False

# 取民國年的字串 106/12/01
today = datetime.date.today()
sToday = str(int(today.strftime("%Y")) - 1911) + today.strftime("/%m/%d")
        
now = datetime.datetime.now()
print()
print("執行時間 %s" %(now.strftime("%Y-%m-%d %H:%M:%S")))
print("--------------------------------------------------")        


# 取得目前 py 檔的資料夾路徑   os.getwcd() 會取得執行 bat 的目錄
ph = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(ph, "0000.csv")
        
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

        rsa = row[5]
        k9 = row[6]
        oldK9 = float(k9)
        if row[0] == sToday:
            isExist = True

if isExist:
    print("今日資料已存在，不繼續執行")
    exit()

# 取得今天的價格資料
rowToday = fetchTodayPriceRealtime()

if rowToday == None:
    print("查無今日資料，不繼續執行")
    exit()

maxList.pop(0)
maxList.append(rowToday[2]) # 最高價
minList.pop(0)
minList.append(rowToday[1]) # 最低價

# 算出今日的 RSV 值
rsv = round((100 * (float(rowToday[0]) - min(minList)) / (max(maxList) - min(minList))), 2)
# 更新，發現 yahoo 的算法應該是先四捨五入後再相加
v1 = round(rsv / 3, 2)
v2 = round(float(oldK9) * 2 / 3, 2)
k9 = round(v1 + v2, 2) # 兩個都已經四捨五入，但相加還是可能會有無限小數，python 太奧妙了
rsv = format(rsv, ".2f")
k9 = format(k9, ".2f")

rowToday.append(rsv)
rowToday.append(k9)

#rowList.pop(0)
rowList.append(rowToday)
            
# line notify
msg = None
if float(k9) <= 20:
    msg = "盤中 K 值 %s  ## 建議買進 ##" %(k9)
elif float(k9) >= 80:
    msg = "盤中 K 值 %s  ## 建議賣出 ##" %(k9)
else:
    print("盤中 K 值 %s (不發通知)" %(k9))

if msg != None:
    print(msg)
    lineTool.lineNotify(os.environ["LINE_0050_TOKEN"], msg)
    time.sleep(3)   # delays for n seconds
    lineTool.lineNotify(os.environ["LINE_0050_TOKEN2"], msg)
