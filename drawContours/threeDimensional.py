import os

import shapefile

import json


import time


class threeDimensional():
    def threeDimensional(self,path,file):
        r = shapefile.Reader(path + file.split('.')[0])
        # 设置参数

        ilong = 1000
        iwidth = 1000
        iheight = 1000

        zlist = []
        for i in range(len(r.records())):
            zlist.append(r.records()[i][1])
        zlist.sort()
        xdist = r.bbox[2] - r.bbox[0]
        ydist = r.bbox[3] - r.bbox[1]
        zdist = zlist[-1] - zlist[0]
        xratio = ilong / xdist
        yratio = iwidth / ydist
        zratio = iheight / zdist
        contours = []
        n = 0
        for shape in r.shapes():
            # 读取高程
            high = r.records()[n][1]
            for i in range(len(shape.parts)):
                pixels = []
                pt = None
                if i < len(shape.parts) - 1:
                    pt = shape.points[shape.parts[i]:shape.parts[i + 1]]
                else:
                    pt = shape.points[shape.parts[i]:]
                for x, y in pt:
                    px = int(ilong - ((r.bbox[2] - x) * xratio))
                    py = int(iwidth - ((r.bbox[3] - y) * yratio))
                    pz = int(iheight - ((zlist[-1] - high) * zratio))
                    # px = int(x/10 )
                    # py = int(y/10 )
                    # pz = int(high)
                    contours.append([px, py, int(pz)])
            n = n + 1
        list = sorted(contours, key=lambda x: (x[1], x[0], x[2]))

        # 删除重复的点
        sorted_data = []
        num = [-10000, -10000, -10000]
        for i in range(len(list)):
            if num == list[i]:
                continue
            else:
                if num[0] == list[i][0]:
                    if num[-1] <= list[i][-1]:
                        sorted_data.pop()

                num = list[i]
                sorted_data.append(list[i])

        # 把点先按y大小排序，再按x大小排序
        sorted_data = sorted(sorted_data, key=lambda x: (x[1], x[0]))

        JF = [['x', 'y', 'z']]

        for i in range(len(sorted_data)):
            x = sorted_data[i][0]
            y = sorted_data[i][1]
            z = sorted_data[i][2]
            JF.append([x, y, z])

        # File = os.path.join(os.path.join(os.path.dirname(os.getcwd()) + "/webGIS/static/drawContours/")+file.split('.')[0]+'data.json')
        # with open(File, 'w') as f:
        #     json.dump(JF, f, ensure_ascii=False)  # 最后一个参数为了避免乱码
        #
        #
        # path = '/static/drawContours/'+file.split('.')[0]+'data.json'
        return JF


