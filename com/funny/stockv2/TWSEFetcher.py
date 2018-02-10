'''

Created on 2017年12月22日
@author: rocky.wang
'''
import requests, collections, time, os



"""
發送 Line Notify 訊息
"""
def lineNotify(token, msg):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
   
    payload = {'message': msg}
    requests.post(url, headers = headers, params = payload)

token = os.environ["LINE_TEST_TOKEN"]




DATATUPLE = collections.namedtuple('Data', 
                                ['date', 'capacity', 'turnover', 'open', 'high', 'low', 'close', 'change', 'transaction'])
    

TWSE_BASE_STOCK_URL = "http://www.twse.com.tw/exchangeReport/STOCK_DAY"

class TWSEFetcherEx():
    
    def __init__(self):
        pass
    
    def _make_datatuple(self, data):
        data[0] = data[0].strip()
        data[1] = int(data[1].replace(',', ''))
        data[2] = int(data[2].replace(',', ''))
        
        # 3~6
        for i in range(3, 7):
            if data[i].replace(',', '') == '--':
                data[i] = None
            else:
                data[i] = float(data[i].replace(',', ''))
                
        data[8] = int(data[8].replace(',', ''))
        return data

    def purify(self, data):
        return [self._make_datatuple(d) for d in data]
    
    def _convert_date(self, date):
        """Convert '106/05/01' to '2017/05/01'"""
        return '/'.join([str(int(date.split('/')[0]) + 1911)] + date.split('/')[1:])
    
    def fetch(self, ym: str, sid: str, retry = 2):

        print('TWSE Fetching Stock [%s], ym: [%s]' %(sid, ym), flush=True)        
#         params = {'response': 'json', 'date': ym+'01', 'stockNo': sid}
#         r = requests.get(TWSE_BASE_STOCK_URL, params=params)
        
        url = TWSE_BASE_STOCK_URL + "?response=json&date=" + ym + "01&stockNo=" + sid
        print(url, flush=True)
        r = requests.get(url)
        stat = None
        try:
            data = r.json()
            print(data, flush=True)
            
            stat = data['stat']
            
#             if data['stat'] == '很抱歉，沒有符合條件的資料!':
#                 return None

            if data['stat'] == 'OK':
                return self.purify(data['data'])
            else:
                # 目前不應該有查不到資料的問題
                raise Exception("stat error")
        except Exception as e:
            print(e, flush=True)
            
            if retry > 0:
                print("retry %s times, stat: %s" %(retry, stat), flush=True)
                if stat == '很抱歉，沒有符合條件的資料!':
                    time.sleep(5)
                else:
                    lineNotify(token, "error occur, retry after one minute")
                    time.sleep(60)
                    
                return self.fetch(ym, sid, retry - 1)
            else:
                if stat != '很抱歉，沒有符合條件的資料!':
                    lineNotify(token, "error occur !! retry fail")
                    raise e
                else:
                    return None


    def fetch2(self, year: int, month: int, sid: str, retry = 3):
        ym = '%d%02d' %(year, month)
        return self.fetch(self, ym, sid, retry)
            
    
# fetch = TWSEFetcher()
# data = fetch.fetch(2017, 5, "2897")
#print(data)
