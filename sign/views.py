from django.shortcuts import render
from django.http import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event
from sign.models import Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger  # 分页
from django.shortcuts import render,get_object_or_404 #签到

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

# @login_required
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
    paginator = Paginator(guest_list,2) # 对guestlist分页，每页条数据
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page) # 获取page页
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request,'guest_manage.html',{'user':username,'guests':contacts}) #返回当前页数据

#签到页面
@login_required
def sign_index(request,event_id):
    event = get_object_or_404(Event,id=event_id)#从Event的model中获得对应id对象
    return render(request,'sign_index.html',{'event':event})

@login_required
def sign_index_action(request,event_id):
    event = get_object_or_404(Event,id=event_id)
    phone = request.POST.get('phone','')

    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'phone error'})

    result = Guest.objects.filter(phone=phone,event_id=event_id)
    if not result:
        return render(request,'sign_index.html',{'event:':event,'hint':'user has sign in'})
    else:
        Guest.objects.filter(phone=phone,event_id=event_id).update(sign ='1')
        return  render(request,'sign_index.html',{'event':event,'hint':'sign in success!','guest':result})


@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response