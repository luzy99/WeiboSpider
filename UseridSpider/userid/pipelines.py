# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors
import redis
from scrapy.exceptions import DropItem
from userid import settings

# redis_db = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True) #连接redis，相当于MySQL的conn
# redis_data_dict = "userId"  #key的名字，写什么都可以，这里的key相当于字典名称，而不是key值。


class useridPipeline(object):
    tableName = ''
    def process_item(self, item, spider):
        self.cursor.execute(
            """insert ignore into {}(userName, sex, location,userid)
            value (%s, %s, %s,%s)""".format(self.tableName),  # 纯属python操作mysql知识，不熟悉请恶补
            (item['userName'],  # item里面定义的字段和表字段对应
             item['sex'],
             item['location'],
             item['userid']
             ))

        # 提交sql语句
        self.connect.commit()
        print('item ok')
        return item  # 必须实现返回

    def open_spider(self, spider):
        self.tableName = spider.key + '_userinfo'
        # 连接数据库
        self.connect = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER,
                                       passwd=settings.MYSQL_PASSWD, db=settings.MYSQL_DBNAME, charset='utf8')

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
        sql = "CREATE TABLE IF NOT EXISTS `weibo`.`{}` (`userid` varchar(255) NOT NULL,"\
            "`userName` varchar(255) NULL,"\
            "`sex` varchar(255) NULL,"\
            "`location` varchar(255) NULL,"\
            "PRIMARY KEY (`userid`))".format(self.tableName)
        self.cursor.execute(sql)
        self.connect.commit()
        