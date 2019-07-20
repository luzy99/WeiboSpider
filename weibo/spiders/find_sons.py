# -*- coding: utf-8 -*-
import scrapy
import pymysql
from weibo import settings
import json
import re
from ..items import FindsonsItem
import time
import requests
# from weibo.spiders.rootknot import RootknotSpider


class FindSonsSpider(scrapy.Spider):
    name = 'find_sons'
    allowed_domains = ['m.weibo.cn']
    start_urls = []
    key = ''
    keylists = ('',)

    @classmethod
    def changeKey(cls, key):
        cls.key = key

    def __init__(self, key=None, *args, **kwargs):
        super(FindSonsSpider, self).__init__(*args, **kwargs)
        self.changeKey(key)

    def start_requests(self):
        self.keylists = self.getkeys()
        if self.keylists == -1:
            return
        else:
            self.start_urls = [
                'https://m.weibo.cn/detail/{}'.format(result[0]) for result in self.keylists]
            for url in self.start_urls:
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        render_data = re.findall(
            'render_data=\[(.+)\]\[0\]\|\|', response.text.replace(' ', '').replace('\n', ''))[0]

        data = json.loads(render_data)
        status = data['status']

        item = FindsonsItem()
        item['mid'] = status['id']
        item['pid'] = '0'
        item['userid'] = status['user']['id']
        item['verified_type'] = status['user']['verified_type']
        reg = re.compile('<[^>]*>')
        item['text'] = reg.sub('', status['text'])
        item['created_at'] = status['created_at']
        item['created_at'] = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.strptime(item['created_at'], '%a%b%d%H:%M:%S%z%Y'))
        item['reposts_count'] = status['reposts_count']
        item['comments_count'] = status['comments_count']
        item['attitudes_count'] = status['attitudes_count']

        if item['reposts_count'] == 0:
            pass
        else:
            resp = requests.get(
                'https://m.weibo.cn/api/statuses/repostTimeline?id={}&page=1'.format(item['mid']))
            resp.encoding = 'utf-8'
            resp_json = json.loads(resp.text)
            if resp_json['ok'] == 1:
                pages = resp_json['data']['max']
                for page in range(1, pages):
                    yield scrapy.Request('https://m.weibo.cn/api/statuses/repostTimeline?id={}&page={}'.
                                         format(item['mid'], page), callback=self.search_son_list)
            else:
                item['pid'] = '-1'
        yield item

    def search_son_list(self, response):
        ss = json.loads(response.body)
        if ss['ok'] == 1:
            sonlist = ss['data']['data']
            for son in sonlist:
                yield scrapy.Request('https://m.weibo.cn/detail/{}'.format(son['id']), callback=self.getinfo)
        else:
            pass

    def getinfo(self, response):
        render_data = re.findall(
            'render_data=\[(.+)\]\[0\]\|\|', response.text.replace(' ', '').replace('\n', ''))[0]
        data = json.loads(render_data)
        status = data['status']

        item = FindsonsItem()
        item['mid'] = status['id']
        item['text'] = status['raw_text']
        pid_str = response.text.find("pidstr")
        if pid_str == -1:
            pid = status['retweeted_status']['id']
            if '//@' in item['text']:
                item['pid'] = '-' + pid
            else:
                item['pid'] = '+' + pid
        else:
            item['pid'] = '+' + status['pidstr']
        item['userid'] = status['user']['id']
        item['verified_type'] = status['user']['verified_type']
        item['created_at'] = status['created_at']
        item['created_at'] = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.strptime(item['created_at'], '%a%b%d%H:%M:%S%z%Y'))
        item['reposts_count'] = status['reposts_count']
        item['comments_count'] = status['comments_count']
        item['attitudes_count'] = status['attitudes_count']
        #pages = (item['reposts_count'] // 9) + 1
        yield item

        '''if status['reposts_count'] == 0:
            pass
        else:
            for page in range(1, pages):
                yield scrapy.Request('https://m.weibo.cn/api/statuses/repostTimeline?id={}&page={}'.
                                     format(status['id'], page), callback=self.search_son_list)'''

    def getkeys(self):
        mydb = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER,
                               passwd=settings.MYSQL_PASSWD, db=settings.MYSQL_DBNAME, charset='utf8')
        mycursor = mydb.cursor()
        count = 5
        while count > 0:
            try:
                mycursor.execute("SELECT mid FROM {} WHERE flag = 0".format(
                    self.key+'_rootknot'))
                myresult = mycursor.fetchall()
                mycursor.execute("UPDATE {} SET flag = 1 WHERE flag = 0".format(
                    self.key+'_rootknot'))
                mydb.commit()
                if len(myresult) == 0:
                    time.sleep(2)
                    count -= 1
                else:
                    return myresult
            except:
                print("Select is failed")
                time.sleep(5)
        print('No more rootknots')
        return -1
