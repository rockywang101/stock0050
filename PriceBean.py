'''
試算投報率用的

Created on 2018年3月19日
@author: rocky.wang
'''
class PriceBean():

    stockId = ""
    stockName = ""
    
    money = 0 # 現金
    price = 0.0 # 當日股價
    stockNum = 0 # 股數
    years = 1 # 經過年數
    
    totalSalary = 0 # 總成本
    
    @property
    def stockValue(self):
        return int(self.stockNum * self.price)
    
    def __init__(self, stockId, stockName):
        self.stockId = stockId
        self.stockName = stockName
 
    
    def addSalary(self, salary):
        self.money += salary
        self.totalSalary += salary
        
    # 領股息 / 買股票    
    def updateMoney(self, money):
        self.money += money
        
    def addStockNum(self, stockNum):
        self.stockNum += stockNum

    def buyStock(self):
        buyNum = int(self.money / self.price) # 可買股數
        money = int(buyNum * self.price)
        
        self.stockNum += buyNum
        self.money -= money
#         print("買入 %s 股，金額 %s" %(buyNum, money))

        