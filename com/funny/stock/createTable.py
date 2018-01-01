'''
Created on 2017年12月23日

@author: Rocky
'''
import sqlite3

with open("stockDaily.ddl") as fi:
    ddl = fi.read()
    
print(ddl)


conn = sqlite3.connect("stock.sqlite")
cursor = conn.cursor()
cursor.execute(ddl)

conn.commit()
conn.close()



