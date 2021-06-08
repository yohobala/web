from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# namespace
app_name = '绘制等高线'

urlpatterns = [

#上传文件
path('', views.index, name='绘制等高线'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

