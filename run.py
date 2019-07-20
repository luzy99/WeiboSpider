from scrapy.crawler import CrawlerProcess
from weibo.spiders.find_sons import FindSonsSpider
from weibo.spiders.rootknot import RootknotSpider
from scrapy.settings import Settings
from weibo import settings as my_settings
import sys
from concurrent.futures import ThreadPoolExecutor
from scrapy import cmdline
import os


def run(kw):
    crawler_settings = Settings()
    crawler_settings.setmodule(my_settings)
    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(RootknotSpider, kw, 'key')
    #process.crawl(FindSonsSpider, kw, 'key')
    process.start()  # the script will block here until all crawling jobs are finished


def run2(kw):
    crawler_settings = Settings()
    crawler_settings.setmodule(my_settings)
    process = CrawlerProcess(settings=crawler_settings)

    #process.crawl(RootknotSpider, kw, 'key')
    process.crawl(FindSonsSpider, kw, 'key')
    process.start()  # the script will block here until all crawling jobs are finished


def cmdrun(kw):
    os.system("scrapy crawl rootknot -a key={}".format(kw))
    os.system("scrapy crawl find_sons -a key={}".format(kw))
    print('启动成功')


if __name__ == "__main__":
    try:
        kw = sys.argv[1]
        print(kw)
        # run(kw)
        run(kw)
       # cmdrun(kw)
    except:
        print('[Input ERROR]')
