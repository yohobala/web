"""

Converts a LIDAR LAS file to an
ASCII DEM.  Interpolation is used
to account for data loss.
"""

# http://git.io/vOERW

# laspy for Python 3: pip install http://git.io/vOER9
import os

#  laspy 安装pip install http://git.io/vOER9
from laspy.file import File
import numpy as np

from .dem2img import dem2img

class showLidar():
    def showLidar(self,path,file,cell):
        # Source LAS file
        source = path+file


        # No data value for output DEM
        NODATA = 0

        # Open LIDAR LAS file
        las = File(source, mode="r")


        min = las.header.min
        max = las.header.max
        xdist = max[0] - min[0]
        ydist = max[1] - min[1]
        cols = int(xdist / cell)
        rows = int(ydist / cell)
        cols += 1
        rows += 1
        count = np.zeros((rows, cols)).astype(np.float32)
        zsum = np.zeros((rows, cols)).astype(np.float32)
        ycell = -1 * cell
        projx = (las.x - min[0]) / cell
        projy = (las.y - min[1]) / ycell
        ix = projx.astype(np.int32)
        iy = projy.astype(np.int32)
        for x, y, z in np.nditer([ix, iy, las.z]):
            count[y, x] += 1
            zsum[y, x] += z

        # Change 0 values to 1 to avoid numpy warnings,
        # and NaN values in array
        nonzero = np.where(count > 0, count, 1)
        # Average our z values
        zavg = zsum / nonzero

        # Interpolate 0 values in array to avoid any
        # holes in the grid
        mean = np.ones((rows, cols)) * np.mean(zavg)
        left = np.roll(zavg, -1, 1)
        lavg = np.where(left > 0, left, mean)
        right = np.roll(zavg, 1, 1)
        ravg = np.where(right > 0, right, mean)
        interpolate = (lavg + ravg) / 2
        fill = np.where(zavg > 0, zavg, interpolate)

        # Create our ASCII DEM header
        header = "ncols        {}\n".format(fill.shape[1])
        header += "nrows        {}\n".format(fill.shape[0])
        header += "xllcorner    {}\n".format(min[0])
        header += "yllcorner    {}\n".format(min[1])
        header += "cellsize     {}\n".format(cell)
        header += "NODATA_value      {}\n".format(NODATA)

        # Output ASCII DEM file
        target = path + file.split('.')[0] + '.asc'
        # Open the output file, add the header, save the array
        with open(target, "wb") as f:
            f.write(bytes(header, 'UTF-8'))
            # The fmt string ensures we output floats
            # that have at least one number but only
            # two decimal places
            np.savetxt(f, fill, fmt="%1.2f")

        img_path = dem2img().dem2img(path,file.split('.')[0] + '.asc')

        return img_path
