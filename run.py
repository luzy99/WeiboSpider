import scrapy
from scrapy.crawler import CrawlerProcess
from weibo.spiders.find_sons import FindSonsSpider
from weibo.spiders.rootknot import RootknotSpider
import time
from scrapy.settings import Settings
from weibo import settings as my_settings

crawler_settings = Settings()
crawler_settings.setmodule(my_settings)
process = CrawlerProcess(settings=crawler_settings)

process.crawl(RootknotSpider, '测试2', 'key')
process.crawl(FindSonsSpider, '测试2', 'key')
process.start()  # the script will block here until all crawling jobs are finished
