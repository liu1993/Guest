from django.shortcuts import render
from django.http import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event
from sign.models import Guest

# Create your views here.
def index(request):
    return render(request,'index.html')

def login_aciton(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        # if username == 'admin' and password == 'qweqwe':
        user = auth.authenticate(username=username,password=password)#帐号认证 与数据库中的数据进行匹配
        if user is not None:
            auth.login(request,user) #登录
            # response.set_cookie('user',username,3600) #添加浏览器cookie
            request.session['user']=username #将session信息记录到浏览器
            #路径重定向
            response= HttpResponseRedirect('/event_manage/')
            return response
            # return HttpResponse("login success!")
        else:
            return render(request,'index.html',{'error':'username or password error!'})

@login_required
def event_manage(request):
    event_list = Event.objects.all()
    # username = request.COOKIES.get('user','')#读取浏览器cookie
    username = request.session.get('user','') #读取浏览器session
    return render(request,"event_manage.html",{'user':username,'events':event_list})

@login_required
def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get('name','')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,'event_manage.html',{'user':username,'events':event_list})

@login_required
def guest_manage(request):
    username = request.session.get('user','')
    guest_list = Guest.objects.all()
    return render(request,'guest_manage.html',{'user':username,'guests':guest_list})