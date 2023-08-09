# PCRasterPython

Using GDAL to read, write, translate and get ingo from different goefiles format:
Some functions:
gdal.Open("/gdata/geotiff_file.tif")
rds.GetDescription() : Get the description of the raster
rds.RasterCount : Get the number of bands in the raster dataset
rds.RasterXSize : the width of the raster data (the number of pixels in the X direction)
rds.RasterYSize : height of raster data (number of pixels in the Y direction)
rds.GetGeoTransform() : The six parameters of the raster data.
GetProjection() : projection of raster data