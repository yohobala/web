"""Convert an ASCII DEM to an image."""
import os
from osgeo import gdal_array as gd
import numpy as np

try:
    import Image
    import ImageOps
except:
    from PIL import Image, ImageOps

class dem2img():
    def dem2img(self, path, demFile, relieFfile, divide_class, hight, color):
        # Source LIDAR DEM file
        dem = path + demFile
        relief = path + relieFfile

        # Output image file
        target = os.path.dirname(os.getcwd()) + '/web/static/shaded_relief/images/' + demFile.split('.')[0] + '.jpg'

        imagePath = '/static/shaded_relief/images/'+demFile.split('.')[0]+'.jpg'

        # Load the relief as the background image
        bg = gd.numpy.loadtxt(relief, skiprows=6)

        # Load the DEM into a numpy array as the foreground image
        fg = gd.numpy.loadtxt(dem, skiprows=6)[:-2, :-2]

        # Create a blank 3-band image to colorize the DEM
        rgb = gd.numpy.zeros((3, len(fg), len(fg[0])), gd.numpy.uint8)

        # Class list with DEM upper elevation range values.
        classes = []
        hight = hight.split(',')
        for i in range(len(hight)):
            classes.append(int(hight[i]))


        # Color look-up table (lut)
        # The lut must match the number of classes.
        # Specified as R, G, B tuples
        lut = []
        color = color.split(',')
        for i in range(len(color)):
            color_rgb = []
            r = int(color[i][1:3], 16)
            g = int(color[i][3:5], 16)
            b = int(color[i][5:7], 16)
            color_rgb = [r, g, b]
            lut.append(color_rgb)


        start = 1

# 首先用logical_and对文件遍历，判断fg中每个量是否是在start和classes[i]之间，返回False 和True
# 然后用choose进行选择 ，rgb是一个都是0的列表,如果变量是False,选择rgb中相应位置的数也就是0,如果是True，选择lut
# 三次遍历后组成一个rbg的三维列表，生成每个点的颜色
        for i in range(len(classes)):
            mask = gd.numpy.logical_and(start <= fg,
                                        fg <= classes[i])
            for j in range(len(lut[i])):
                rgb[j] = gd.numpy.choose(mask, (rgb[j], lut[i][j]))
            start = classes[i] + 1

        im1 = Image.fromarray(bg).convert('RGB')

        # Convert the colorized DEM to a PIL image.
        # We must transpose it from the Numpy row, col order
        # to the PIL col, row order (width, height).
        im2 = Image.fromarray(rgb.transpose(1, 2, 0)).convert('RGB')

        # Blend the two images with a 40% alpha
        hillshade = Image.blend(im1, im2, .4)

        # Save the hillshade
        hillshade.save(target)

        return imagePath

