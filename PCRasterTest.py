import pcraster as pcr
from pcraster import *

def computeHAND(): 
    pcr.setclone('data\BC_Quesnel_PCr_WShed2_Fill.map')
    DEM = pcr.readmap('data\BC_Quesnel_PCr_WShed2_Fill.map')
    threshold = 8
    FlowDir = lddcreate(DEM,1e31,1e31,1e31,1e31)
    pcr.report(FlowDir, 'data\ldd.map')
    ## Strahler order 
    print('Strahler order...')
    strahlerOrder = streamorder(FlowDir)
    strahlerRiver = ifthen(strahlerOrder>=threshold,strahlerOrder)
    pcr.report(strahlerRiver, 'data\strahlerRiver.map')
    ## Finding outlets
    print('Finding outlets...')
    junctions = ifthen(downstream(FlowDir,strahlerOrder) != strahlerRiver, boolean(1))
    outlets = ordinal(cover(uniqueid(junctions),0))
    print('Calculating subcatchment')
    subCatchments = catchment(FlowDir,outlets)
    pcr.report(subCatchments,'data\subCathments.map')
    print('Ready to print')
    aguila(subCatchments)
    print('Computing HAND')
    
def HAND(DEMPath,subCatchmentsPath,handPath):
    '''
    All path can be eather local or full path. 
    '''
    DEM = pcr.readmap(DEMPath)
    subCatchments = pcr.readmap(subCatchmentsPath)
    areaMin = areaminimum(DEM,subCatchments)
    aguila(areaMin)
    pcr.report(areaMin,'data\z_drainage.map')
    HAND = DEM - areaMin
    aguila(HAND)
    pcr.report(HAND,handPath)

def main():
    pass 
       
if __name__ == "__main__":
    main()  