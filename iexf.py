from iexfinance.stocks import Stock
import time, datetime
iex_token='sk_8a855bd5a63f4966a734af05765d3d08'
import yfinance as yf
from datetime import datetime
from datetime import timedelta

def test():
   a = yf.Ticker("AAPL")
   i=a.info
   print(i)
   p=i['regularMarketPrice']
   t=i['regularMarketTime']
   utc_time = datetime.utcfromtimestamp(t)
   return p, utc_time
if __name__ == '__main__':
 #   a = Stock("AAPL", token=iex_token)
# a.get_quote()
    '''
    a=yf.Ticker("aapl")
    print(a.info)
    print(a.info['marketCap'])
    print(a.info['regularMarketPrice'])
    t=a.info['regularMarketTime']
    print(t)

    loc_time = time.localtime(t)
    time1 = time.strftime("%Y-%m-%d %H:%M:%S", loc_time)
    print(time1)
    utc_time = datetime.utcfromtimestamp(t)
    print(utc_time)
    print(a.info['regularMarketOpen'])
    print(a.info['regularMarketVolume'])
    '''
    tmp='p:{0[0]} on {0[1]} UTC'.format(test())
    print(tmp)