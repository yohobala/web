"""
Draw an entire contour shapefile
to a pngcanvas image.
"""

# http://git.io/vYwTN
import os

import shapefile
import pngcanvas
from PIL import Image



class drawContours():
    def drawContours(self,path,file,iwidth,iheight,tone):
        # Open the contours
        r = shapefile.Reader(path + file.split('.')[0])
        # Setup the world to pixels conversion
        xdist = r.bbox[2] - r.bbox[0]
        ydist = r.bbox[3] - r.bbox[1]
        xratio = iwidth / xdist
        yratio = iheight / ydist
        contours = []
        for shape in r.shapes():
            for i in range(len(shape.parts)):
                pixels = []
                pt = None
                if i < len(shape.parts) - 1:
                    pt = shape.points[shape.parts[i]:shape.parts[i + 1]]
                else:
                    pt = shape.points[shape.parts[i]:]
                for x, y in pt:
                    px = int(iwidth - ((r.bbox[2] - x) * xratio))
                    py = int((r.bbox[3] - y) * yratio)
                    pixels.append([px, py])
                contours.append(pixels)

        canvas = pngcanvas.PNGCanvas(iwidth, iheight)
        # PNGCanvas accepts rgba byte arrays for colors
        r = int(tone[1:3], 16)
        g = int(tone[3:5], 16)
        b = int(tone[5:7], 16)
        red = [r, g, b, 255]
        canvas.color = red
        # Loop through the polygons and draw them
        for c in contours:
            canvas.polyline(c)
        # Save the image
        img_path = os.path.dirname(os.getcwd()) + '/webGIS/static/drawContours/images/' + file.split('.')[0]
        filePath =  img_path+'.png'
        f = open(filePath, "wb")
        f.write(canvas.dump())
        f.close()
        with Image.open(filePath) as im:
            im.convert('RGB').save(filePath[:-3] + 'jpg')

        image = '/static/drawContours/images/' + file.split('.')[0] + '.jpg'

        return image

