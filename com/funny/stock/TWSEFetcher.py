'''

Created on 2017年12月22日
@author: rocky.wang
'''
import requests, collections, time


DATATUPLE = collections.namedtuple('Data', 
                                ['date', 'capacity', 'turnover', 'open', 'high', 'low', 'close', 'change', 'transaction'])
    

TWSE_BASE_STOCK_URL = "http://www.twse.com.tw/exchangeReport/STOCK_DAY"

class TWSEFetcher():
    
    def __init__(self):
        pass
    
    def _make_datatuple(self, data):
        data[0] = data[0].strip()
        data[1] = int(data[1].replace(',', ''))
        data[2] = int(data[2].replace(',', ''))
        data[3] = float(data[3].replace(',', ''))
        data[4] = float(data[4].replace(',', ''))
        data[5] = float(data[5].replace(',', ''))
        data[6] = float(data[6].replace(',', ''))
        data[8] = int(data[8].replace(',', ''))
        return data

    def purify(self, data):
        return [self._make_datatuple(d) for d in data]
    
    def _convert_date(self, date):
        """Convert '106/05/01' to '2017/05/01'"""
        return '/'.join([str(int(date.split('/')[0]) + 1911)] + date.split('/')[1:])
    
    def fetch(self, ym: str, sid: str, retry = 3):

        print('TWSE Fetching Stock [%s], ym: [%s]' %(sid, ym))        
        params = {'date': ym+'01', 'stockNo': sid}
        r = requests.get(TWSE_BASE_STOCK_URL, params=params)
        try:
            data = r.json()
            if data['stat'] == '很抱歉，沒有符合條件的資料!':
                return None

            if data['stat'] == 'OK':
                return self.purify(data['data'])
        except Exception as e:
            print(e)
            if retry > 0:
                time.sleep(5)
                print("retry %s times" %(retry))
                return self.fetch(ym, sid, retry - 1)

            print("Cannot get data")


    def fetch2(self, year: int, month: int, sid: str, retry = 3):
        ym = '%d%02d' %(year, month)
        return self.fetch(self, ym, sid, retry)
            
    
# fetch = TWSEFetcher()
# data = fetch.fetch(2017, 5, "2897")
#print(data)
