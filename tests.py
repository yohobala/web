import csv
import re

import pandas
from PIL import Image
import pytesseract
from django.test import TestCase
import datetime
# Create your tests here.

now_time = datetime.datetime.now()
print(now_time)
fileName = "static\\getCardPassword\\images\\1.jpg"
print(fileName)
img_src = Image.open(fileName)
text = pytesseract.image_to_string(img_src, lang='chi_sim', config='--psm 6 --oem 1')
print(text)
card_csv = open("卡密.csv", 'r', encoding='utf-8')
card_data = csv.reader(card_csv)
list_10 = []
list_20 = []
list_30 = []
list_other = []
print(card_data)
next(card_data)
for line in card_data:
    print(line)
    list_10.append(line[1])
    list_20.append(line[2])
    list_30.append(line[3])
    list_other.append(line[4])
    # line = line[0].split("\t")
    # print(line)

# 判断多少元
number = re.split("[元换]", text)[1].strip()
# 获得卡密
cardPassword = re.split("[:。]", text)[2].strip().replace("\n", '')
# print(cardPassword)
# if(number == "10.00"):
#     list_10.append(cardPassword)
#     list_20.append("")
#     list_30.append("")
#     list_other.append("")
# elif number == "20.00":
#     list_10.append("")
#     list_20.append(cardPassword)
#     list_30.append("")
#     list_other.append("")
# elif number == "30.00":
#     list_10.append("")
#     list_20.append("")
#     list_30.append(cardPassword)
#     list_other.append("")
# else:
#     list_10.append("")
#     list_20.append("")
#     list_30.append("")
#     list_other.append(number+ ":" + cardPassword)
#
# data = pandas.DataFrame({
#     '10': list_10,
#     '20': list_20,
#     '30': list_30,
#     'other': list_other
# })
#
#
#
# data.to_csv('卡密.csv')
