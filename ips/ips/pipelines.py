# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import requests
from ips import settings

class IpsPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        ip=item["ip"]
        port=item["port"]
        proxy=ip+":"+port
        url="http://www.baidu.com"
        try:
            res=requests.get(url,timeout=3,proxies={'http':proxy } )
            print(proxy)
            print(res.status_code)
            if res.status_code != 200:
                print (proxy + " failed")
            else:
                print (proxy+ "    ok")
                sql="insert ignore into ip(ip,port) VALUES(%s,%s)"
                self.cursor.execute(sql,(ip,port))
                self.connect.commit()
        except:
            print (proxy+ "    timeout")
        
    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()
