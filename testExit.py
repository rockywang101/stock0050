'''
exit() 會丟出例外，不能只寫 except

需改用 os._exit(1) 或  except Exception as e 才會正常退出

Created on 2018年2月27日
@author: rocky.wang
'''
import os

try:
    print("Run 1")
    exit() # this will raise except
except:
    print("except occur")
    
print("----------------------------------")    

try:
    print("Run 2")
    os._exit(1)
except Exception as e:
    print("except occur")
    
print("----------------------------------")
    
try:
    print("Run 3")
    exit() # this will raise except
except Exception as e:
    print("except occur")
    
    