# -*-coding=utf-8-*-
__author__ = 'Rocky'
'''
http://30daydo.com
Contact: weigesysu@qq.com
'''

import requests
import json
import time
import hmac
import base64
import hashlib
from toolkit import Toolkit
import pandas as pd


class api_demo():
    def __init__(self):

        self.host = 'http://www.jubi.com'

        with open('coin_list.cfg') as f:
            c_content = f.read()

        self.d_content = json.loads(c_content)

        # x=zip(* d_content)
        #print x
        #为什么得不到想要的结果?

        self.coin_list = self.d_content.keys()
        self.coin_name = self.d_content.values()

        self.private_key = Toolkit.getUserData('data.cfg')['private_key']
        self.public_key = Toolkit.getUserData('data.cfg')['public_key']
        self.md5 = self.getHash(self.private_key)


    def getHash(self, s):
        m = hashlib.md5()
        m.update(s)
        return m.hexdigest()

    def get_nonce_time(self):
        lens = 12
        curr_stamp = time.time() * 100
        nonece = long(curr_stamp)
        return nonece

    def toHex(self, str):
        lst = []
        for ch in str:
            hv = hex(ord(ch)).replace('0x', '')
            if len(hv) == 1:
                hv = '0' + hv
            lst.append(hv)
        return reduce(lambda x, y: x + y, lst)

    def account_balance(self):
        '''
        列举您的帐户信息
        Path：/api/v1/balance/
        Request类型：POST
        参数
        key - API key
        signature - signature
        nonce - nonce
        返回JSON dictionary
        asset - 折合人民币总余额
        cny_balance - 人民币总余额
        ltc_balance - 比特币总余额
        cny_lock - 人民币冻结余额
        ltc_lock - 比特币冻结余额
        ............
        nameauth - 实名认证状态 0 未实名 1 等待确认 2 已经认证成功
        moflag - 手机绑定状态 0 未绑定 1 绑定
        返回结果示例：
        {"uid":8,"nameauth":0,"moflag":0,"doge_balance":4234234,"doge_lock":0,"ltc_balance":32429.6,"ltc_lock":2.4,"xpm_balance":0,"xpm_lock":0,"cny_balance":2344581.519,"cny_lock":868862.481}

        :return:
        '''

        url = self.host + '/api/v1/balance/'
        nonce = self.get_nonce_time()
        parameters = {'key': self.public_key, 'nonce': str(nonce), 'signature': ''}
        post_data = ''
        for k, v in parameters.items():
            post_data = post_data + k + '=' + v + '&'

        post_data = post_data.replace('&signature=&', '')
        # print post_data
        signature = signature = hmac.new(self.md5, post_data, digestmod=hashlib.sha256).digest()
        sig = self.toHex(signature)
        parameters['signature'] = sig
        r = requests.post(url, data=parameters)
        s = r.json()
        #print s
        for k, v in s.items():

            #print k,v
            if v != 0:
                print k, v
        return s

    def Trade_list(self, coin):
        '''
        Trade_list（挂单查询）
        您指定时间后的挂单，可以根据类型查询，比如查看正在挂单和全部挂单
        Path：/api/v1/trade_list/
        Request类型：POST
        参数
        key - API key
        signature - signature
        nonce - nonce
        since - unix timestamp(utc timezone) default == 0, i.e. 返回所有
        coin - 币种简称,例如btc、ltc、xas
        type - 挂单类型[open:正在挂单, all:所有挂单]

        返回JSON dictionary
        id - 挂单ID
        datetime - date and time
        type - "buy" or "sell"
        price - price
        amount_original - 下单时数量
        amount_outstanding - 当前剩余数量
        '''
        url = self.host + '/api/v1/trade_list/'
        nonce = self.get_nonce_time()
        types = 'all'
        # since=0
        parameters = {'key': self.public_key, 'nonce': str(nonce), 'type': types, 'coin': coin, 'signature': ''}
        #print parameters
        post_data = ''
        for k, v in parameters.items():
            if not isinstance(v, str):
                #if type(v) is not types.StringType:
                v = str(v)
            post_data = post_data + k
            post_data = post_data + '=' + v + '&'

        #print 'post-data:\n',post_data
        post_data = post_data[:-1]
        post_data = post_data.replace('&signature=', '')
        #print post_data

        signature = hmac.new(self.md5, post_data, digestmod=hashlib.sha256).digest()
        sig = self.toHex(signature)
        parameters['signature'] = sig
        #print parameters
        r = requests.post(url=url, data=parameters)
        s = r.json()
        #print s
        #print type(s)
        '''
        for i in s:
            #print i
            pass
        '''
        return s

    def Trade_add(self, coin,  price,amount):

        '''
        Trade_add（下单）
        Path：/api/v1/trade_add/
        Request类型：POST
        参数
        key - API key
        signature - signature
        nonce - nonce
        amount - 购买数量
        price - 购买价格
        type - 买单或者卖单
        coin - 币种简称,例如btc、ltc、xas
        返回JSON dictionary
        id - 挂单ID
        result - true(成功), false(失败)
        返回结果示例：
        {"result":true, "id":"11"}
        '''
        url = self.host + '/api/v1/trade_add/'
        nonce = self.get_nonce_time()
        types = 'buy'
        # amount=100
        #price=0.1
        parameters = {'key': self.public_key, 'nonce': str(nonce), 'type': types, 'coin': coin, 'signature': '',
                      'amount': amount, 'price': price}
        #print parameters
        post_data = ''
        for k, v in parameters.items():
            if not isinstance(v, str):
                #if type(v) is not types.StringType:
                v = str(v)
            post_data = post_data + k
            post_data = post_data + '=' + v + '&'

        #print 'post-data:\n', post_data
        post_data = post_data[:-1]
        #print post_data
        post_data = post_data.replace('signature=&', '')
        #print post_data
        signature = hmac.new(self.md5, post_data, digestmod=hashlib.sha256).digest()
        sig = self.toHex(signature)
        parameters['signature'] = sig
        #print parameters
        r = requests.post(url=url, data=parameters)
        s = r.json()
        print s
        if s['result'] is True:
            return s['id']
        #return s
        return False


    def Trade_cancel(self, coin, id_num):
        '''
        Trade_cancel（取消订单）
        Path：/api/v1/trade_cancel/
        Request类型：POST
        参数
        key - API key
        signature - signature
        nonce - nonce
        id - 挂单ID
        coin - 币种简称,例如btc、ltc、xas
        返回JSON dictionary
        result - true(成功), false(失败)
        id - 订单ID
        返回结果示例：
        {"result":true, "id":"11"}
        '''
        url = self.host + '/api/v1/trade_cancel/'
        nonce = self.get_nonce_time()

        parameters = {'nonce': str(nonce), 'coin': coin, 'id': id_num, 'key': self.public_key, 'signature': ''}
        post_data = ''
        for k, v in parameters.items():
            post_data = post_data + k + '=' + v + '&'
        post_data = post_data[:-1]
        #print post_data
        post_data = post_data.replace('&signature=', '')
        signature = hmac.new(self.md5, post_data, digestmod=hashlib.sha256).digest()
        sig = self.toHex(signature)
        parameters['signature'] = sig
        r = requests.post(url=url, data=parameters)
        s = r.json()
        print s
        return s['result']


    def Trade_view(self, coin, id_num):
        '''
        Trade_view（查询订单信息）
        Path：/api/v1/trade_view/
        Request类型：POST
        参数
            key - API key
            signature - signature
            nonce - nonce
            id - 挂单ID
            coin - 币种简称,例如btc、ltc、xas



            返回JSON dictionary
            id - 挂单ID
            datetime - 挂单时间（格式：YYYY-mm-dd HH:ii:ss）
            type - "buy" or "sell"
            price - 挂单价
            amount_original - 下单时数量
            amount_outstanding - 当前剩余数量
            status - 状态：new(新挂单), open(开放交易), cancelled(撤消), closed(完全成交)
            avg_price - 成交均价
        '''
        url = self.host + '/api/v1/trade_view/'
        nonce = self.get_nonce_time()

        parameters = {'nonce': str(nonce), 'coin': coin, 'id': id_num, 'key': self.public_key, 'signature': ''}
        post_data = ''
        for k, v in parameters.items():
            post_data = post_data + k + '=' + v + '&'
        post_data = post_data[:-1]
        # print post_data
        post_data = post_data.replace('&signature=', '')
        signature = hmac.new(self.md5, post_data, digestmod=hashlib.sha256).digest()
        sig = self.toHex(signature)
        parameters['signature'] = sig

        r = requests.post(url=url, data=parameters)
        s = r.json()
        print s
        return s



    def AllTicker(self):
        url=self.host+'/api/v1/allticker/'
        r=requests.get(url)
        s=r.json()
        #print s
        '''
        for k,v in s.items():
            print self.d_content[k]
            for vk,vv in v.items():
                print vk,vv
            print '*'*15
        '''
        return s
    def Cancel_All(self,coin):
        df=self.Data_transform(coin)
        res=df['id'].map(lambda x:self.Trade_cancel(coin,x))
        print res
        #self.Trade_cancel(coin,)

    def Data_transform(self,coin):
        data = self.Trade_list(coin)
        df = pd.DataFrame(data)

        # df['datetime']=df['datetime'].applymap(lambda x:)
        df['datetime'] = pd.to_datetime(df['datetime'])
        #print df
        df.set_index('datetime',inplace=True,drop=True)
        print df
        print df.info()
        print df.dtypes
        '''
        for i in df['id'].values:
            self.Trade_view('zet', i)
        '''
        df['status']=df['id'].map(lambda x:self.Trade_view(coin,x)['status'])
        df=df[df[u'status']==u'open']
        self.current_order=df
        return self.current_order

def main():
    obj = api_demo()
    #obj.Trade_add('zet',0.01,2000)
    #obj.Trade_list('zet')
    #obj.Trade_cancel('zet','862979')
    #obj.Data_transform()
    #res=obj.Trade_view('zet','882354')
    #print res[u'status']
    #obj.Data_transform()
    #obj.account_balance()
    #s=obj.AllTicker()
    #print s['zet']['last']
    obj.Cancel_All('zet')

if __name__ == '__main__':
    main()