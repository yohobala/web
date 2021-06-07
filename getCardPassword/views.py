import csv
import datetime
import shutil
import os,base64
import sys
import time
import pandas
from django.shortcuts import render
import pytesseract
from django.http import HttpResponse
import pandas as pd




import re
#解压文件
import rarfile

from PIL import Image
import pytesseract



def index(request):

    print(request.method)
    if request.method == 'POST':
        text = request.POST.get('cardText')
        text = text.replace('data:image/png;base64,',"")
        imgdata = base64.b64decode(text)

        now_time = int(time.time())
        fileName = "static\\getCardPassword\\images\\" +str(now_time) + '.jpg'
        print(fileName)
        file = open(fileName,'wb')
        file.write(imgdata)
        file.close()
        img_src = Image.open(fileName)
        text = pytesseract.image_to_string(img_src, lang='chi_sim', config='--psm 6 --oem 1')

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
        print(cardPassword)
        if (number == "10.00"):
            list_10.append(cardPassword)
            list_20.append("")
            list_30.append("")
            list_other.append("")
        elif number == "20.00":
            list_10.append("")
            list_20.append(cardPassword)
            list_30.append("")
            list_other.append("")
        elif number == "30.00":
            list_10.append("")
            list_20.append("")
            list_30.append(cardPassword)
            list_other.append("")
        else:
            list_10.append("")
            list_20.append("")
            list_30.append("")
            list_other.append(number + ":" + cardPassword)

        data = pandas.DataFrame({
            '10': list_10,
            '20': list_20,
            '30': list_30,
            'other': list_other
        })

        data.to_csv('卡密.csv')

        return HttpResponse("金额："+number+"  "+cardPassword)
    return render(request, 'getCardPassword/getCardPassword.html')




