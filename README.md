# WeiboSpider
调用微博搜索API搜索话题
查找转发树根节点，并存储在Mysql中
>使用了scrapy框架

```
scrapy crawl knotroot
```
运行,可加参数
key = 搜索内容

```
scrapy crawl rootknot -a key=xxx
```

运行run.py一键启动3个爬虫[rootknot, find_sons, UseridSpider]
```
python run.py KEY
```
基本实现分布式架构，可多线程运行
2019.7.25
前端页面初步整合，可通过页面键入文本启动后端爬虫

## [:warning:NOTICE]
#### Requirements
>pip install
```
pymsql
scrapy
scrapy-redis
redis
requests
pyecharts
jieba
echarts-countries-pypkg
pip install echarts-china-provinces-pypkg
pip install echarts-china-cities-pypkg
```
Thanks for @jhao104's [proxy_pool](https://github.com/jhao104/proxy_pool.git)
