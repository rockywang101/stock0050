'''
抓取個股配股配息資料

Created on 2018年2月18日
@author: rocky.wang
'''
import requests
from bs4 import BeautifulSoup

print("start...")

def fetch(sid):
    
    url = "https://goodinfo.tw/StockInfo/StockDividendSchedule.asp?STOCK_ID=" + sid
    
    headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
                    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }
    
    r = requests.get(url, headers = headers)
    r.encoding = 'UTF-8'
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    #elem = soup.find("table", {"class": "solid_1_padding_3_0_tbl"})
    #elem = soup.find("table", {"class": "solid_1_padding_3_3_tbl"}).findAll("tr", {"bgcolor": "white"})
    elem = soup.find("table", {"class": "solid_1_padding_3_3_tbl"}).findAll("tr", {"height": "23px"})
    
    for tr in elem:
        tds = tr.findAll("td")
        m = float(tds[10].text)
        s = float(tds[13].text)
        x = calRate(19, m, s)
        print("%s years  %s + %s, Rate: %s" %(tds[1].text, tds[10].text, tds[13].text, x))
    
    
def calRate(p: float, m:float, s:float):
    t = m * 1000 + s * 100 * p # 總獲利
    x = t / (p * 1000) * 100 # 總獲利 / 總成本
    return format(x, ".2f")
    



if __name__ == "__main__":
    sid = "2820"
    fetch(sid)




        