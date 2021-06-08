from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# namespace
app_name = '点密度计算'

urlpatterns = [

path('', views.index, name='点密度计算'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)