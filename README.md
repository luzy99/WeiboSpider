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