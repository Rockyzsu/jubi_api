# -*-coding=utf-8-*-
import base64
import hashlib

__author__ = 'Rocky'
'''
http://30daydo.com
Contact: weigesysu@qq.com
'''

import requests
import json
import time
import hmac

class api_demo():
    def __init__(self):
        with open('coin_list.cfg') as f:
            c_content=f.read()
        d_content=json.loads(c_content)

        #x=zip(* d_content)
        #print x
        #为什么得不到想要的结果?

        self.coin_list=d_content.keys()
        self.coin_name=d_content.values()

        self.private_key='xx'
        self.public_key='xx'
        self.md5=self.getHash(self.private_key)

    '''
    参数
    key - API key
    signature - signature
    nonce - nonce
    since - unix timestamp(utc timezone) default == 0, i.e. 返回所有
    coin - 币种简称,例如btc、ltc、xas
    type - 挂单类型[open:正在挂单, all:所有挂单]
    '''
    def Trade_list(self,coin):
        nonce=self.get_nonce_time()
        types='all'
        since=0
        parameters={'key':self.public_key,'nonce':nonce,'type':types,'coin':coin,'since':since}
        print parameters
        s='dd'
        post_data=''
        for k,v in parameters.items():
            if not isinstance(v,str) :
            #if type(v) is not types.StringType:
                v=str(v)
            post_data=post_data+k
            post_data=post_data+'='+v+'&'

        print 'post-data',post_data
        post_data=post_data[:-1]
        print post_data
        signature =hmac.new(self.md5,s,digestmod=hashlib.sha256).digest()
        sig=self.toHex(signature)
        parameters['signature']='sig'
        print parameters
        #r=requests.get()


    def getHash(self, s):
        m = hashlib.md5()
        m.update(s)
        return m.hexdigest()

    def get_nonce_time(self):
        lens = 12
        curr_stamp = time.time()*100
        nonece=long(curr_stamp)
        return nonece

    def toHex(self,str):
        lst = []
        for ch in str:
            hv = hex(ord(ch)).replace('0x', '')
            if len(hv) == 1:
                hv = '0' + hv
            lst.append(hv)
        return reduce(lambda x, y: x + y, lst)

def main():
    obj=api_demo()
    obj.Trade_list('zet')


if __name__=='__main__':
    main()