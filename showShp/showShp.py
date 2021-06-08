import math
import os
import shapefile
from PIL import Image, ImageDraw


class showShp():
    def showShp(self,path,file,iwidth,iheight,color):
        shp = shapefile.Reader(path + file)
        # 初始化 Image
        img = Image.new("RGB", (iwidth, iheight), (255, 255, 255))
        # 填充多边形
        draw = ImageDraw.Draw(img)
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        R = int(r)
        G = int(g)
        B = int(b)
        # 绘制多边形
        for sr in shp.shapeRecords():
            pixels = []
            for x, y in sr.shape.points:
                """转换地理空间坐标系到屏幕坐标"""
                minx, miny, maxx, maxy = shp.bbox
                xdist = maxx - minx
                ydist = maxy - miny
                xratio = iwidth / xdist
                yratio = iheight / ydist
                px = int(iwidth - ((maxx - x) * xratio))
                py = int((maxy - y) * yratio)
                pixels.append((px, py))
            draw.polygon(pixels, outline=(255, 255, 255), fill=(R, G, B))

        img_path = os.path.dirname(os.getcwd()) + '/webGIS/static/showShp/' + file.split('.')[0] + '.jpg'
        img.save(img_path)
        image = '/static/showShp/' + file.split('.')[0] + '.jpg'

        return image
