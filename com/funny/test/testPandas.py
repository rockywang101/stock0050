# '''
# Created on 2018年1月22日
# @author: rocky.wang
# '''
# 
# import pandas as pd # 引用套件並縮寫為 pd  
# 
# print("begin")
# 
# df = pd.read_csv('2897.csv')  
# 
# print(df)  
# 
# print("end")


''' 
demo multi-thread 
'''
import time
from random import randint
from multiprocessing import Pool

def printit(item):
    print("item %s start" %(item))
    seconds = randint(1, 3)
    time.sleep(seconds)
    print("item %s completed" %(item))

datas = []
for i in range(5):
    datas.append(i+1)



if __name__ == '__main__':

    print("--- single thread version ---")
    for i in range(len(datas)):
        printit(datas[i])
    
    print("\n--- multithread version ---")
    with Pool(processes=8) as pool:
        pool.map(printit, datas)
        

