# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class useridItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    userid = scrapy.Field()
    userName = scrapy.Field()
    sex = scrapy.Field()
    location = scrapy.Field()
#    registerTime = scrapy.Field()
