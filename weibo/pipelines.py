# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from weibo import settings
from weibo.spiders.rootknot import RootknotSpider


class RootknotPipeline(object):
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

    tableName = RootknotSpider.key + '_' + RootknotSpider.name

    def __init__(self):
        self.conn = pymysql.connect(host=settings.MYSQL_HOST,
                                    user=settings.MYSQL_USER,
                                    passwd=settings.MYSQL_PASSWD,
                                    db=settings.MYSQL_DBNAME, charset='utf8')
        self.cur = self.conn.cursor()
        sql = "CREATE TABLE IF NOT EXISTS `weibo`.`{}` "\
            "(`mid` varchar(20) NOT NULL,`flag` tinyint(1) NOT NULL,"\
            "PRIMARY KEY (`mid`))".format(self.tableName)
        self.cur.execute(sql)
        self.conn.commit()

    def process_item(self, item, spider):
        mid = item.get("mid")
        flag = item.get("flag")
        # userid = item.get("userid", "N/A")
        # verified_type = item.get("verified_type", "N/A")
        # text = item.get("text", "N/A")
        # created_at = item.get("created_at", "N/A")

        sql = "insert ignore into {}(mid, flag) VALUES (%s,%s)".format(
            self.tableName)
        self.cur.execute(sql, (mid, flag))
        self.conn.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
