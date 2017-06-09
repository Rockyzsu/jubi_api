# -*-coding=utf-8-*-
import datetime
import time
import requests
import pandas as pd
import threading
__author__ = 'Rocky'
'''
http://30daydo.com
Contact: weigesysu@qq.com
获取聚币网的成交量与成交价的数据，保存到本地，官方只为用户保存100条记录，没有提供完整的记录
'''


class Storage():

    def __init__(self):
        self.coin_list=['IFC','DOGE','EAC','DNC','MET','ZET','SKT','YTC','PLC','LKC',
                        'JBC','MRYC','GOOC','QEC','PEB','XRP','NXT','WDC','MAX','ZCC',
                        'HLB','RSS','PGC','RIO','XAS','TFC','BLK','FZ','ANS','XPM','VTC',
                        'KTC','VRC','XSGS','LSK','PPC','ETC','GAME','LTC','ETH','BTC']
        self.url='http://www.jubi.com/api/v1/orders/'
        self.today=datetime.datetime.now().strftime('%Y-%m-%d')


    def getOrders(self,coin):
        try:
            js=requests.get(self.url,params={'coin':coin}).json()
        except Exception,e:
            print e
            print "can't get data, will retry"
            time.sleep(30)
        #print js
        '''
        u'date': u'1496936989',
	    u'tid': u'121264',
	    u'price': 0.1631,
	    u'type': u'sell',
	    u'amount': 8043.1328
        '''
        '''
        frame=[]
        for i in js:

            df=pd.DataFrame(i,index=[1])
            df.set_index('date',inplace=True)
            #print df
            frame.append(df)
            #print i
            #print type(i)
        new_df=pd.concat(frame)
        print new_df.dtypes
        print new_df.info
        new_df.sort_values('date',inplace=True,ascending=True)
        #print new_df.groupby('date')
        print new_df
        '''

        df=pd.DataFrame(js,columns=['date','tid','price','type','amount'])
        #print df
        df.set_index('tid',inplace=True)
        print df
        #df.to_excel('test.xls')
        time1=df['date'].values[0]
        df['date']=df['date'].map(lambda x:datetime.datetime.fromtimestamp(long(x) ))
        print df
        filename=self.today+'_'+coin+'.csv'
        df.to_csv(filename,mode='a',header=False)

    def loops(self,coin):
        while 1:
            self.getOrders(coin)
            time.sleep(10)

    def multi_thread(self):
        t1=threading.Thread(target=self.loops,args=('zet',))

    def testcase(self):
        #self.getOrders('zet')
        self.loops('zet')
if __name__=='__main__':
    obj=Storage()
    obj.testcase()