# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ..items import RootknotItem


class RootknotSpider(scrapy.Spider):
    name = 'rootknot'
    allowed_domains = ['m.weibo.cn']
    key = ''
    start_urls = []

    @classmethod
    def changeKey(cls, key):
        cls.key = key

    def __init__(self, key=None, *args, **kwargs):
        super(RootknotSpider, self).__init__(*args, **kwargs)
        self.changeKey(key)
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D60%26q%3D' + \
            key+'&page_type=searchall'
        self.start_urls.append(url)
        for i in range(2, 3):
            self.start_urls.append(url+'&page='+str(i))

    def parse(self, response):
        ss = json.loads(response.body)
        bloglist = ss['data']['cards'][0]['card_group']

        for i in bloglist:
            if "retweeted_status" in i['mblog'].keys():
                print('转发')
                mid = i['mblog']['retweeted_status']['id']
            else:
                print('原创')
                mid = i['mblog']['id']
            yield scrapy.Request(
                'https://m.weibo.cn/api/statuses/repostTimeline?id={}&page=1'.format(mid), callback=self.getpage, meta={'mid': mid})

    def getpage(self, response):
        item = RootknotItem()

        resp_json = json.loads(response.body)
        if resp_json['ok'] == 1:
            pages = resp_json['data']['max']
        else:
            pages = 1
        mid = response.meta['mid']
        for p in range(0, pages//10+1):
            item['mid'] = 'id={}&page={}'.format(mid, 10*p+1)
            yield item
