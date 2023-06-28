
import PCRasterTest as PCR 
import util as U 


# inmport raster.tif
# OPTIONAL: clip raster by polygon
# extract data from raster as np and keep raster metadata(cellsize, crs, bbox, etc.)
# convert num2PCRaster to procede with computations.
# revert PCRaster2num to build raster (*.tif) file format with the saved metadate
# save raster output( *.tif)




def main():
    DEM =  r'C:\Users\abfernan\CrossCanFloodMapping\PCRasterPython\data\BCQuesnellWsh2GeoFill.tif'
    gdalReader = U.importRasterGDAL(DEM)
    gdalReader.printRaster()
    
if __name__ == "__main__":
    main()  