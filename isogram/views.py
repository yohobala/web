import shutil

from django.shortcuts import render
from django.http import HttpResponse
import os
import zipfile
import shapefile
from PIL import Image, ImageDraw
#解压文件
import rarfile

from .make import make

def index(request):
    global path
    print(request.method)
    if request.method == 'POST':
        flow = int(request.POST.get('flow'))
        if flow == 1:
            f = request.FILES.get('file_obj')
            filename = f.name.split('.')[0]
            path1 = os.path.join(os.path.dirname(os.getcwd()) + "/webGIS/data/isogram/")
            filePath = path1 + filename + '.zip'
            with open(os.path.join(filePath), 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

            zip_file = zipfile.ZipFile(filePath)
            zip_list = zip_file.namelist()  # 得到压缩包里所有文件

            path = path1 + filename + '/'

            for file in zip_list:
                zip_file.extract(file, path)  # 循环解压文件到指定目录

            l = os.listdir(path)
            existFile = 0
            for file in l:
                if file[-3:] == 'shp':
                    inShp = shapefile.Reader(path + file.split('.')[0])
                    filelist = inShp.fields
                    data = ''
                    for i in filelist:
                        message = str(i[0])
                        data = data + message + '|'
                    existFile = 1
            if existFile !=1 :
                path = path + filename + '/'
                l = os.listdir(path )
                for file in l:
                   if file.split('.')[1] == 'shp':
                       inShp = shapefile.Reader(path +  file.split('.')[0])
                       filelist = inShp.fields
                       data = ''
                       for i in filelist:
                          message = str(i[0])
                          data = data + message + '|'
            return HttpResponse(data)
        elif flow == 2:
            f = request.FILES.get('file_obj')
            width = int(request.POST.get('width'))
            height = int(request.POST.get('height'))
            first_field = request.POST.get('first_field')
            second_field = request.POST.get('second_field')
            rule = request.POST.get('rule')
            color1 = request.POST.get('color1')
            color2 = request.POST.get('color2')
            divide_class = int(request.POST.get('divide_class'))
            l = os.listdir(path)
            for i in l:
                if i.split('.')[1] == 'shp':
                    isogram = make()
                    imgPath = isogram.drawing(path, i, width, height, first_field, second_field,rule,color1,color2,divide_class)
            # with open(os.path.join(img_path), 'wb+') as f:  # 图片上传
            #     for item in fafafa.chunks():
            #         f.write(item)

            fp = os.path.join(os.path.dirname(os.getcwd()) + "/webGIS/data/isogram/")
            filename = f.name.split('.')[0]

            shutil.rmtree(fp+filename)
            os.remove(fp+filename+'.zip')
            return HttpResponse(imgPath)

    return render(request, 'isogram/isogram.html')





def Result(request):
    if request.method == 'POST':
        f = request.FILES['file']
        width = int(request.POST.get('width'))
        height = int(request.POST.get('height'))
        first_field = request.POST.get('first_field')
        second_field = request.POST.get('second_field')
        path1 = os.path.join(os.path.dirname(os.getcwd())+"/webGIS/data/isogram",f.name)
        path2 = os.path.dirname(os.getcwd())+"/webGIS/data/isogram"
        with open(os.path.join(path1), 'wb+') as destination:
                  for chunk in f.chunks():
                       destination.write(chunk)

        zip_file = zipfile.ZipFile(path1)
        zip_list = zip_file.namelist()  # 得到压缩包里所有文件

        for f in zip_list:
            zip_file.extract(f, path2)  # 循环解压文件到指定目录
        path = path1.split('.')[0] + '/'
        l = os.listdir(path)

        for i in l:
            if i.split('.')[1] == 'shp':
                isogram = make()
                imgPath = isogram.drawing(path,i,width,height,first_field,second_field,color)
    return render(request, 'isogram/Result.html',{'image':imgPath})
