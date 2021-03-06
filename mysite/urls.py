"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path,include
from django.conf.urls import  url
from django.conf import settings
from django.views import static
#总链接，为了连接到每个app,如果不设置，urls里面就找不到，比如不设置COVID
#就不能打开127.0.0.1:8000/COVID
urlpatterns = [
    #主页
    path('',include('homepage.urls')),
    #小功能页面
    #得到卡密
    path('getCardPassword/',include('getCardPassword.urls')),
    path('dotDensity/', include('dot_density.urls')),
    path('COVID/', include('COVID.urls')),
    path('admin/', admin.site.urls),
    path('isogram/', include('isogram.urls')),
    path('showShp/', include('showShp.urls')),
    path('showLidar/', include('showLidar.urls')),
    path('drawContours/', include('drawContours.urls')),
    path('shadedRelief/', include('shaded_relief.urls')),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT }, name='static'),
]
