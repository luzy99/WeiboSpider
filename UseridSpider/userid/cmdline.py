# -*- coding: utf-8 -*-
import os
import scrapy.cmdline
import sys


def cmdrun(kw):
    os.popen("scrapy crawl UseridSpider -a key={}".format(kw))
    os.popen("scrapy crawl UseridSpider -a key={}".format(kw))
    os.popen("scrapy crawl UseridSpider -a key={}".format(kw))
    os.popen("scrapy crawl UseridSpider -a key={}".format(kw))
    os.popen("scrapy crawl UseridSpider -a key={}".format(kw))

    print('启动成功')


if __name__ == "__main__":
    try:
        kw = sys.argv[1]
        print(kw)
        # run(kw)
        # run2(kw)
        cmdrun(kw)
    except:
        print('[Input ERROR]')
