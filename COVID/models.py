from django.db import models
import os
import django



# Create your models here.
#这是这个app的数据库
class Country(models.Model):
    #设置了国家英文名称(english_name)，中文名称(chinese_name)，简写(atate_abbreviations)
    chinese_name = models.CharField(max_length=200,default='')
    english_name = models.CharField(max_length=200,default='')
    atate_abbreviations = models.CharField(max_length=200,default='')
    def data (self):#返回一个对象的信息，注意要用self.
        return self.chinese_name, self.english_name, self.atate_abbreviations

class Data(models.Model):
    #分别设置时间（time_stamp)、新增死亡(new_deaths)、累计死亡(Cumula_deaths)、新增确诊(new_confirmed)、累计确诊(total_confirmed)
    time_stamp = models.CharField(max_length=200,default='')
    new_deaths = models.BigIntegerField()#BigIntegerField表示64位的正负整数，'new deaths'定义的人类可读的名字
    cumula_deaths = models.BigIntegerField()
    new_confirmed = models.BigIntegerField()
    cumula_confirmed = models.BigIntegerField()
    country = models.ForeignKey(Country,on_delete=models.CASCADE)#这是一个外部键
    def data (self):
        return self.time_stamp, self.new_deaths, self.cumula_deaths, self.new_confirmed, self.cumula_confirmed
