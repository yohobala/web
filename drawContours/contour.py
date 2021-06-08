"""
Use GDAL and OGR to create a contour shapefile
"""

# http://git.io/vYwUX

# import gdal
from osgeo import ogr

class contour():
    def contour(self,path,file,interval,height):
        # Elevation DEM
        source = path + file
        # Output shapefile
        target = path + file.split('.')[0]

        ogr_driver = ogr.GetDriverByName('ESRI Shapefile')
        ogr_ds = ogr_driver.CreateDataSource(target + ".shp")
        ogr_lyr = ogr_ds.CreateLayer(target, geom_type=ogr.wkbLineString25D)
        field_defn = ogr.FieldDefn('ID', ogr.OFTInteger)
        ogr_lyr.CreateField(field_defn)
        field_defn = ogr.FieldDefn('ELEV', ogr.OFTReal)
        ogr_lyr.CreateField(field_defn)

        # gdal.ContourGenerate() arguments
        # Band srcBand,
        # double contourInterval,
        # double contourBase,
        # double[] fixedLevelCount,
        # int useNoData,
        # double noDataValue,
        # Layer dstLayer,
        # int idField,
        # int elevField

        ds = gdal.Open(source)
        gdal.ContourGenerate(ds.GetRasterBand(1), interval, height, [], 0, 0, ogr_lyr, 0, 1)
        ogr_ds = None

