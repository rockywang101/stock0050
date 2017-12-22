'''

Created on 2017年12月22日
@author: rocky.wang
'''
import requests
import datetime
import collections


DATATUPLE = collections.namedtuple('Data', 
                                       ['date', 'capacity', 'turnover', 'open', 'high', 'low', 'close', 'change', 'transaction'])
    

class TWSEFetcher():
    
    TWSE_BASE_URL = "http://www.twse.com.tw/"
    TWSE_BASE_STOCK_URL = TWSE_BASE_URL + "exchangeReport/STOCK_DAY"
    
    
    def __init__(self):
        pass
    
    def _make_datatuple(self, data):
        data[0] = datetime.datetime.strptime(self._convert_date(data[0]), '%Y/%m/%d')
        data[1] = int(data[1].replace(',', ''))
        data[2] = int(data[2].replace(',', ''))
        data[3] = float(data[3].replace(',', ''))
        data[4] = float(data[4].replace(',', ''))
        data[5] = float(data[5].replace(',', ''))
        data[6] = float(data[6].replace(',', ''))
        data[7] = float(0.0 if data[7].replace(',', '') == 'X0.00' else data[7].replace(',', ''))  # +/-/X表示漲/跌/不比價
        data[8] = int(data[8].replace(',', ''))
        return DATATUPLE(*data)

    def purify(self, original_data):
        return [self._make_datatuple(d) for d in original_data['data']]
    
    def _convert_date(self, date):
        """Convert '106/05/01' to '2017/05/01'"""
        return '/'.join([str(int(date.split('/')[0]) + 1911)] + date.split('/')[1:])
    

    def fetch(self, year: int, month: int, sid: str, retry = 3):
        
        params = {'response': 'json', 'date': '%d%02d01' %(year, month), 'stockNo': sid}
        r = requests.get(self.TWSE_BASE_STOCK_URL, params=params)
        try:
            data = r.json()
        except:
            if retry > 0:
                print("retry %s times" %(retry))
                return self.fetch(year, month, sid, retry - 1)
            else:
                data = {'stat': '', 'data': []}

        if data['stat'] == 'OK':
            data['data'] = self.purify(data)
        else:
            data['data'] = []
        return data
    
    
    
fetch = TWSEFetcher()

data = fetch.fetch(2017, 5, "0050")

print(data)
