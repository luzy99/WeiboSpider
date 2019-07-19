from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ips.spiders.ip_spider1 import IpSpider1Spider
from ips.spiders.ip_spider2 import IpSpider2Spider
from ips.spiders.ip_spider3 import IpSpider3Spider
from ips.spiders.ip_spider4 import IpSpider4Spider


def run():
    setting = get_project_settings()
    process = CrawlerProcess(setting)

    process.crawl(IpSpider1Spider)
    process.crawl(IpSpider2Spider)
    process.crawl(IpSpider3Spider)
    process.crawl(IpSpider4Spider)
    process.start()  # the script will block here until all crawling jobs are finished


if __name__ == "__main__":
    run()
