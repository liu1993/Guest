from django.shortcuts import render
from django.http import *
# Create your views here.
def index(request):
    return render(request,'index.html')

def login_aciton(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        if username == 'admin' and password == 'qweqwe':
            #路径重定向
            response= HttpResponseRedirect('/event_manage/')
            response.set_cookie('user',username,3600)
            return response
            # return HttpResponse("login success!")
        else:
            return render(request,'index.html',{'error':'username or password error!'})

def event_manage(request):
    username = request.COOKIES.get('user','')
    return render(request,"event_manage.html",{'user':username})