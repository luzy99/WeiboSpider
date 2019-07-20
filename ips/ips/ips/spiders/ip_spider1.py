# -*- coding: utf-8 -*-
import scrapy
from ..items import IpsItem
import re

class IpSpider1Spider(scrapy.Spider):
    name = 'ip_spider1'
    allowed_domains = ['kuaidaili.com']
    start_urls = ["https://www.kuaidaili.com/free/inha/{}/".format(i) for i in range(101,400)]

    def parse(self, response):
        ips=response.css('td[data-title="IP"]::text').extract()
        #ips=soup.find_all('td',attrs={'data-title':'IP'})
        ports=response.css('td[data-title="PORT"]::text').extract()
        #ports=soup.find_all('td',attrs={'data-title':'PORT'})
        https=response.css('td[data-title="类型"]::text').extract()
        item=IpsItem()
        for ip,port,http in zip(ips,ports,https):
            item['ip']=ip
            item['port']=port
            item['http']=http

            yield item
