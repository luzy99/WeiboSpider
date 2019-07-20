# -*- coding: utf-8 -*-
import scrapy
from ..items import IpsItem
import re

class IpSpider2Spider(scrapy.Spider):
    name = 'ip_spider2'
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/nn/{}'.format(i) for i in range(2,400)]

    def parse(self, response):
        ips=response.css('#ip_list>tr.odd>td:nth-of-type(2)::text').extract()
        #ips=soup.find_all('td',attrs={'data-title':'IP'})
        ports=response.css('#ip_list>tr.odd>td:nth-of-type(3)::text').extract()
        #ports=soup.find_all('td',attrs={'data-title':'PORT'})
        https=response.css('#ip_list>tr.odd>td:nth-of-type(6)::text').extract()
        item=IpsItem()
        for ip,port,http in zip(ips,ports,https):
            item['ip']=ip
            item['port']=port
            item['http']=http
            yield item
