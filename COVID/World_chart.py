import datetime
import json
import os
import time
from typing import List

import pyecharts.options as opts
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Timeline, Grid, Bar, Map, Pie, Line, Tab
from crawler.crawlerFromWHO import transform_time



def COVID_Data(file,day,timeStamp):
    #定义一个总的列表，里面存放所有数据，再定义一个字典，存放时间和每天的数据，再一个列表存放每天每个国家的数据
    #累计确诊 TC ,新增确诊 NC ,累计死亡 TD ,新增死亡 ND
    # 这是总列表
    TC_Total_list = []
    NC_Total_list = []
    TD_Total_list = []
    ND_Total_list = []
    # 四个数据最大数
    TC_max = 0
    NC_max = 0
    TD_max = 0
    ND_max = 0
    # 四个数据，每个数据的每天总和的列表
    TC_day_sum = []
    NC_day_sum = []
    TD_day_sum = []
    ND_day_sum = []
    while day <= timeStamp:
        # 这是字典，存放每天的数据
        TC_day_dict = {"time" : transform_time(day)}
        NC_day_dict = {"time" : transform_time(day)}
        TD_day_dict = {"time" : transform_time(day)}
        ND_day_dict = {"time" : transform_time(day)}
        # 这是列表，被上面那个字典包含
        TC_day_data = []
        NC_day_data = []
        TD_day_data = []
        ND_day_data = []
        # 每天的总和
        TC = 0
        NC = 0
        TD = 0
        ND = 0
        #先计算下四个数据每日总和
        for i in range(len(file)):
            if day == file[i][0]:  # 时间戳是不是一样
                if ND_max <= file[i][5]:
                    ND_max = file[i][5]
                if TD_max <= file[i][6]:
                    TD_max = file[i][6]
                if NC_max <= file[i][7]:
                    NC_max = file[i][7]
                if TC_max <= file[i][8]:
                    TC_max = file[i][8]
                ND = ND + file[i][5]
                TD = TD + file[i][6]
                NC = NC + file[i][7]
                TC = TC + file[i][8]
        for i in range(len(file)):
            # 这是每天每个国家的数据列表
            TC_list = []
            NC_list = []
            TD_list = []
            ND_list = []
            # 字典
            TC_dict = {}
            NC_dict = {}
            TD_dict = {}
            ND_dict = {}
            if day == file[i][0]:  # 时间戳是不是一样
                name = file[i][2]
                tc = file[i][8]
                if TC != 0:
                    percent_1 = tc / TC * 100
                else:
                    percent_1 = 0
                TC_list.append(tc)
                TC_list.append(percent_1)
                TC_list.append(name)
                TC_dict['name'] = name
                TC_dict['value'] = TC_list
                TC_day_data.append(TC_dict)

                nc = file[i][7]
                if NC != 0 :
                    percent_2 = nc / NC * 100
                else:
                    percent_2 = 0
                NC_list.append(nc)
                NC_list.append(percent_2)
                NC_list.append(name)
                NC_dict['name'] = name
                NC_dict['value'] = NC_list
                NC_day_data.append(NC_dict)

                td = file[i][6]
                if TD != 0:
                    percent_3 = td / TD * 100
                else:
                    percent_3 = 0
                TD_list.append(td)
                TD_list.append(percent_3)
                TD_list.append(name)
                TD_dict['name'] = name
                TD_dict['value'] = TD_list
                TD_day_data.append(TD_dict)

                nd = file[i][5]
                if ND != 0:
                    percent_4 = nd / ND * 100
                else:
                    percent_4 = 0
                ND_list.append(nd)
                ND_list.append(percent_4)
                ND_list.append(name)
                ND_dict['name'] = name
                ND_dict['value'] = ND_list
                ND_day_data.append(ND_dict)


        day = day + 86400000

        TC_day_sum.append(TC)
        TC_day_dict['data'] = TC_day_data
        TC_Total_list.append(TC_day_dict)

        NC_day_sum.append(NC)
        NC_day_dict['data'] = NC_day_data
        NC_Total_list.append(NC_day_dict)

        TD_day_sum.append(TD)
        TD_day_dict['data'] = TD_day_data
        TD_Total_list.append(TD_day_dict)

        ND_day_sum.append(ND)
        ND_day_dict['data'] = ND_day_data
        ND_Total_list.append(ND_day_dict)









    data = [TC_Total_list,TC_max,TC_day_sum,NC_Total_list,NC_max,NC_day_sum,TD_Total_list,TD_max,TD_day_sum,ND_Total_list,ND_max,ND_day_sum]

    return data




#转换时间戳为年月日格式
def transform_time(timeStamp):
    timeArray = time.localtime(timeStamp / 1000)
    date = time.strftime("%Y--%m--%d", timeArray)
    date = date.split('--')[1] +'月'+ date.split('--')[2]+'日'
    return date

def get_day_chart(day:str,data:list,minNum:int,maxNum:int,total_num:list):
    map_data = [
            [[x["name"], x["value"]] for x in d["data"]] for d in data if d["time"] == day
    ][0]
    min_data, max_data = (minNum, maxNum)
    data_mark: List = []
    i = 0
    for x in time_list:
        if x == day:
            data_mark.append(total_num[i])
        else:
            data_mark.append("")
        i = i + 1
    country = []
    values = []
    for i in map_data:
        country.append(i[0])
        values.append(i[1][0])
    map_chart = (
        Map()
            .add('国家',[list(z) for z in zip(country,values)], "world",zoom=0.7,center=[119.5, -60],is_roam=False)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=200),
            title_opts=opts.TitleOpts(
                title="" + str(day) + "全球疫情情况 数据来源：WHO",
                subtitle="",
                pos_left="center",
                pos_top="10",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=25, color="rgba(255,255,255, 0.9)"
                ),
            ),
            legend_opts=opts.LegendOpts(
                is_show = False,

            ),
        )
    )

    line_chart = (
        Line()
            .add_xaxis(time_list)
            .add_yaxis("", total_num)
            .add_yaxis(
            "",
            data_mark,
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="全球总人数", pos_left="72%", pos_top="5%"
            )
        )
    )

    bar_x_data = [x[0] for x in map_data]
    bar_y_data = [{"name": x[0], "value": x[1][0]} for x in map_data]
    bar = (
        Bar()
            .add_xaxis(xaxis_data=bar_x_data)
            .add_yaxis(
            series_name="",
            yaxis_data=bar_y_data,
            label_opts=opts.LabelOpts(
                is_show=False, position="right", formatter="{b} : {c}"
            ),
        )
            .reversal_axis()
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                max_=maxNum, axislabel_opts=opts.LabelOpts(is_show=False)
            ),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
            tooltip_opts=opts.TooltipOpts(is_show=True),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="10",
                pos_top="top",
                range_text=["High", "Low"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=min_data,
                max_=max_data,
            ),
        )
    )

    pie_data = [[x[0], x[1][0]] for x in map_data]
    pie = (
        Pie()
        .add(
            series_name="",
            data_pair=pie_data,
            radius=["15%", "35%"],
            center=["80%", "82%"],
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=1, border_color="rgba(0,0,0,0.3)"
            ),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True, trigger = "item",trigger_on = "mousemove|click",formatter="{b} {d}%"),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    grid_chart = (
        Grid()
        .add(
            bar,
            grid_opts=opts.GridOpts(
                pos_left="10", pos_right="45%", pos_top="50%", pos_bottom="5"
            ),
        )
        .add(
            line_chart,
            grid_opts=opts.GridOpts(
                pos_left="65%", pos_right="80", pos_top="10%", pos_bottom="50%"
            ),
        )
        .add(pie, grid_opts=opts.GridOpts(pos_left="45%", pos_top="60%"))
        .add(map_chart, grid_opts=opts.GridOpts(pos_bottom='80%'))
    )

    return grid_chart

if __name__ == "__main__":

    # 打开文件
    f = open(os.path.dirname(os.getcwd())+'/crawler/ByTime_COVID-19.json', 'r')
    # 获得一个字典格式的数据
    data = json.load(f)
    # 从字典中提取出疫情数据所在的列表
    file = data['rows']

    time_list = []
    Day = 1578441600000  # 初始日期2020年1月8号
    # 读取运行代码时的时间，并保留年月日，时间变成8：00：00，然后扩大1000倍，因为json文件里的时间戳到毫秒，并变成字符串格式
    now_time = datetime.datetime.now()
    timeStr = datetime.datetime.strftime(now_time, '%Y-%m-%d 08:00:00')
    timeStamp = int(time.mktime(time.strptime(timeStr, '%Y-%m-%d %H:%M:%S')) * 1000)
    while Day <= timeStamp:
        time_list.append(transform_time(Day))
        Day = Day + 86400000

    data = COVID_Data(file,1578441600000,timeStamp)


    #累计确诊
    timeline_1 = Timeline(
        init_opts=opts.InitOpts(width="calc(100vw)",
                                height="1000px",
                                theme=ThemeType.DARK,
                                page_title='全球疫情累计确诊'),
    )
    for y in time_list:
        g = get_day_chart(day=y,data=data[0],minNum=0,maxNum=data[1],total_num=data[2])
        timeline_1.add(g, time_point=str(y))

    timeline_1.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=5000,
        pos_left="null",
        pos_right="5",
        pos_top="20",
        pos_bottom="20",
        width="60",
        label_opts=opts.LabelOpts(is_show=True, color="#fff"),
        itemstyle_opts=opts.ItemStyleOpts(opacity=0.5),
    )

    #新增确诊
    timeline_2 = Timeline(
        init_opts=opts.InitOpts(width="1400px",
                                height="1000px",
                                theme=ThemeType.DARK,
                                page_title='全球新增确诊')
    )

    for y in time_list:
        g = get_day_chart(day=y,data=data[3],minNum=0,maxNum=data[4],total_num=data[5])
        timeline_2.add(g, time_point=str(y))

    timeline_2.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=5000,
        pos_left="null",
        pos_right="5",
        pos_top="20",
        pos_bottom="20",
        width="60",
        label_opts=opts.LabelOpts(is_show=True, color="#fff"),
    )

    # 累计死亡

    timeline_3 = Timeline(
        init_opts=opts.InitOpts(width="1400px",
                                height="1000px",
                                theme=ThemeType.DARK,
                                page_title='全球累计死亡')
    )

    for y in time_list:
        g = get_day_chart(day=y, data=data[6], minNum=0, maxNum=data[7], total_num=data[8])
        timeline_3.add(g, time_point=str(y))

    timeline_3.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=5000,
        pos_left="null",
        pos_right="5",
        pos_top="20",
        pos_bottom="20",
        width="60",
        label_opts=opts.LabelOpts(is_show=True, color="#fff"),
    )

    # 新增死亡

    timeline_4 = Timeline(
        init_opts=opts.InitOpts(width="1400px",
                                height="1000px",
                                theme=ThemeType.DARK,
                                page_title='全球新增死亡')
    )

    for y in time_list:
        g = get_day_chart(day=y, data=data[9], minNum=0, maxNum=data[10], total_num=data[11])
        timeline_4.add(g, time_point=str(y))

    timeline_4.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=5000,
        pos_left="null",
        pos_right="5",
        pos_top="20",
        pos_bottom="20",
        width="60",
        label_opts=opts.LabelOpts(is_show=True, color="#fff"),
    )

    timeline_1.render("templates/COVID/"+'world_TC'+'.html')
    timeline_2.render("templates/COVID/"+'world_NC'+'.html')
    timeline_3.render("templates/COVID/" + 'world_TD' + '.html')
    timeline_4.render("templates/COVID/" + 'world_ND' + '.html')