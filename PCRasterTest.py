
from pcraster import *
import pcraster as pcr
import util as U

def computeHAND(DEMPath,HANDPath,saveStrahOrder:bool=True,saveSubCath:bool = True): 
    DEMMap = U.saveTiffAsPCRaster(DEMPath)
    pcr.setclone(DEMMap)
    DEM = pcr.readmap(DEMMap)
    ## Flow Direcction (Use to take long...)
    threshold = 8
    # FlowDir = lddcreate(DEM,1e31,1e31,1e31,1e31)
    ### Testing replace D8 Flow direction with Dinf from WbTools
    FDirPath = U.replaceExtention(DEMPath,'_Dinf.tif')
    wbt_DTMTransformer = U.dtmTransformer()
    print("Computing DInf flow dir....")
    wbt_DTMTransformer.DInfPointer(DEMPath,FDirPath)
    FlowDir = U.saveTiffAsPCRaster(FDirPath)
    ## Strahler order 
    print('Strahler order...')
    strahlerOrder = streamorder(FlowDir)
    strahlerRiver = ifthen(strahlerOrder>=threshold,strahlerOrder)
    if saveStrahOrder:
        pcr.report(strahlerRiver, 'data\strahlerRiver.map')
    ## Finding outlets
    print('Finding outlets...')
    junctions = ifthen(downstream(FlowDir,strahlerOrder) != strahlerRiver, boolean(1))
    outlets = ordinal(cover(uniqueid(junctions),0))
    print('Calculating subcatchment')
    subCatchments = catchment(FlowDir,outlets)
    if saveSubCath:
        pcr.report(subCatchments,'data\subCathments.map')
    print('Ready to print')
    aguila(subCatchments)
    print('Computing HAND')
    areaMin = areaminimum(DEM,subCatchments)
    aguila(areaMin)
    pcr.report(areaMin,'data\z_drainage.map')
    HAND = DEM - areaMin
    aguila(HAND)
    pcr.report(HAND,HANDPath)
