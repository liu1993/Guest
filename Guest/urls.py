"""Guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from sign import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),#后台管理页面
    url(r'^$',views.index),#根目录
    url(r'^index/',views.index),
    url(r'^login_action/$',views.login_aciton),
    url(r'^event_manage/',views.event_manage),
    url(r'^accounts/login/$',views.index),#尝试未登录直接到达登陆成功页面弹出的错误页面，引导用户至登录页面
    url(r'^search_name/',views.search_name),
    url(r'^guest_manage/',views.guest_manage)
]
