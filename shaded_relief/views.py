import shutil

from django.shortcuts import render
from django.http import HttpResponse
import os
import zipfile
from osgeo import gdal_array as gd
#解压文件
import rarfile

from .shaded_relief import shaded_relief


def index(request):
    global path
    global name
    if request.method == 'POST':
        flow = int(request.POST.get('flow'))
        if flow == 1:
            f = request.FILES.get('file_obj')
            path = os.path.join(os.path.dirname(os.getcwd()) + "/web/data/shaded_relief/")

            with open(os.path.join(path+f.name), "wb") as file:
                for chunk in f.chunks():
                    file.write(chunk)

            filename = f.name.split('.')[0]
            filePath = path + filename + '.zip'

            zip_file = zipfile.ZipFile(filePath)
            zip_list = zip_file.namelist()  # 得到压缩包里所有文件

            path = path + filename + '/'

            for file in zip_list:
                zip_file.extract(file, path)  # 循环解压文件到指定目录

            l = os.listdir(path)
            print(l)
            minimum = 0  # 表示正无穷大， 负无穷大是float('-inf') 或者-float('inf')
            maximum = -float('inf')


            existFile = 0
            for file in l:
                if file[-3:] == 'asc':
                    name = file
                    dem = path + file
                    fg = gd.numpy.loadtxt(dem, skiprows=6)[:-2, :-2]
                    for x in range(len(fg)):
                        for y in range(len(fg[x])):
                            if fg[x][y] < minimum:
                                minimum = fg[x][y]
                                print(fg[x][y])
                                print(x)
                                print(y)
                            if fg[x][y] > maximum:
                                maximum = fg[x][y]
                    existFile = 1
            if existFile != 1:
                path = path + filename + '/'
                l = os.listdir(path)
                for file in l:
                    if file[-3:] == 'asc':
                        name = file
                        dem = path + file
                        fg = gd.numpy.loadtxt(dem, skiprows=6)[:-2, :-2]
                        for x in range(len(fg)):
                            for y in range(len(fg[x])):
                                if fg[x][y] < minimum:
                                    minimum = fg[x][y]
                                if fg[x][y] > maximum:
                                    maximum = fg[x][y]

            data = str(maximum) + '|' + str(minimum)
            return HttpResponse(data)
        elif flow == 2:
            f = request.FILES.get('file_obj')
            azimuth = int(request.POST.get('azimuth'))
            altitude = int(request.POST.get('altitude'))
            z = int(request.POST.get('z'))
            scale = int(request.POST.get('scale'))
            divide_class = int(request.POST.get('divide_class'))
            hight = request.POST.get('hight')
            color = request.POST.get('color')
            print(hight)
            print(color)


            shaded = shaded_relief()
            print(name)
            imgPath = shaded.drawing(path, name, azimuth, altitude, z, scale, divide_class, hight, color)

            fp = os.path.join(os.path.dirname(os.getcwd()) + "/web/data/shaded_relief/")
            filename = f.name.split('.')[0]

            shutil.rmtree(fp+filename)
            os.remove(fp+filename+'.zip')

            # with open(os.path.join(img_path), 'wb+') as f:  # 图片上传
            #     for item in fafafa.chunks():
            #         f.write(item)
            return HttpResponse(imgPath)

    return render(request, 'shaded_relief/shaded_relief.html')

# Create your views here.
