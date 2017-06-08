# -*-coding=utf-8-*-
__author__ = 'Rocky'
'''
http://30daydo.com
Contact: weigesysu@qq.com
'''
#关注成交量暴涨的coin
import requests,time
import pandas as pd
class CoinVol():
    def __init__(self):
        self.host='https://www.jubi.com'
        self.coin_list=['IFC','DOGE','EAC','DNC','MET','ZET','SKT','YTC','PLC','LKC',
                        'JBC','MRYC','GOOC','QEC','PEB','XRP','NXT','WDC','MAX','ZCC',
                        'HLB','RSS','PGC','RIO','XAS','TFC','BLK','FZ','ANS','XPM','VTC',
                        'KTC','VRC','XSGS','LSK','PPC','ETC','GAME','LTC','ETH','BTC']


    def vol_detect(self,coin):
        url=self.host+'/api/v1/orders/'
        data={'coin':coin}
        while 1:
            js=requests.get(url,params=data).json()
            #print js
            #rint type(js)
            #将字典列表转为Dataframe
            df=pd.DataFrame(js)
            #print df
            #print df.info()
            #print df.dtypes
            if float(df['amount'].values[0]) >100000:
                print 'Coin : %s' %coin,
                print " Big deal more than 10w"

            time.sleep(10)



    def testcase(self):
        for i in self.coin_list:

            self.vol_detect(i.lower())

if __name__=='__main__':
    obj=CoinVol()
    obj.testcase()

