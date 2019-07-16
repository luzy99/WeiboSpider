# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ..items import WeiboItem
import time


class WeiboSpider(scrapy.Spider):
    name = 'rootknot'
    allowed_domains = ['m.weibo.cn']
    key = '李彦宏 泼水'
    start_urls = [
        ('https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D60%26q%3D'+key+'&page_type=searchall')]

    def parse(self, response):
        ss = json.loads(response.body)
        bloglist = ss['data']['cards'][0]['card_group']

        for i in bloglist:
            yield scrapy.Request('https://m.weibo.cn/detail/'+i['mblog']['id'], callback=self.root_knot)
        for i in range(2, 6):
            try:
                yield scrapy.Request(response.url+'&page='+str(i), callback=self.search_url)
            except:
                continue

    def search_url(self, response):
        ss = json.loads(response.body)
        bloglist = ss['data']['cards'][0]['card_group']
        for i in bloglist:
            yield scrapy.Request('https://m.weibo.cn/detail/'+i['mblog']['id'], callback=self.root_knot)

    def root_knot(self, response):
        retweet = response.text.find("retweeted_status")
        if retweet == -1:
            print('原创')
            render_data = re.findall(
                'render_data=\[(.+)\]\[0\]\|\|', response.text.replace(' ', '').replace('\n', ''))[0]

            data = json.loads(render_data)
            status = data['status']

            item = WeiboItem()
            item['mid'] = status['id']
            item['userid'] = status['user']['id']
            item['verified_type'] = status['user']['verified_type']

            reg = re.compile('<[^>]*>')
            item['text'] = reg.sub('', status['text'])

            item['created_at'] = status['created_at']
            item['created_at'] = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.strptime(item['created_at'], '%a%b%d%H:%M:%S%z%Y'))

            print('mid:{} userid:{} V{} created_at:{}'.format(
                item['mid'], item['userid'], item['verified_type'], item['created_at']))
            print('转发：{} 评论：{} 赞：{}'.format(
                status['reposts_count'], status['comments_count'], status['attitudes_count']))
            yield item

        else:
            temp = response.text[retweet:retweet+200]
            pid = re.findall(r'"id":.+"(.*?)",', temp, re.S)[0]
            print('转发', pid)
            yield scrapy.Request('https://m.weibo.cn/detail/'+pid, callback=self.root_knot)
