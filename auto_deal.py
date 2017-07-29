#-*-coding=utf-8-*-
#聚币网自动下单 量化交易

import random,json
import hashlib
import hmac,time
from email import Utils
import threading
import requests,datetime,itchat
import urllib,urllib2
from toolkit import Toolkit
import Queue
from basic_usage import api_demo
import pandas as pd
import numpy as np

obj=api_demo()
q=Queue.Queue()
data_dict={}
def price_strategy(coin,price,amount):
    '''
    当价格满足要求的时候就下单
    :return:
    '''

    '''
    t_id=obj.Trade_add(coin,price,amount)
    print t_id
    data_dict={t_id:[coin,price,amount]}
    '''

    s=obj.Trade_list('zet')
    '''
    for i in s:
        #print k,v
        print i
    '''


    #df=pd.DataFrame(s,index_col='datetime')
    #df=pd.DataFrame(s,index=[u'datetime'])
    df=pd.DataFrame(s)
    #print df

    #df['datetime']=df['datetime'].map(lambda x:datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    #上面这两种方法都可以
    df['datetime'] = pd.to_datetime(df['datetime'])

    df.set_index('datetime',inplace=True,drop=True)

    #print df.dtypes
    #print df.info()
    #print df
    df['status']=df['id'].map(lambda x:obj.Trade_view('zet',x)['status'])

    print df
    new_df = df[df['status']=='open']

    #df.to_csv('')
    print new_df




def main():

    price_strategy('zet',0.0112,1000)
    #price_strategy('zet',0.011,1000)

    while q.empty() is False:
        print q.get()



if __name__=='__main__':
    main()

