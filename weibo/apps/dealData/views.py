from django.shortcuts import render
from pyecharts.charts.basic_charts import pie
import csv


# Create your views here.
def deal(request):
    #select * from table into outfile 'log/data.csv';
    f = open('log/测试_userinfo.csv', encoding='utf-8', errors='ignore')
    L = list(csv.reader(f))
    #print(L)
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
    piechart.render('templates/male-female.html')
    return render(request,'male-female.html')