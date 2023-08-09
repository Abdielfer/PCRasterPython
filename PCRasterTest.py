
from pcraster import *
import pcraster as pcr
import util as U

def computeHAND(DEMPath,HANDPath,saveDDL:bool=True,saveStrahOrder:bool=True,saveSubCath:bool = False): 
    '''
    1- DEMPath is converted to PCRaster *.map expention.
    2- pcr.setClone(DEMPath)
    
    '''

    DEMMap = U.saveTiffAsPCRaster(DEMPath)
    pcr.setclone(DEMPath)
    print(DEMMap)
    DEM = pcr.readmap(DEMMap)
    ## Flow Direcction (Use to take long...)
    print("#####......Computing DInf flow dir.......######")
    threshold = 8
    FlowDir = lddcreate(DEM,1e31,1e31,1e31,1e31)
    if saveDDL: 
        pcr.report(FlowDir,'data\ddl.map')
    ## Strahler order 
    print('#####......Computing Strahler order.......######')
    strahlerOrder = streamorder(FlowDir)
    strahlerRiver = ifthen(strahlerOrder>=threshold,strahlerOrder)
    if saveStrahOrder:
        pcr.report(strahlerRiver, 'data\strahlerRiver.map')
    ## Finding outlets
    print('#####......Finding outlets.......######')
    junctions = ifthen(downstream(FlowDir,strahlerOrder) != strahlerRiver, boolean(1))
    outlets = ordinal(cover(uniqueid(junctions),0))
    print('#####......Calculating subcatchment.......######')
    subCatchments = catchment(FlowDir,outlets)
    if saveSubCath:
        pcr.report(subCatchments,'data\subCathments.map')
    print('#####......Computing HAND.......######')
    areaMin = areaminimum(DEM,subCatchments)
    HAND = DEM - areaMin
    pcr.report(HAND,HANDPath)
    aguila(HAND)
    print('#####......Ready to print.......######')
    aguila(subCatchments)
    aguila(areaMin)
    # pcr.report(areaMin,'data\z_drainage.map')
    
