#-*-coding=utf-8-*-
#聚币网自动下单 量化交易

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

class Jubi_access():
    def __init__(self):
        cfg = Toolkit.getUserData('data.cfg')
        self.public_key = cfg['public_key']
        self.private_key = cfg['private_key']
        self.host='https://www.jubi.com'


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