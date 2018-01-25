'''
常用功能

Created on 2018年1月23日
@author: rocky.wang
'''
import datetime, time

beginTime = int(time.time()*1000)

dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("執行時間 %s" %(dt))


t = int(time.time() * 1000)
print("like java new Date().getTime() => %s" %(t))


time.sleep(0.5)

endTime = int(time.time()*1000)

print("執行花費時間 %s" %(endTime - beginTime))

dt = "20180724"
print(dt[0:4])
print(dt[4:6])
print(dt[6:8])