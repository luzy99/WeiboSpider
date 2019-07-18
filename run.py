from scrapy.crawler import CrawlerProcess
from weibo.spiders.find_sons import FindSonsSpider
from weibo.spiders.rootknot import RootknotSpider
from scrapy.settings import Settings
from weibo import settings as my_settings
import sys


def run(kw):
    crawler_settings = Settings()
    crawler_settings.setmodule(my_settings)
    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(RootknotSpider, kw, 'key')
    process.crawl(FindSonsSpider, kw, 'key')
    process.start()  # the script will block here until all crawling jobs are finished


if __name__ == "__main__":
    try:
        kw = sys.argv[1]
        print(kw)
        run(kw)
    except:
        print('[Input ERROR]')