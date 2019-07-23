# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from weibo import settings
from weibo.items import FindsonsItem
from weibo.items import RootknotItem


class RootknotPipeline(object):
    tableName = ''

    def open_spider(self, spider):
        if spider.name == 'rootknot':
            self.tableName = spider.key + '_rootknot'
            self.conn = pymysql.connect(host=settings.MYSQL_HOST,
                                        user=settings.MYSQL_USER,
                                        passwd=settings.MYSQL_PASSWD,
                                        db=settings.MYSQL_DBNAME, charset='utf8')
            self.cur = self.conn.cursor()
            sql = "CREATE TABLE IF NOT EXISTS `weibo`.`{}` "\
                "(`mid` varchar(255) NOT NULL,`flag` tinyint(1) NOT NULL,"\
                "PRIMARY KEY (`mid`))".format(self.tableName)
            self.cur.execute(sql)
            self.conn.commit()

    def process_item(self, item, spider):
        if isinstance(item, RootknotItem):
            mid = item.get("mid")
            flag = item.get("flag")

            sql = "insert ignore into {}(mid, flag) VALUES (%s,%s)".format(
                self.tableName)
            self.cur.execute(sql, (mid, flag))
            self.conn.commit()
        return item

    def close_spider(self, spider):
        if spider.name == 'rootknot':
            self.cur.close()
            self.conn.close()


class FindsonsPipeline(object):
    tableName = ''

    def open_spider(self, spider):
        #if spider.name == 'find_sons':
        self.tableName = spider.key + '_findsons'
        self.conn = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER,
                                    passwd=settings.MYSQL_PASSWD, db=settings.MYSQL_DBNAME, charset='utf8')
        self.cur = self.conn.cursor()
        sql = "CREATE TABLE IF NOT EXISTS `weibo`.`{}` (`mid` varchar(255) NOT NULL,`pid` varchar(255) NULL," \
            "`userid` varchar(255) NULL,`verified_type` varchar(255) NULL,`text` varchar(2555) NULL," \
            "`created_at` timestamp(0) NULL,`reposts_count` int(10) NULL,`comments_count` int(10) NULL," \
            "`attitudes_count` int(10) NULL,`followers_count` int(10) NULL ,`follow_count` int(10) NULL ," \
            "PRIMARY KEY (`mid`))".format(self.tableName)
        self.cur.execute(sql)
        self.conn.commit()

    def process_item(self, item, spider):
        if isinstance(item, FindsonsItem):
            pid = item.get("pid", "N/A")
            mid = item.get("mid", "N/A")
            userid = item.get("userid", "N/A")
            verified_type = item.get("verified_type")
            text = item.get("text", "N/A")
            created_at = item.get("created_at", "N/A")
            reposts_count = item.get("reposts_count", "N/A")
            comments_count = item.get("comments_count", "N/A")
            attitudes_count = item.get("attitudes_count", "N/A")
            followers_count = item.get("followers_count", "N/A")
            follow_count = item.get("follow_count","N/A")
            print(item)
            sql = "insert ignore into {}(mid, pid, userid, verified_type, text" \
                ", created_at, reposts_count, comments_count, attitudes_count," \
                " followers_count, follow_count) VALUES " \
                "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(self.tableName)
            self.cur.execute(sql, (mid, pid, userid, verified_type, text,
                                   created_at, reposts_count, comments_count,
                                   attitudes_count, followers_count, follow_count))
            self.conn.commit()
        return item

    def close_spider(self, spider):
        if spider.name == 'find_sons':
            self.cur.close()
            self.conn.close()
