# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from weibo import settings
from weibo.items import FindsonsItem
from weibo.items import RootknotItem
import redis


class RootknotPipeline(object):
    tableName = ''

    def open_spider(self, spider):
        if spider.name == 'rootknot':
            pool = redis.ConnectionPool(
                host='localhost', port=6379, decode_responses=True)
            self.r = redis.Redis(connection_pool=pool)
            self.r.delete('rootknot')

    def process_item(self, item, spider):
        if isinstance(item, RootknotItem):
            mid = item.get("mid")
            self.r.rpush('rootknot', mid)
        return item

    def close_spider(self, spider):
        pass


class FindsonsPipeline(object):
    tableName = ''

    def open_spider(self, spider):
        # if spider.name == 'find_sons':
        self.tableName = spider.key + '_findsons'
        self.conn = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER,
                                    passwd=settings.MYSQL_PASSWD, db=settings.MYSQL_DBNAME, charset='utf8')
        self.cur = self.conn.cursor()
        sql = "CREATE TABLE IF NOT EXISTS `weibo`.`{}` (`mid` varchar(255) NOT NULL,`pid` varchar(255) NULL," \
            "`userid` varchar(255) NULL,`verified_type` varchar(255) NULL,`text` varchar(2555) NULL," \
            "`created_at` timestamp(0) NULL,`reposts_count` int(10) NULL,`comments_count` int(10) NULL," \
            "`attitudes_count` int(10) NULL,`followers_count` int(10) NULL ,`follow_count` int(10) NULL ,`rootknot` varchar(255) NULL," \
            "`generation` int(10) NULL, PRIMARY KEY (`mid`))".format(self.tableName)
        self.cur.execute(sql)
        self.conn.commit()
        pool = redis.ConnectionPool(
            host='localhost', port=6379, decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)
        self.r.delete('userid')

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
            follow_count = item.get("follow_count", "N/A")
            rootknot = item.get("rootknot", "N/A")
            generation = item.get("generation", "N/A")
            sql = "insert ignore into {}(mid, pid, userid, verified_type, text" \
                ", created_at, reposts_count, comments_count, attitudes_count," \
                " followers_count, follow_count, rootknot, generation) VALUES " \
                "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(self.tableName)
            self.cur.execute(sql, (mid, pid, userid, verified_type, text,
                                   created_at, reposts_count, comments_count,
                                   attitudes_count, followers_count, follow_count, rootknot, generation))
            self.conn.commit()

            self.r.rpush(
                'userid', 'https://m.weibo.cn/api/container/getIndex?containerid=230283'+str(userid)+'_-_INFO')
        return item

    def close_spider(self, spider):
        if spider.name == 'find_sons':
            self.cur.close()
            self.conn.close()
