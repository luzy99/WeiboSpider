from django.shortcuts import render
from example.commons import Collector, Faker
from pyecharts import options as opts
from pyecharts.charts import Line, Page, Map, WordCloud, Bar
from pyecharts.charts.basic_charts import pie
from pyecharts.globals import ChartType, SymbolType
import csv
import time
import jieba.analyse
import datetime
import os
from ..getkw import views
import pymysql
from static.loadjson import writefile
from .dealCsv import read_mysql_to_csv


def deal(request):
    # print(views.keyword)

    read_mysql_to_csv('log/findsons.csv', '{}_findsons'.format(views.keyword))
    read_mysql_to_csv('log/userinfo.csv', '{}_userinfo'.format(views.keyword))
    writefile(views.keyword)  # json
    os.remove('static/ceng.html')
    dealceng()
    return render(request, 'home.html')

# 总览的视图函数
# def deal(request):
#     os.remove('static/ceng.html')
#     dealceng()
#     return render(request,'home.html')

# 传播分析的视图函数


def dealfenxi(request):
    os.remove('static/time-depending.html')
    dealfenxishijian()
    return render(request, 'home2.html')

# 传播分析中绘制时间变化表的函数


def dealfenxishijian():
    C = Collector()
    f = open('log/cxk_findsons.csv', encoding='utf-8', errors='ignore')
    L = list(csv.reader(f))
    time_dist = {}
    clock_dist = {}
    time_list = []

    for row in L[1:]:
        tem = datetime.datetime.strptime(str(row[5]), "%d/%m/%Y %H:%M:%S")
        temt = tem.strftime("%Y-%m-%d %H:%M:%S")
        time_list.append(temt)

    for time in time_list:
        if (time.split(':')[0]) in clock_dist:
            clock_dist[time.split(':')[0]] += 1
        else:
            clock_dist[time.split(':')[0]] = 1

    choose = [key for key, value in clock_dist.items()]
    values = [value for key, value in clock_dist.items()]

    @C.funcs
    def line_areastyle_boundary_gap() -> Line:
        c = (
            Line()
            .add_xaxis(choose)
            .add_yaxis("商家A", values, is_smooth=True)
            .set_series_opts(
                areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="热度随时间分布图"),
                xaxis_opts=opts.AxisOpts(
                    axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                    is_scale=False,
                    boundary_gap=False,
                ),
            )
        )
        return c
    Page().add(*[fn() for fn, _ in C.charts]
               ).render('D:static/time-depending.html')

# 传播路径的视图函数


def deallujing(request):
    return render(request, 'home3.html')

# 传播路径层数视图


def dealceng():
    C = Collector()
    f = open('log/cxk_findsons.csv', encoding='utf-8', errors='ignore')
    L = list(csv.reader(f))
    data_dist = {}
    for row in L[1:]:
        rowed = str(int(row[3]) + 1)
        if (rowed in data_dist):
            data_dist[rowed] += 1
        else:
            data_dist[rowed] = 1

    choose = [key for key, value in data_dist.items()]
    values = [value for key, value in data_dist.items()]

    @C.funcs
    def bar_is_selected() -> Bar:
        c = (
            Bar()
            .add_xaxis(choose)
            .add_yaxis("商家A", values)
            .set_global_opts(title_opts=opts.TitleOpts(title="转发层数显示图"))
        )
        return c

    Page().add(*[fn() for fn, _ in C.charts]).render('D:static/ceng.html')

# 参与者信息的视图函数


def dealcanyu(request):
    os.remove('static/region-spreading.html')
    dealcanyudiqu()
    dealcanyugender()
    return render(request, 'home4.html')

# 绘制参与者地区分布的函数


def dealcanyudiqu():
    C = Collector()
    f = open('log\测试_userinfo.csv', encoding='utf-8', errors='ignore')
    L = list(csv.reader(f))
    print(L)
    data_dist = {}
    for row in L[1:]:
        rowed = str(row[3]).split()[0]
        if (rowed in data_dist):
            data_dist[rowed] += 1
        else:
            data_dist[rowed] = 1

    print(data_dist)

    @C.funcs
    def map_without_label() -> Map:
        c = (
            Map()
            .add("微博名", [list(z) for z in zip(data_dist.keys(), data_dist.values())], "china")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="转发用户地域分布展示"))
        )
        return c

    Page().add(*[fn() for fn, _ in C.charts]
               ).render('D:static/region-spreading.html')

# 绘制参与者男女比例函数


def dealcanyugender():
    f = open('log/测试_userinfo.csv', encoding='utf-8', errors='ignore')
    L = list(csv.reader(f))
    # print(L)
    male = 0
    female = 0
    for row in L[1:]:
        if row[2] == '女':
            female = female + 1
        else:
            male = male + 1
    attr = ["男", "女"]
    piechart = pie.Pie()
    piechart.add("男女比例图", [('男', male), ('女', female)])
    piechart.render('D:static/gender-spreading.html')

# 内容分析的视图函数


def dealneirong(request):
    dealneirongciyun()
    return render(request, 'home6.html')

# 制作词云的函数


def dealneirongciyun():
    C = Collector()
    f = open('log\cxk_findsons.csv', encoding='utf-8', errors='ignore')
    L = list(csv.reader(f))
    sentence = ''
    for row in L[1:]:
        sentence += str(row[4])
    words = jieba.analyse.extract_tags(
        sentence, topK=40, withWeight=True, allowPOS=())
    for word in words:
        if "转发" in word:
            words.remove(word)
    for word in words:
        if "微博" in word:
            words.remove(word)
    for word in words:
        if "##" in word:
            words.remove(word)

    @C.funcs
    def wordcloud_base() -> WordCloud:
        c = (
            WordCloud()
            .add("", words, word_size_range=[20, 100])
            .set_global_opts(title_opts=opts.TitleOpts(title="词云分析"))
        )
        return c

    Page().add(*[fn() for fn, _ in C.charts]).render('D:static/ciyun.html')
