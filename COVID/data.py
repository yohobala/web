#这是往数据库中存入数据的文件
import os
import django

from COVID import Country_chart

import csv
import time
import  requests
import json


def getJson(url):
    Json = requests.get(url)
    data = json.loads(Json.text)
    return data


#转换时间戳为年月日格式
def transform_time(timeStamp):
    timeArray = time.localtime(timeStamp / 1000)
    date = time.strftime("%Y--%m--%d", timeArray)
    return date

#匹配国家缩写，获取国家中英文名字
def countryName(name,countryData):
    for line in countryData:
        if name in line[2]:
            ChineseName = line[0]
            EnglishName = line[1]
            break
    return ChineseName,EnglishName

def classifyByName(file,countryData):
    # 定义一个二维列表TotalList，以及子列表List，子列表存储每个国家的信息，二维列表存储所有子列表
    atateAbbreviations = ''
    for i in range(len(file)):
        if atateAbbreviations != file[i][1]:  # 判断是不是一个国家,如果名字不一样换一个
            atateAbbreviations = file[i][1]

        chineseCountry, englishCountry = countryName(file[i][1], countryData)  # 国家中文名和英文名
        # 分别是日期、中文国名，国家缩写，英文国名，地区，确诊人数，新增确诊，死亡人数，新增死亡
        c = Country(chinese_name = chineseCountry,
                    english_name = englishCountry,
                    atate_abbreviations = atateAbbreviations
                    )#
        c.save()
        c.data_set.create(time_stamp =  file[i][0],new_deaths =file[i][3],cumula_deaths=file[i][4],new_confirmed=file[i][5],cumula_confirmed=file[i][6])


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    django.setup()
    #打开有国家中文名和国家英文名的csv文件,并生成一个列表，如果直接用读取的csv.reader只能迭代一次
    country = open("/Users/huanghao/Desktop/Python/GIS/crawler/country.csv", 'r', encoding="utf-8")
    country_data = csv.reader(country)
    countryList = []
    for line in country_data:
        countryList.append(line)
    # 从url链接里获取json文件，并在rows里获得数据
    starttime = time.time()
    url = 'https://dashboards-dev.sprinklr.com/data/9043/global-covid19-who-gis.json'
    data = getJson(url)
    rows = data['rows']
    print(rows)
    classifyByName(rows, countryList)


