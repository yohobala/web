import os
from linecache import getline
import numpy as np

from .dem2img import dem2img

class shaded_relief():
    def drawing(self, path, file, azimuth, altitude, z, scale,divide_class, hight, color):
        # ASCII数字高程模型文件
        source = path + file

        # 高程阴影参数
        # NODATA值
        NODATA = -9999

        # 转换
        deg2rad = 3.141592653589793 / 180.0
        rad2deg = 180.0 / 3.141592653589793

        # 解析文件头部信息
        hdr = [getline(source, i) for i in range(1, 7)]
        values = [float(h.split(" ")[-1].strip()) for h in hdr]
        cols, rows, lx, ly, cell, nd = values
        xres = cell
        yres = cell * -1

        # 将DEM载入numpy数组中
        arr = np.loadtxt(source, skiprows=6)

        # 建立3*3的窗口进行坡度计算
        window = []
        for row in range(3):
            for col in range(3):
                window.append(arr[row:(row + arr.shape[0] - 2),
                              col:(col + arr.shape[1] - 2)])

        x = ((z * window[0] + z * window[3] + z * window[3] + z * window[6]) -
             (z * window[2] + z * window[5] + z * window[5] + z * window[8])) / \
            (8.0 * xres * scale)

        y = ((z * window[6] + z * window[7] + z * window[7] + z * window[8]) -
             (z * window[0] + z * window[1] + z * window[1] + z * window[2])) / \
            (8.0 * yres * scale)

        # 计算坡度
        slope = 90.0 - np.arctan(np.sqrt(x * x + y * y)) * rad2deg

        # 计算坡向
        aspect = np.arctan2(x, y)

        # 计算晕染阴影
        shaded = np.sin(altitude * deg2rad) * np.sin(slope * deg2rad) + \
                 np.cos(altitude * deg2rad) * np.cos(slope * deg2rad) * \
                 np.cos((azimuth - 90.0) * deg2rad - aspect)
        shaded = shaded * 255

        # 生成新的头部信息
        header = "ncols        {}\n".format(shaded.shape[1])
        header += "nrows        {}\n".format(shaded.shape[0])
        header += "xllcorner    {}\n".format(lx + (cell * (cols - shaded.shape[1])))
        header += "yllcorner    {}\n".format(ly + (cell * (rows - shaded.shape[0])))
        header += "cellsize     {}\n".format(cell)
        header += "NODATA_value      {}\n".format(NODATA)

        for pane in window:
            slope[pane == nd] = NODATA
            aspect[pane == nd] = NODATA
            shaded[pane == nd] = NODATA

        # # 坡度文件
        # slopegrid = path + file.split('.')[0] + '_slope' + '.asc'
        #
        # # 保存坡度
        # with open(slopegrid, "wb") as f:
        #     f.write(bytes(header, 'UTF-8'))
        #     np.savetxt(f, slope, fmt="%4i")
        #
        # # 坡向文件
        # aspectgrid = path + file.split('.')[0] + '_aspect' + '.asc'
        #
        # # 保存坡向
        # with open(aspectgrid, "wb") as f:
        #     f.write(bytes(header, 'UTF-8'))
        #     np.savetxt(f, aspect, fmt="%4i")

        # 输出晕染文件

        shadegrid = path + 'relief_' + file.split('.')[0] + '.asc'

        # 保存晕染
        with open(shadegrid, "wb") as f:
            f.write(bytes(header, 'UTF-8'))
            np.savetxt(f, shaded, fmt="%4i")

        reliefFile= 'relief_' + file.split('.')[0] + '.asc'

        imagePath = dem2img().dem2img(path,file,reliefFile,divide_class, hight, color)



        return imagePath