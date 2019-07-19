# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import requests
from ips import settings
from concurrent.futures import ThreadPoolExecutor


class IpsPipeline(object):
    executor = ThreadPoolExecutor(max_workers=12)

    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()
        sql = "CREATE TABLE IF NOT EXISTS `weibo`.`ips` "\
            "(`ip` varchar(20) NOT NULL,`port` varchar(6) NOT NULL,"\
            "PRIMARY KEY (`ip`))"
        self.cursor.execute(sql)
        self.connect.commit()

    def process_item(self, item, spider):
        ip = item["ip"]
        port = item["port"]

        self.executor.submit(self.checkip, (self, ip, port))

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

    def checkip(self, ip, port):
        proxy = ip+":"+port
        url = "http://www.baidu.com"
        try:
            res = requests.get(url, timeout=3, proxies={'http': proxy})
            print(proxy)
            print(res.status_code)
            if res.status_code != 200:
                print(proxy + " failed")
            else:
                print(proxy + "    ok")
                sql = "insert ignore into ips(ip,port) VALUES(%s,%s)"
                self.cursor.execute(sql, (ip, port))
                self.connect.commit()
        except:
            print(proxy + "    timeout")
