import math
import os

import shapefile


from PIL import Image, ImageDraw

class make():
  def world2screen(self,bbox, w, h, x, y):
    """转换地理空间坐标系到屏幕坐标"""
    minx, miny, maxx, maxy = bbox
    xdist = maxx - minx
    ydist = maxy - miny
    xratio = w/xdist
    yratio = h/ydist
    px = int(w - ((maxx - x) * xratio))
    py = int((maxy - y) * yratio)
    return (px, py)

  def drawing(self,path,file,iwidth,iheight,first_field,second_field,rule,tone1,tone2,divide_class):
    # 打开shapefile
    inShp = shapefile.Reader(path + file.split('.')[0])
    # print(inShp.fields)
    # for sr in inShp.shapeRecords():
    #     print(sr.record)
    # 初始化 Image
    img = Image.new("RGB", (iwidth, iheight), (255, 255, 255))
    # 填充多边形
    draw = ImageDraw.Draw(img)

    # 获取人口和区域索引
    first_index = None
    second_index = None

    # 绘制阴影
    for i, f in enumerate(inShp.fields):
        if f[0] == first_field:
            # Account for deletion flag
            first_index = i - 1
        elif f[0] == second_field:
            second_index = i - 1
    minimum =  float('inf') #表示正无穷大， 负无穷大是float('-inf') 或者-float('inf')
    maximum =  -float('inf')
    num = 0
    #得到最小值和最大值
    for sr in inShp.shapeRecords():
        if second_field == '无':
            num = sr.record[first_index]
        else:
            if rule == 'addition':
                num = sr.record[first_index] + sr.record[second_index]
            elif rule == 'minus':
                num = sr.record[first_index] - sr.record[second_index]
            elif rule == 'multiplication':
                num = sr.record[first_index] - sr.record[second_index]
            elif rule == 'division':
                num = sr.record[first_index] / sr.record[second_index]
        if num < minimum:
            minimum = num
        if num > maximum:
            maximum = num
    #划分等级
    weight = maximum/minimum/divide_class
    # 绘制多边形
    for sr in inShp.shapeRecords():
        if second_field == '无':
            num = sr.record[first_index]
        else:
            if rule == 'addition':
                num = sr.record[first_index] + sr.record[second_index]
            elif rule == 'minus':
                num = sr.record[first_index] - sr.record[second_index]
            elif rule == 'multiplication':
                num = sr.record[first_index] - sr.record[second_index]
            elif rule == 'division':
                num = sr.record[first_index] / sr.record[second_index]
        level = math.ceil(num/minimum/weight)
        r1 = int(tone1[1:3], 16)
        g1 = int(tone1[3:5], 16)
        b1 = int(tone1[5:7], 16)
        r2 = int(tone2[1:3], 16)
        g2 = int(tone2[3:5], 16)
        b2 = int(tone2[5:7], 16)
        R = int(r1 + (r2-r1)*level/divide_class)
        G = int(g1 + (g2-g1)*level/divide_class)
        B = int(b1 + (b2-b1)*level/divide_class)

        pixels = []
        for x, y in sr.shape.points:
            """转换地理空间坐标系到屏幕坐标"""
            minx, miny, maxx, maxy = inShp.bbox
            xdist = maxx - minx
            ydist = maxy - miny
            xratio = iwidth / xdist
            yratio = iheight / ydist
            px = int(iwidth - ((maxx - x) * xratio))
            py = int((maxy - y) * yratio)
            pixels.append((px, py))
        draw.polygon(pixels, outline=(255, 255, 255), fill=(R, G, B))
    print(minimum)
    #img_path = path+file.split('.')[0]+'.jpg'

    img_path = os.path.dirname(os.getcwd())+'/webGIS/static/isogram/images/'+file.split('.')[0]+'.jpg'
    img.save(img_path)
    image = '/static/isogram/images/'+file.split('.')[0]+'.jpg'

    return image

