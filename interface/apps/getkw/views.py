from django.shortcuts import render
import MySQLdb
import os

global keyword
# Create your views here.


def getkw(request):
    if request.method == "POST":
        global keyword
        keyword = request.POST.get('keyword', '')
        os.popen('cd ..&&python run.py {}'.format(keyword))
    return (render(request, "input.html"))
