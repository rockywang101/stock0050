'''
投報率試算
Created on 2017年12月14日
@author: rocky.wang
'''
from random import getrandbits

# n 現金股利
# m 股票股利
# p 現價
def getRate(n, m, price):
    v1 = n * 1000 # 每張可領多少現金股利
    v2 = price * m * 100 # 每張領到的股票股利價值現金多少錢
    total = v1 + v2
    rate = total / price * 1000 / 10000
    print(format(rate, ".2f") + "%")
    return rate

getRate(1, 0, 20.1)
getRate(0.49, 0.74, 18.6)
getRate(0.52, 0.43, 13.5)
