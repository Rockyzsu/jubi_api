# -*-coding=utf-8-*-
import base64

__author__ = 'Rocky'
'''
http://30daydo.com
Contact: weigesysu@qq.com
'''
import random,json
import hashlib
import hmac,time
import smtplib
from email.mime.text import MIMEText
from email import Utils
import threading
import requests,datetime,itchat
import urllib,urllib2
from toolkit import Toolkit
#from Crypto import HMAC, SHA256
from itertools import permutations
class Jubi_access():
    def __init__(self):
        cfg = Toolkit.getUserData('data.cfg')
        self.public_key = cfg['public_key']
        self.private_key = cfg['private_key']
        self.host='https://www.jubi.com'
        self.coin_list=['IFC','DOGE','EAC','DNC','MET','ZET','SKT','YTC','PLC','LKC',
                        'JBC','MRYC','GOOC','QEC','PEB','XRP','NXT','WDC','MAX','ZCC',
                        'HLB','RSS','PGC','RIO','XAS','TFC','BLK','FZ','ANS','XPM','VTC',
                        'KTC','VRC','XSGS','LSK','PPC','ETC','GAME','LTC','ETH','BTC']



    def getContent(self):
        url = 'https://www.jubi.com/api/v1/trade_list'
        params_data = {'key': 'x', 'signature': 'x'}
        s = requests.get(url=url, params=params_data)

    def getHash(self, s):
        m = hashlib.md5()
        m.update(s)
        return m.hexdigest()

    def sha_convert(self, s):
        return hashlib.sha256(self.getHash(s)).hexdigest()

    def get_nonce(self):
        lens = 12
        return ''.join([str(random.randint(0, 9)) for i in range(lens)])

    def get_nonce_time(self):
        lens = 12
        curr_stamp = time.time()*100
        nonece=long(curr_stamp)
        return nonece

    def get_signiture(self,):

        nonce_value=self.get_nonce_time()
        key_value=self.public_key
        private_key=self.private_key
        s='nonce='+str(nonce_value)+'&'+'key='+key_value
        print s
        #signature是签名，是将amount price type nonce key等参数通过'&'字符连接起来通过md5(私钥)为key进行sha256算法加密得到的值.
        md5=self.getHash(private_key)
        signature =hmac.new(md5,s,digestmod=hashlib.sha256).digest()
        sig=self.toHex(signature)

        md5 = self.getHash(self.private_key)
        message = 'nonce=' + nonce + '&' + 'key=' + self.public_key
        # print message
        signature = hmac.new(md5, message, digestmod=hashlib.sha256).digest()
        # print signature

        # req=requests.post(url,data={'signature':signature,'key':public_key,'nonce':nonce,'coin':'zet'})
        req = requests.post(url, data={'coin': coin})
        print req.status_code
        print req.text


    def getAccount(self):
        url='https://www.jubi.com/api/v1/balance/'
        nonce_value=self.get_nonce_time()
        print nonce_value
        key_value=self.public_key
        private_key=self.private_key
        s='nonce='+str(nonce_value)+'&'+'key='+key_value
        s='key='+key_value+'&'+'nonce='+str(nonce_value)
        print s
        #signature是签名，是将amount price type nonce key等参数通过'&'字符连接起来通过md5(私钥)为key进行sha256算法加密得到的值.
        md5=self.getHash(private_key)
        signature =hmac.new(md5,s,digestmod=hashlib.sha256).digest()
        sig=self.toHex(signature)
        data_wrap={'nonce':nonce_value,'key':key_value,'signature':sig}
        '''
        data_en=urllib.urlencode(data_wrap)
        req=urllib2.Request(url,data=data_en)
        resp=urllib2.urlopen(req).read()
        print resp
        '''

        js=requests.post(url,data=data_wrap).json()
        print js


    def toHex(self,str):
        lst = []
        for ch in str:
            hv = hex(ord(ch)).replace('0x', '')
            if len(hv) == 1:
                hv = '0' + hv
            lst.append(hv)
        return reduce(lambda x, y: x + y, lst)

    def hmac_sha256(self,key, msg):
        hash_obj = HMAC.new(key=key, msg=msg, digestmod=SHA256)
        return hash_obj.hexdigest()

    def order_check(self):
        url=self.host+'/api/v1/trade_list/'
        print url
        coin='zet'
        types='all'
        #since='2017-5-10 13:29:39'
        since=0
        nonce=self.get_nonce_time()
        key_value=self.public_key
        private_key=self.private_key

        #s='nonce='+str(nonce)+'&'+'type='+types+'&'+'coin='+coin+'&'+'since='+since+'&'+'key='+key_value

        s='coin='+coin+'&'+'since'+str(since)+'&'+'type='+types+'&'+'nonce='+str(nonce)+'&'+'key='+key_value
        print s
        md5=self.getHash(private_key)

        msg=bytes(s).encode('utf-8')
        key=bytes(md5).encode('utf-8')
        sig=hmac.new(md5,s,digestmod=hashlib.sha256).digest()
        print sig
        sig_encode=self.toHex(sig)
        print sig_encode
        data_wrap1={'nonce':nonce,'type':types,'coin':coin,'signature':sig_encode,'key':key_value,'since':since}
        print data_wrap1
        js=requests.post(url,data=data_wrap1).json()
        print js

    def order_id(self):
        url=self.host+'/api/v1/trade_view/'
        print url
        coin='zet'
        types='open'
        since=0
        id=10
        nonce=self.get_nonce_time()
        print nonce
        key_value=self.public_key
        private_key=self.private_key
        s='nonce='+str(nonce)+'&'+'coin='+coin+'&'+'id='+str(id)+'&'+'key='+key_value
        print s
        md5=self.getHash(private_key)

        msg=bytes(s).encode('utf-8')
        key=bytes(md5).encode('utf-8')
        sig=hmac.new(md5,s,digestmod=hashlib.sha256).digest()
        print sig
        sig_encode=self.toHex(sig)
        print sig_encode
        data_wrap1={'nonce':nonce,'coin':coin,'signature':sig_encode,'key':key_value,'id':id}
        print data_wrap1
        js=requests.post(url,data=data_wrap1).json()
        print js

    def buy(self):
        url=self.host+'/api/v1/trade_add/'

    def get_access(self):
        url='https://www.jubi.com/api/v1/trade_list/'
        nonce_value=self.get_nonce_time()
        print nonce_value
        key_value=self.public_key
        private_key=self.private_key
        types='all'
        coin='zet'
        since_value=0
        s='type='+types+'&'+'since='+str(since_value)+'&'+'coin='+coin+'&'+'nonce='+str(nonce_value)+'&'+'key='+key_value
        print s
        #signature是签名，是将amount price type nonce key等参数通过'&'字符连接起来通过md5(私钥)为key进行sha256算法加密得到的值.
        md5=self.getHash(private_key)
        signature =hmac.new(md5,s,digestmod=hashlib.sha256).digest()
        sig=self.toHex(signature)
        data_wrap={'nonce':nonce_value,'key':key_value,'signature':sig,'type':types,'coin':coin,'since':since_value}

        js=requests.post(url,data=data_wrap).json()
        print js

    #下单
    def TradeOder(self,coin,types,amount,price):
        url='https://www.jubi.com/api/v1/trade_add/'
        nonce_value=self.get_nonce_time()
        #print nonce_value
        key_value=self.public_key
        private_key=self.private_key
        #types='buy'
        #coin='zet'
        #amount=500
        #price=0.1
        #s="amount="+str(amount)+"&price="+str(price)+"&type="+types+"&nonce="+str(nonce_value)+"&key="+key_value+"&coin="+coin
        #print s
        s="nonce="+str(nonce_value)+"&price="+str(price)+"&amount="+str(amount)+"&key="+key_value+"&coin="+coin+"&type="+types
        print s
        #signature是签名，是将amount price type nonce key等参数通过'&'字符连接起来通过md5(私钥)为key进行sha256算法加密得到的值.
        md5=self.getHash(private_key)
        signature =hmac.new(md5,s,digestmod=hashlib.sha256).digest()
        sig=self.toHex(signature)
        #print sig
        data_wrap={'signature':sig,'nonce':str(nonce_value),'coin':coin,'key':key_value,'amount':amount,'price':price,'type':types}
        print data_wrap
        js=requests.post(url,data=data_wrap).json()
        print js



    def testcase(self):
        #self.getAccount()
        #self.order_id()
        #self.order_check()
        #self.get_access()
        self.TradeOder('zet','buy','100',0.01)
if __name__ == '__main__':

    obj = Jubi_access()
    obj.testcase()
    # print obj.get_signiture()
    #print obj.real_time_ticker('zet')
    # obj.real_time_depth('zet')
    #obj.warming('zet',0.23,0.17)
    #obj.list_all_price()
    #obj.turnover('doge')
    #print obj.getOrder('zet')


