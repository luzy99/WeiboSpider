# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
from ..items import IpsItem
from bs4 import BeautifulSoup
import lxml
import re

class IpSpider5Spider(scrapy.Spider):
    name = 'ip_spider5'
    allowed_domains = ['ip3366.net']
    start_urls = ["http://www.ip3366.net/free/?stype=1&page={}/".format(i) for i in range(1,100)]

    def parse(self, response):
        soup=BeautifulSoup(response.body,"lxml")
        Text=str(soup.find_all('td'))
        ips=re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',Text) 
        ports=re.findall(r'\d{1,5}',Text)
        item=IpsItem()
        for ip,port in zip(ips,ports):
            item['ip']=ip
            item['port']=port
            yield item