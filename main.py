import PCRasterTest as PCRT
import util as U

# inmport raster.tif
# OPTIONAL: clip raster by polygon
# extract data from raster as np and keep raster metadata(cellsize, crs, bbox, etc.)
# convert num2PCRaster to procede with computations.
# revert PCRaster2num to build raster (*.tif) file format with the saved metadate
# save raster output( *.tif)


def main():
    DEM =  r'C:\Users\abfernan\CrossCanFloodMapping\PCRasterPython\data\BCQuesnellWsh2GeoFill.tif'
    HANDPath =  r'C:\Users\abfernan\CrossCanFloodMapping\PCRasterPython\data\BCQuesnellWsh2HAND.map'
    
    PCRT.computeHAND(DEM,HANDPath)
    # gdalReader = U.importRasterGDAL(DEM)
    # nodata = gdalReader.NoData
    # print(nodata)
    # 
    #  gdalReader.printRaster()
    # arr = gdalReader.getRasterNpArray().astype('int64')
    # print(type(arr))

    # arrPCR = PCR.numpy2pcr(dataType='Nominal',array = arr,mv = nodata)

    # rasterData,_ = U.readRaster(DEM)
    # pcr.setclone('data\BC_Quesnel_PCr_WShed2_Fill.map')
    # arrPCR = pcr.numpy2pcr(pcr.clone(),array = rasterData,mv = -3.40282347e+38)

if __name__ == "__main__":
    main()  