# -*-coding=utf-8-*-
__author__ = 'Rocky'
'''
http://30daydo.com
Contact: weigesysu@qq.com
'''
#关注成交量暴涨的coin
import requests,time,datetime,threading
import pandas as pd
from jubi_wechat import Jubi_web
class CoinVol():
    def __init__(self):
        self.obj_wc=Jubi_web()
        self.host='https://www.jubi.com'
        self.coin_list=['IFC','DOGE','EAC','DNC','MET','ZET','SKT','YTC','PLC','LKC',
                        'JBC','MRYC','GOOC','QEC','PEB','XRP','NXT','WDC','MAX','ZCC',
                        'HLB','RSS','PGC','RIO','XAS','TFC','BLK','FZ','ANS','XPM','VTC',
                        'KTC','VRC','XSGS','LSK','PPC','ETC','GAME','LTC','ETH','BTC']
        self.coin_name={'zet':u'泽塔币',
                        'doge':u'狗狗币',
                        'eac':u'地球币',
                        'dnc':u'暗网币',
                        'rio':u'里约币',
                        'blk':u'黑币',
                        'ifc':u'无限币',
                        'met':u'美通币',
                        'gooc':u'谷壳币',
                        'jbc':u'聚宝币',
                        'pgc':u'乐通币',
                        'lsk':u'LISK',
                        'tfc':u'传送币',
                        'xpm':u'质数币',
                        'nxt':u'未来币',
                        'ppc':u'点点币',
                        'ktc':u'肯特币',
                        'mtc':u'猴宝币',
                        'skt':u'鲨之信',
                        'btc':u'比特币',
                        'peb':u'普银币',
                        'ltc':u'莱特币',
                        'xsgs':u'雪山古树',
                        'eth':u'以太坊',
                        'vtc':u'绿币',
                        'bts':u'比特股',
                        'hlb':u'活力币',
                        'zcc':u'招财币',
                        'etc':u'以太经典',
                        'qec':u'企鹅币',
                        'fz':u'冰河币',
                        'plc':u'保罗币',
                        'max':u'最大币',
                        'ytc':u'一号币',
                        'xrp':u'瑞波币',
                        'lkc':u'幸运币',
                        'wdc':u'世界币',
                        'vrc':u'维理币',
                        'rss':u'红贝壳',
                        'ans':u'小蚁股',
                        'xas':u'阿希比',
                        'game':u'游戏点',
                        'mryc':u'美人鱼币',
                            }


    def vol_detect(self,coin):

        url=self.host+'/api/v1/orders/'
        data={'coin':coin}
        print "in %s" %coin
        while 1:
            try:
                js=requests.get(url,params=data).json()
            except Exception,e:
                time.sleep(10)
                continue
            #print js
            #rint type(js)
            #将字典列表转为Dataframe
            df=pd.DataFrame(js)
            df['date']=df['date'].map(lambda x:datetime.datetime.fromtimestamp(long(x) ))

            #print df
            #print df.info()
            #print df.dtypes
            buy_df=df[df['type']=='buy']
            #print buy_df
            buy_count= len(buy_df)
            total= len(df)
            buy_ratio=buy_count*1.00/total*100.00
            if buy_ratio>65.0:
                print datetime.datetime.now().strftime('%H:%M:%S')
                print "Coin : %s " %self.coin_name[coin],
                print "buy more than 60 percent in the pass 100 order: %s\n" %buy_ratio
                txt="buy more than 60 percent in the pass 100 order: %s\n" %buy_ratio
                self.obj_wc.send_wechat(coin,txt)
            if float(df['amount'].values[0]) >100000:
                print datetime.datetime.now().strftime('%H:%M:%S')
                print 'Coin : %s' %self.coin_name[coin],
                print " Big deal more than 10w"
                self.obj_wc.send_wechat(coin," Big deal more than 10w")



            time.sleep(60)


    def multi_thread(self):
        thread_list=[]
        print len(self.coin_name)
        for i in self.coin_name:
            print i," ",
            print self.coin_name[i]
            t=threading.Thread(target=self.vol_detect,args=(i,))
            thread_list.append(t)

        for j in thread_list:
            j.start()
            #j.join()
        for k in thread_list:
            k.join()



    def testcase(self):
        #self.multi_thread()
        self.vol_detect('zet')
if __name__=='__main__':
    obj=CoinVol()
    obj.testcase()

