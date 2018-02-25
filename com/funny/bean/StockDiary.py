'''
Created on 2018年1月17日
@author: rocky.wang
'''
import json

class StockDairy(object):
    
    j = None
    
    def __init__(self, jObj):
        self.j = jObj
    
    
    def get(self, key):
        return self.j.get("msgArray")[0].get(key)
    
    def myPrint(self, prettyPrint):
        if prettyPrint:
            print("%s\n" %(json.dumps(self.j, indent=4)))
        else:
            print("%s\n" %(self.j))
        
    

