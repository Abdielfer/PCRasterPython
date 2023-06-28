from osgeo import gdal



####   GDAL Tools  #####
def imprtRaster(rasterPath):
    rast = gdal.Open(rasterPath)
    return rast
