"""Create a dot-density thematic map"""

# https://github.com/GeospatialPython/Learn/raw/master/GIS_CensusTract.zip
import os
import random
import pngcanvas
import shapefile

class dot_density():
    def point_in_poly(self,x, y, poly):
        """Boolean: is a point inside a polygon?"""
        # check if point is a vertex
        if (x, y) in poly:
            return True
        # check if point is on a boundary
        for i in range(len(poly)):
            p1 = None
            p2 = None
            if i == 0:
                p1 = poly[0]
                p2 = poly[1]
            else:
                p1 = poly[i - 1]
                p2 = poly[i]
            if p1[1] == p2[1] and p1[1] == y and \
                    x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
                return True
        n = len(poly)
        inside = False

        p1x, p1y = poly[0]
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x, p1y = p2x, p2y

        if inside:
            return True
        else:
            return False

    def world2screen(self,bbox, w, h, x, y):
        """convert geospatial coordinates to pixels"""
        minx, miny, maxx, maxy = bbox
        xdist = maxx - minx
        ydist = maxy - miny
        xratio = w / xdist
        yratio = h / ydist
        px = int(w - ((maxx - x) * xratio))
        py = int((maxy - y) * yratio)
        return (px, py)

    def drawing(self, path, file, iwidth, iheight, first_field,tone):
        # Open the census shapefile
        inShp = shapefile.Reader(path + file.split('.')[0])



        # Get the index of the population field
        first_index = None
        dots = []

        for i, f in enumerate(inShp.fields):
            if f[0] == first_field:
                # Account for deletion flag
                first_index = i - 1


        for sr in inShp.shapeRecords():
            first = sr.record[first_index]
            density = first / 100
            found = 0
            while found < density:
                minx, miny, maxx, maxy = sr.shape.bbox
                x = random.uniform(minx, maxx)
                y = random.uniform(miny, maxy)
                if self.point_in_poly(x, y, sr.shape.points):
                    dots.append((x, y))
                    found += 1

        # Set up the PNG output image
        c = pngcanvas.PNGCanvas(iwidth, iheight)
        r = int(tone[1:3], 16)
        b = int(tone[3:5], 16)
        g = int(tone[5:7], 16)
        # Draw the red dots
        c.color = (r, b, g, 0xff)
        for d in dots:
            x, y = self.world2screen(inShp.bbox, iwidth, iheight, *d)
            c.filled_rectangle(x - 1, y - 1, x + 1, y + 1)

        # Draw the census tracts
        c.color = (0, 0, 0, 0xff)
        for s in inShp.iterShapes():
            pixels = []
            for p in s.points:
                pixel = self.world2screen(inShp.bbox, iwidth, iheight, *p)
                pixels.append(pixel)
            c.polyline(pixels)

        # Save the image
        img_path = os.path.dirname(os.getcwd()) + '/webGIS/static/dot_density/images/' + file.split('.')[0] + '.jpg'
        img = open(img_path, "wb")
        img.write(c.dump())
        img.close()
        image = '/static/dot_density/images/'+file.split('.')[0]+'.jpg'

        return  image





