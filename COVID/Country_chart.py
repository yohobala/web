import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pandas as pd
import  seaborn as sns
import  numpy as np
import csv
import sys
import json
import os
import django

from pyecharts import options as opts
from pyecharts.charts import Bar,Page,Tab,Pie,Timeline,Grid
from pyecharts.faker import Faker

from crawler.crawlerFromWHO import transform_time


def death_histogram(list,title,name):
    x_list = []
    y_list = []
    for i in list:
        x_list.append(transform_time(i[0]))
        y_list.append(i[5])
    histogram = (
        Bar()
            .add_xaxis(x_list)
            .add_yaxis('新增死亡',y_list, color=Faker.rand_color())
            .set_global_opts(datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
                             )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False)
                             )
    )
    return histogram
def CumulativeDeaths_histogram(list,title,name):
    x_list = []
    y_list = []
    for i in list:
        x_list.append(transform_time(i[0]))
        y_list.append(i[6])
    histogram = (
        Bar()
            .add_xaxis(x_list)
            .add_yaxis('累计死亡',y_list, color=Faker.rand_color())
            .set_global_opts(datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
                             )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False)
                             )
    )
    return histogram

def Confirmed_histogram(list,title,name):
    x_list = []
    y_list = []
    for i in list:
        x_list.append(transform_time(i[0]))
        y_list.append(i[7])
    histogram = (
        Bar()
            .add_xaxis(x_list)
            .add_yaxis('新增确诊',y_list, color=Faker.rand_color())
            .set_global_opts(datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
                             )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False)
                             )
    )
    return histogram

def CumulativeConfirmed_histogram(list,title,name):
    x_list = []
    y_list = []
    for i in list:
        x_list.append(transform_time(i[0]))
        y_list.append(i[8])
    histogram = (
        Bar()
            .add_xaxis(x_list)
            .add_yaxis('累计确诊',y_list, color=Faker.rand_color())
            .set_global_opts(datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
                             )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False)
                             )
    )
    return histogram
def timeline(list,title,name):
    attr = Faker.choose()
    tl = Timeline()
    for i in list:
        x_list = ['每日死亡','累计死亡','每日确诊','累计确诊']
        y_list = []
        for x in range(5,9):
            y_list.append(i[x])
        histogram = (
            Bar()
                .add_xaxis(x_list)
                .add_yaxis(name, y_list, color=Faker.rand_color())
        )
        tl.add(histogram, "{}年".format(transform_time(i[0])))
    return tl

def tab_layout(list,title,name):
    tab = Tab()
    tab.add(death_histogram(list,title,name), "每日死亡")
    tab.add(CumulativeDeaths_histogram(list,title,name),'累计死亡')
    tab.add(Confirmed_histogram(list,title,name), "每日确诊")
    tab.add(CumulativeConfirmed_histogram(list,title,name),'累计确诊')
    tab.add(timeline(list,title,name),'时间轴')
    tab.render(name+'.html')

def page_layout(list,title,name):
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        death_histogram(list,title,name),
        CumulativeDeaths_histogram(list,title,name),
        Confirmed_histogram(list,title,name),
        CumulativeConfirmed_histogram(list,title,name),
        timeline(list,title,name),
    )
    page.render("templates/COVID/"+name+'.html')



if __name__ == '__main__':
    # mac下配置 font 为中文字体，自己去该路径找到自己电脑自带的字体
    font = FontProperties(fname='/System/Library/Fonts/STHeiti Medium.ttc')

    # 打开文件
    f = open(os.path.dirname(os.getcwd())+'/crawler/ByName_COVID-19.json', 'r')
    #获得一个字典格式的数据
    data = json.load(f)
    #从字典中提取出疫情数据所在的列表
    country_line = data['rows']
    DataList = []
    name = 'AF'  #第一个国家阿富汗
    for i in country_line:
            list = []
            if name == i[1] or name == i[2] or name  == i[3]:
                for x in range(9):
                    list.append(i[x])
                DataList.append(list)
                name = i[2]
            else:
                page_layout(DataList, name + "疫情", name)
                print(name)
                DataList = []
                for x in range(9):
                    list.append(i[x])
                DataList.append(list)
                name = i[2]



