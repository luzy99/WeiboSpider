# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ..items import RootknotItem


class RootknotSpider(scrapy.Spider):
    name = 'rootknot'
    allowed_domains = ['m.weibo.cn']
    key = '微博'
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
        for i in range(2, 6):
            self.start_urls.append(url+'&page='+str(i))

    def parse(self, response):
        ss = json.loads(response.body)
        bloglist = ss['data']['cards'][0]['card_group']
        for i in bloglist:
            yield scrapy.Request('https://m.weibo.cn/detail/'+i['mblog']['id'],
                                 callback=self.root_knot)

    def root_knot(self, response):
        retweet = response.text.find("retweeted_status")
        item = RootknotItem()
        if retweet == -1:
            print('原创')
            render_data = re.findall(
                'render_data=\[(.+)\]\[0\]\|\|',
                response.text.replace(' ', '').replace('\n', ''))[0]

            data = json.loads(render_data)
            status = data['status']
            item['mid'] = status['id']
        else:
            temp = response.text[retweet:retweet+200]
            rootid = re.findall(r'"id":.+"(.*?)",', temp, re.S)[0]
            print('转发自', rootid)
            item['mid'] = rootid
        item['flag'] = 0
        yield item
