import os, sys
from osgeo import gdal 
from osgeo import gdalconst as gconst 
import rasterio as rio
import numpy as np
from osgeo import gdal_array

####   GDAL Tools  ###

class importRasterGDAL():
    '''
    Some info about GDAL deo Transform
    adfGeoTransform[0] /* top left x */
    adfGeoTransform[1] /* w-e pixel resolution */
    adfGeoTransform[2] /* rotation, 0 if image is "north up" */
    adfGeoTransform[3] /* top left y */
    adfGeoTransform[4] /* rotation, 0 if image is "north up" */
    adfGeoTransform[5] /* n-s pixel resolution */
    
    '''
    def __init__(self, rasterPath) -> None:
        gdal.AllRegister() # register all of the drivers
        self.ds = gdal.Open(rasterPath)
        if self.ds is None:
            print('Could not open image')
            sys.exit(1)   
        # get image size
        self.rows = self.ds.RasterYSize
        self.cols = self.ds.RasterXSize
        self.NumOfBands = self.ds.RasterCount
        # get georeference info
        transform = self.ds.GetGeoTransform()
        self.xOrigin = transform[0]
        self.yOrigin = transform[3]
        self.pixelWidth = transform[1]
        self.pixelHeight = transform[5]
        self.projection = self.ds.GetProjection()
        self.MetaData = self.ds.GetMetadata()

    def setDirGDAL(self, path ):
        os.chdir()
    
    def getRasterDataset(self):
        return self.ds 
   
    def getRasterNpArray(self):
        return self.ds.ReadAsArray()
    
    def computePixelOffset(self,x,y):
        # compute pixel offset
        xOffset = int((x - self.xOrigin) / self.pixelWidth)
        yOffset = int((y - self.yOrigin) / self.pixelHeight)
        return xOffset, yOffset

    def closeRaster(self):
        self.ds = None

    def printRaster(self):
        print("---- Image size ----")
        print(f"Row : {self.rows}")
        print(f"Cols : {self.cols}")
        print(f"xOrigin : {self.xOrigin}")
        print(f"yOrigin : {self.yOrigin}") 
        print(f"NumOfBands : {self.NumOfBands}")
        print(f"pixelWidth : {self.pixelWidth}")
        print(f"pixelHeight : {self.pixelHeight}")
        print(f"projection : {self.projection}")
        print(f"MetaData : {self.MetaData}")
    

# Read raster data as numeric array from file
def readRasterAsArry(rasterPath):
   return gdal_array.LoadFile(rasterPath)



####   Rasterio Tools  #####
def readRaster(rasterPath:os.path):
    '''
    Read a raster qith Rasterio.
    return:
     Raster data as np.array
     Raster.profile: dictionary with all rater information
    '''
    inRaster = rio.open(rasterPath, mode="r")
    profile = inRaster.profile
    rasterData = inRaster.read()
    # print(f"raster data shape in ReadRaster : {rasterData.shape}")
    return rasterData, profile

def createRaster(savePath:os.path, data:np.array, profile, noData:int = None):
    '''
    parameter: 
    @savePath: Most contain the file name ex.: *name.tif.
    @data: np.array with shape (banself.ds,H,W)
    '''
    B,H,W = data.shape[-3],data.shape[-2],data.shape[-1] 
    # print(f"C : {B}, H : {H} , W : {W} ")
    profile.update(dtype = rio.uint16, nodata = noData, blockysize = profile['blockysize'])
    with rio.open(
        savePath,
        mode="w",
        #out_shape=(B, H ,W),
        **profile
        ) as new_dataset:
            # print(f"New Dataset.Profile: ->> {new_dataset.profile}")
            new_dataset.write(data)
            print("Created new raster>>>")
    return savePath