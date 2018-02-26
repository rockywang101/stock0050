#!/usr/bin/env python
import re
from urllib.request import urlopen
import ystockquote
import datetime
from datetime import date, timedelta as td
from pprint import pprint

# ID setting
ID = '2108'

def get_average(ID, year):
    ID = ID+'.TW'
    
    if year != datetime.datetime.today().date().year:
        current_date = date(year,12,31)
    else:
        current_date = datetime.datetime.today().date()
    start_date = date(year,1,1)
    delta = current_date-start_date
    date_list = [start_date+datetime.timedelta(days=x) for x in range(0, delta.days)]
    data = ystockquote.get_historical_prices(ID, start_date.isoformat(), current_date.isoformat())
    temp_list = []
    for item in date_list:
        try:
            value= float(data[item.isoformat()]['Close'])
        except:
            # TypeError or KeyError
            continue
        temp_list.append(float(value))
    #    print(item.date().isoformat()+':'+value)
    return sum(temp_list)/len(temp_list)

# Get the webpage's source html code
source = 'http://www.goodinfo.tw/stockinfo/StockDividendSchedule.asp?STOCK_ID='
filename = ID+'.html'
result = urlopen(source+ID).read().decode("big5")#.encode("utf8")

# Get the data <table></table>
regex = re.compile("<table class='std_tbl' width='100%'.*<\/table>")
datatable = regex.findall(result)[0]

# Get the data row <tr></tr>
regex = re.compile("<tr bgcolor=.*</tr>")
datarow = regex.findall(datatable)
string = datarow[0].strip()

# Clean data row
cleanlist = ["<nobr>", " align='right'", "</nobr>"]
for target in cleanlist:
    string = string.replace(target,'').strip(' ')
# Special operation on empty data cell
string = string.replace("</td>"," ")
    
# Get each data <td></td>
datalist = string.split('</tr>')
totaldata = {}
infolist =['盈餘所屬年度',
           '股利發放年度',
           '股東會日期',
           '除息交易日',
           '除息參考價（元）',
           '除權交易日',
           '除權參考價（元）',
           '股利發放年度之股價統計：最高',
           '股利發放年度之股價統計：最低',
           '股利發放年度之股價統計：年均',
           '現金股利：盈餘',
           '現金股利：公積',
           '現金股利：合計',
           '股票股利：盈餘',
           '股票股利：公積',
           '股票股利：合計',
           '股利合計',
           '年均殖利率（%）']

# Print Out the result
data_dict = {}
for item in datalist[:-1]:
    if '股' in item or '權' in item:
        continue
    rowlist = item.split('<td>')[1:]
    newrowlist = {}
    for num,item in enumerate(rowlist):
        newrowlist[infolist[num]] = item.strip()
    try:
        newrowlist['前年收盤均價'] = get_average(ID, int(rowlist[1].strip())-1)
        newrowlist['本年收盤均價'] = get_average(ID, int(rowlist[1].strip()))
        data_dict[rowlist[1].strip()] = newrowlist
    except:
        break
   
def price(info, percent):
    return ((float(info['本年收盤均價'])-float(info['前年收盤均價']))+float(info['現金股利：合計']))/(percent-float(info['股票股利：合計'])/10)

pprint(data_dict['2013'])
print(price(data_dict['2013'], 0.06))