import pcraster as pcr
from pcraster import *

def computeHAND(DEMPath,HANDPath, saveLowDirc:bool=True, saveStrahOrder:bool=True,saveSubCath:bool = True): 
    pcr.setclone(DEMPath)
    DEM = pcr.readmap(DEMPath)
    ## Flow Direcction (Use to take long...)
    threshold = 8
    FlowDir = lddcreate(DEM,1e31,1e31,1e31,1e31)
    if saveLowDirc:
        pcr.report(FlowDir, 'data\ldd.map')
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
