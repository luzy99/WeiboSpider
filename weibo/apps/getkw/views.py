from django.shortcuts import render
import MySQLdb

# Create your views here.
def getkw(request):
    if request.method == "POST":
        keyword = request.POST.get('keyword','')
    return (render(request,"input.html"))