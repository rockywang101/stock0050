'''
Created on 2018年1月21日

@author: Rocky
'''
from pony.orm import *

db = Database()
db.bind(provider='sqlite', filename='testpony.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
set_sql_debug(True)

class Stock(db.Entity):
    id = PrimaryKey(int, auto=True)
    stockId = Required(str, unique=True)
    o = Optional(float)
    h = Optional(float)
    l = Optional(float)
    z = Optional(float)
    
    