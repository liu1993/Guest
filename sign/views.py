from django.shortcuts import render
from django.http import  HttpResponse
# Create your views here.
def index(request):
    return render(request,'index.html')

def login_aciton(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        if username == 'admin' and password == 'qweqwe':
            return HttpResponse('login success!')
        else:
            return render(request,'index.html',{'error':'username or password error!'})