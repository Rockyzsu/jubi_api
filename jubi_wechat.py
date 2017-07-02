# -*-coding=utf-8-*-
__author__ = 'Rocky'
'''
http://30daydo.com
Contact: weigesysu@qq.com
'''
import random
import hashlib
import hmac,time
import smtplib
from email.mime.text import MIMEText
from email import Utils
import threading
import requests,datetime,itchat

from toolkit import Toolkit


class Jubi_web():
    def __init__(self, send=None):
        cfg = Toolkit.getUserData('data.cfg')
        self.public_key = cfg['public_key']
        self.private_key = cfg['private_key']
        self.send=send
        from_mail = cfg['from_mail']
        password = cfg['password']
        to_mail = cfg['to_mail']
        smtp_server = 'smtp.qq.com'

        self.server = smtp_server
        self.username = from_mail.split("@")[0]
        self.from_mail = from_mail
        self.password = password
        self.to_mail = to_mail
        self.coin_list=['IFC','DOGE','EAC','DNC','MET','ZET','SKT','YTC','PLC','LKC',
                        'JBC','MRYC','GOOC','QEC','PEB','XRP','NXT','WDC','MAX','ZCC',
                        'HLB','RSS','PGC','RIO','XAS','TFC','BLK','FZ','ANS','XPM','VTC',
                        'KTC','VRC','XSGS','LSK','PPC','ETC','GAME','LTC','ETH','BTC']
        # 初始化邮箱设置读取需要股票信息
        # 这样子只登陆一次
        if self.send == 'msn':

            try:
                self.smtp = smtplib.SMTP_SSL(port=465)
                self.smtp.connect(self.server)
                self.smtp.login(self.username, self.password)
            except smtplib.SMTPException, e:
                print e
                return 0

        if send=='wechat':
            self.w_name=u'wwwei'
            #self.w_name1=u'wwwei'
            itchat.auto_login(hotReload=True)
            account=itchat.get_friends(self.w_name)
            for i in account:
                if i[u'PYQuanPin']==self.w_name:
                    self.toName= i['UserName']
                    #print self.toName

    def send_wechat(self,name,content):
        w_content=name+' '+content
        itchat.send(w_content,toUserName=self.toName)
        time.sleep(1)
        itchat.send(w_content,toUserName='filehelper')


    def send_text(self, name, content):

        subject = '%s' % name
        self.msg = MIMEText(content, 'plain', 'utf-8')
        self.msg['to'] = self.to_mail
        self.msg['from'] = self.from_mail
        self.msg['Subject'] = subject
        self.msg['Date'] = Utils.formatdate(localtime=1)
        try:
            self.smtp.sendmail(self.msg['from'], self.msg['to'], self.msg.as_string())
            self.smtp.quit()
            print "sent"
        except smtplib.SMTPException, e:
            print e
            return 0

    def warming(self, coin, up_price, down_price):
        url = 'https://www.jubi.com/api/v1/ticker/'
        while 1:
            time.sleep(5)
            try:
                data = requests.post(url, data={'coin': coin}).json()
            except Exception,e:
                print e
                print "time out. Retry"
                time.sleep(15)
                continue

            current = float(data['last'])
            if current >= up_price:
                print "Up to ", up_price
                print "current price ",current

                if self.send=='msn':
                    self.send_text(coin,str(current))
                if self.send=='wechat':
                    self.send_wechat(coin,str(current))

                time.sleep(1200)
            if current <= down_price:
                print "Down to ", down_price
                print "current price ",current
                if self.send=='msn':
                    self.send_text(coin,str(current))
                if self.send=='wechat':
                    self.send_wechat(coin,str(current))
                time.sleep(1200)
    #上面的内容尽量不用修改。


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

    def get_signature(self):
        url = 'https://www.jubi.com/api/v1/ticker/'
        coin = 'zet'
        nonce = self.get_nonce()

        # sha=self.sha_convert(private_key)
        md5 = self.getHash(self.private_key)
        message = 'nonce=' + nonce + '&' + 'key=' + self.public_key
        # print message
        signature = hmac.new(md5, message, digestmod=hashlib.sha256).digest()
        # print signature

        # req=requests.post(url,data={'signature':signature,'key':public_key,'nonce':nonce,'coin':'zet'})
        req = requests.post(url, data={'coin': coin})
        print req.status_code
        print req.text

    def real_time_ticker(self, coin):
        url = 'https://www.jubi.com/api/v1/ticker/'
        try:
            data = requests.post(url, data={'coin': coin}).json()
            #print data
        except Exception ,e:
            print e
        return data



    def real_time_depth(self, coin):
        url = 'https://www.jubi.com/api/v1/depth/'
        data = requests.post(url, data={'coin': coin}).json()
        print data
        data_bids = data['bids']
        data_asks = data['asks']
        print "bids"
        for i in data_bids:
            print i[0],
            print ' ',
            print i[1]
        print "asks"
        for j in data_asks:
            print j[0],
            print ' ',
            print j[1]

    def list_all_price(self):
        for i in self.coin_list:
            print i,
            print " price: ",
            p=self.real_time_ticker(i.lower())
            if p is not None:
                print p[u'last']

    def getOrder(self,coin):
        url='https://www.jubi.com/api/v1/orders/'
        try:
            req=requests.get(url,params={'coin':coin})
        except Exception,e:
            print e

        data=req.json()
        return data
    # recent 100 trade turn over
    def turnover(self,coin):
        i=coin.lower()
        coins=Toolkit.getUserData('coins.csv')
        total=long(coins[i])
        p=self.getOrder(i)
        print p
        amount=0.00
        for j in p:
            t= j[u'amount']
            amount=float(t)+amount
        #current=float(self.real_time_ticker(i)[u'last'])
        turn_over=amount*1.00/total*100

        print turn_over

    def multi_thread(self,coin_list,price_list):
        thread_num=len(coin_list)
        thread_list=[]
        for i in range(thread_num):
            t=threading.Thread(target=self.warming, args=(coin_list[i],price_list[i][0],price_list[i][1]),)
            thread_list.append(t)
        for j in thread_list:
            j.start()
        for k in thread_list:
            k.join()

if __name__ == '__main__':

    obj = Jubi_web(send='wechat')

    # print obj.get_signature()
    #print obj.real_time_ticker('zet')
    # obj.real_time_depth('zet')
    #obj.warming('zet',0.23,0.17)
    #obj.list_all_price()
    #obj.turnover('doge')
    #print obj.getOrder('zet')

    coin_list=['zet','doge']
    price_list=[[0.2,0.13],[0.03,0.021]]
    #obj.warming('zet',0.24,0.16)
    obj.multi_thread(coin_list,price_list)

