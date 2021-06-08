from django.conf.urls import url
from  django.urls import path
from  . import  views #将当前目录下的views导入

urlpatterns = [

path('', views.index, name='COVID'),

path('world_TC/', views.world_TC, name='COVID'),

path('world_NC/', views.world_NC, name='COVID'),

path('world_TD/', views.world_TD, name='COVID'),

path('world_ND/', views.world_ND, name='COVID'),
]