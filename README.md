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