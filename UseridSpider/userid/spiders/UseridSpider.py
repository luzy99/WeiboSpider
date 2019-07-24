# -*- coding: utf-8 -*-
import scrapy
import requests
import re
from scrapy import Request
import json
from ..items import useridItem
from scrapy_redis.spiders import RedisSpider
import pymysql

class UseridSpider(RedisSpider):
    name = 'UseridSpider'
    redis_key = 'userid'
    key = ''
    allowed_domains = ['m.weibo.cn']
#    id='5717775404'

    # https://m.weibo.cn/api/container/getIndex?containerid=2302835717775404_-_INFO


    @classmethod
    def changeKey(cls, key):
        cls.key = key
    
    def __init__(self, key=None, *args, **kwargs):
        print('spider init...')
        super(UseridSpider, self).__init__(*args, **kwargs)
        self.changeKey(key)

#https://m.weibo.cn/api/container/getIndex?uid=1887790981&type=uid&value=1887790981    
# def start_requests(self):
    #      idList = []
        # con=pymysql.connect(
        #     host='127.0.0.1',  # 数据库地址
        #     port=3306,  # 数据库端口
        #     db='scrapymysql',  # 数据库名
        #     user='root',  # 数据库用户名
        #     passwd='s19990615z',  # 数据库密码
        #     charset='utf8',  # 编码方式
        #     use_unicode=True)
        # cur= con.cursor()
        # print('successfully connect!')
#        cur.execute('select userid from 东南大学_findsons')
#       print(cur.fetchall())
#         for userid in cur.fetchall():
#             idList.append(userid[0])
#         con.close()
#         print('close')

        # for uid in idList:
        #     url ='https://m.weibo.cn/api/container/getIndex?containerid=230283'+ uid +'_-_INFO'
        #     yield Request(url,callback=self.parse)

    def parse(self, response):
        ss = json.loads(response.body)
        cards = ss['data']['cards']
        item = useridItem()
        if（ss['ok']==0):
            uid=re.findall('230283(.*?)_-_',response.url)[0]
            req=requests.get('https://m.weibo.cn/api/container/getIndex?uid='+uid+'&type=uid&value='+uid)
            req_json=json.loads(req.text)
            item['userName']=req_json['userInfo']['screen_name']
            yield item
        elif()   
            item['userName']=cards[0]['card_group'][1]['item_content']
            item['sex']=cards[1]['card_group'][1]['item_content']
            item['location']=cards[1]['card_group'][2]['item_content']
            item['userid']=re.findall('230283(.*?)_-_',response.url)[0]
            yield item

