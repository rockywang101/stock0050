'''
Created on 2017年12月23日
@author: Rocky
'''

import sqlite3

conn = sqlite3.connect("test.sqlite")
cursor = conn.cursor()
cursor.execute("select DATE('NOW')")

conn.commit()
conn.close()
