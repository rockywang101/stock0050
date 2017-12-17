"""
fetch my need and notify me

"""
import requests
import os
from lineTool import lineNotify
from bs4 import BeautifulSoup

def fetchPrice(stockId):
    
    rtnList = [stockId]
    url = "http://finance.google.com.hk/finance?q=TPE:" + stockId
    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")

    # find price
    div = soup.find("div", {"id": "price-panel"})
    price = div.find("span").find("span").text
    rtnList.append(price)
    # find chgPrice
    div = soup.find("div", {"class": "id-price-change"})
    chgPrice = div.find("span").find("span").text;
    rtnList.append(chgPrice)
    # find chgPercent
    chgPercent = div.find_all("span")[2].text
    rtnList.append(chgPercent)
    
    return rtnList

    # work, but i cannot get cid 682750 for stockId
#     span = soup.find("span", id = "ref_682750_l")
#     print(span.text)

def composeLineText(rtnList, minPrice, maxPrice):
    #text = "%s 價格 [%s], [%s], %s，目標 [%s]-[%s]" %(rtnList[0], rtnList[1], rtnList[2], rtnList[3], minPrice, maxPrice)
    text = "%s 價格 %s, %s, %s" %(rtnList[0], rtnList[1], rtnList[2], rtnList[3])
    text += "\n"
    text += "目標 %s ~ %s " %(format(minPrice, ".2f"), format(maxPrice, ".2f"))
    
    if float(rtnList[1]) >= maxPrice:
        text += "### YES, 賣掉它 !"
    
    if float(rtnList[1]) <= minPrice:
        text += "### YES, 用力買 !"
    return text

text = "\n\n"
text += composeLineText(fetchPrice("0056"), 24, 26)
text += "\n\n"
text += composeLineText(fetchPrice("2890"), 9.0, 9.6)
text += "\n\n"
text += composeLineText(fetchPrice("2891"), 19, 24)

print(text)

# price2890 = fetchPrice("2890")
# text += "2890 現在價格 : " + str(price2890) +"，目標 : 9.6"
# if price2890 >= 9.6:
#     text += "### YES, sale it !"
# 
# text += "\n"

token = os.environ["LINE_TEST_TOKEN"]
lineNotify(token, text)
