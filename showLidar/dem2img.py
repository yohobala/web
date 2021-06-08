"""Convert an ASCII DEM to an image."""
import os

import numpy as np

try:
    import Image
    import ImageOps
except:
    from PIL import Image, ImageOps

import colorsys
class dem2img():
    def dem2img(self,path,file):
        # Source LIDAR DEM file
        source = path + file

        # Load the ASCII DEM into a numpy array
        arr = np.loadtxt(source, skiprows=6)

        # Convert the numpy array to a PIL image
        im = Image.fromarray(arr).convert('L')

        # Enhance the image
        im = ImageOps.equalize(im)
        im = ImageOps.autocontrast(im)

        # Begin building our color ramp
        palette = []

        # Hue, Saturaction, Value
        # color space
        h = .67
        s = 1
        v = 1

        step = h / 256.0


        for i in range(256):
            rp, gp, bp = colorsys.hsv_to_rgb(h, s, v)
            r = int(rp * 255)
            g = int(gp * 255)
            b = int(bp * 255)
            palette.extend([r, g, b])
            h -= step

        # Apply the palette to the image
        im.putpalette(palette)

        im = im.convert('RGB')

        # Output image file
        img_path = os.path.dirname(os.getcwd()) + '/webGIS/static/showLidar/images/' + file.split('.')[0] + '.jpg'
        # Save the image
        im.save(img_path)

        image = '/static/showLidar/images/' + file.split('.')[0] + '.jpg'

        return  image
