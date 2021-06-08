from django.conf.urls import url
from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
# namespace
app_name = '查看shp文件'

urlpatterns = [

#上传文件
path('', views.index, name='查看shp文件'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

