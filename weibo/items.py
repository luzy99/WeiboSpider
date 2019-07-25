# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RootknotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mid = scrapy.Field()
    flag = scrapy.Field()


class FindsonsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mid = scrapy.Field()
    pid = scrapy.Field()
    userid = scrapy.Field()
    verified_type = scrapy.Field()
    text = scrapy.Field()
    created_at = scrapy.Field()
    reposts_count = scrapy.Field()
    comments_count = scrapy.Field()
    attitudes_count = scrapy.Field()
    followers_count = scrapy.Field()
    follow_count = scrapy.Field()
    rootknot = scrapy.Field()
    generation = scrapy.Field()
