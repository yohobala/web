import shutil

from django.shortcuts import render
from django.http import HttpResponse
import os
import zipfile
import shapefile
from PIL import Image, ImageDraw
#解压文件
import rarfile

from .dot_density import dot_density

def index(request):
    global path
    if request.method == 'POST':
        flow = int(request.POST.get('flow'))
        if flow == 1:
            f = request.FILES.get('file_obj')
            filename = f.name.split('.')[0]
            path1 = os.path.join(os.path.dirname(os.getcwd()) + "/webGIS/data/dot_density/")
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
            existFile = 0 ;
            for file in l:
                if file[-3:] == 'shp':
                    inShp = shapefile.Reader(path + file.split('.')[0])
                    filelist = inShp.fields
                    data = ''
                    for i in filelist:
                        message = str(i[0])
                        data = data + message + '|'
                    existFile = 1 ;
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
            color = request.POST.get('color')
            l = os.listdir(path)
            for i in l:
                if i.split('.')[1] == 'shp':
                    dot = dot_density()
                    imgPath = dot.drawing(path, i, width, height, first_field,color)

            fp = os.path.join(os.path.dirname(os.getcwd()) + "/webGIS/data/dot_density/")
            filename = f.name.split('.')[0]

            shutil.rmtree(fp+filename)
            os.remove(fp+filename+'.zip')
            # with open(os.path.join(img_path), 'wb+') as f:  # 图片上传
            #     for item in fafafa.chunks():
            #         f.write(item)
            return HttpResponse(imgPath)

    return render(request, 'dot_density/dot_density.html')

# Create your views here.
