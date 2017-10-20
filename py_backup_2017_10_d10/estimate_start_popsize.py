
def estimate_start_popsize(landscape_matrix, pland, homerangesize, spatialresolution):
    '''
    This function estimates the start population size, given the size of the landscape,
    the proportion of habitat in the landscape, and the minimum indivial homerange size.
    Input:
    - landscape_matrix: matrix/map of habitat/matrix or map of habitat(HQ,MQ)/matriz(LQ)
    - pland: percentage of habitat in the landscape (0 - 100)
    - homerangesize: minimum homerange size for an agent/individual
    - spatialresolution: size of the map pixels
    Output:
    - tmp_starting_popsize: start population size, considering the population
      at the carrying capacity of the landscape
    '''
    
    pland_0_1 = float(pland)/100.0
    PixelAreaHA=float(spatialresolution*spatialresolution)/10000.0
    LandscapePixels=len(landscape_matrix)*len(landscape_matrix[0])
    tmp_starting_popsize=int(pland_0_1*LandscapePixels*PixelAreaHA/homerangesize)+1
    
    return tmp_starting_popsize