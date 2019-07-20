from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pymysql
import time
import requests
from ips import settings
from ips.spiders.ip_spider1 import IpSpider1Spider
from ips.spiders.ip_spider2 import IpSpider2Spider
from ips.spiders.ip_spider3 import IpSpider3Spider
from ips.spiders.ip_spider4 import IpSpider4Spider

connect = pymysql.connect(
host= '127.0.0.1',
db= 'ips',
user= 'root',
passwd= 'root',
charset='utf8',
use_unicode=True)
cursor = connect.cursor()

def test_number():
    while True:
        sql="SELECT count(*) FROM ip;"
        ipNumber=cursor.execute(sql)
        if ipNumber < 500:
            run()
            time.sleep(3)
            
def test_useful():
    sql="SELECT *  FROM ip;"
    try:
    # 执行SQL语句
        cursor.execute(sql)
        result = cursor.fetchone()
        url="http://m.weibo.cn"
        while result!=None:
            ips=result[0]
            port=result[1]
            http=result[2]
            proxy=ips+":"+port
            try:
                res=requests.get(url,timeout=3,proxies={http:proxy } )
                if res.status_code != 200:
                    sql = "DELETE FROM ip WHERE ip = ips"
                    cursor.execute(sql)
                    connect.commit()
            except:
                sql = "DELETE FROM ip WHERE ip = ips"
                cursor.execute(sql)
                connect.commit()  
            result = cursor.fetchone()
    except:
        print ("Error: unable to fetch data")

def run():
    setting = get_project_settings()
    process = CrawlerProcess(setting)

    process.crawl(IpSpider1Spider)
    process.crawl(IpSpider2Spider)
    process.crawl(IpSpider3Spider)
    process.crawl(IpSpider4Spider)
    process.start()  # the script will block here until all crawling jobs are finished

def close():
    cursor.close()
    connect.close()

if __name__ == "__main__":
    test_useful()
    test_number()
    close()
