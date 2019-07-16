# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from weibo import settings


class WeiboPipeline(object):
    # def __init__(self):
    #     host = '127.0.0.1'
    #     port = 27017
    #     dbName = 'mydb'
    #     client = pymongo.MongoClient(host=host, port=port)
    #     tdb = client[dbName]
    #     self.post = tdb['new']

    # def process_item(self, item, spider):
    #     article = dict(item)
    #     self.post.insert(article)
    #     return item
    def __init__(self):
        self.conn = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER,
                                    passwd=settings.MYSQL_PASSWD, db=settings.MYSQL_DBNAME, charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        mid = item.get("mid", "N/A")    
        userid = item.get("userid", "N/A")
        verified_type = item.get("verified_type", "N/A")
        text = item.get("text", "N/A")
        created_at = item.get("created_at", "N/A")

        sql = "insert ignore into rootknot(mid, userid, verified_type, text, created_at) VALUES (%s, %s, %s, %s, %s)"
        self.cur.execute(sql, (mid, userid, verified_type, text, created_at))
        self.conn.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
