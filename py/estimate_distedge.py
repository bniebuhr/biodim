
def estimate_distedge(indiv_xy_position, landscape_habdist):
    """
    This function takes the information of distance (in meters) from the current
    location of an individual to the nearest patch edge
    Input:
    - indiv_xy_position: position (row, col) of an animal
    - landscape_habdist: matrix of distance to edges, in meters (negative = inside patch; positive = into the matrix)
    Output:
    - distedge: distance of the position to the nearest habitat edge, in meters
    """    

    row=int(indiv_xy_position[0])
    col=int(indiv_xy_position[1])
    #if row<=0:
    #    row=0
    #if row>=511:
    #    row=511
    #if col<=0:
    #    col=0
    #if col>=511:
    #    col=511
        
    distedge = landscape_habdist[row][col]
    return distedge


def estimate_distedgePix(indiv_xy_position, landscape_habdist):
    """
    This function takes the information of distance (in pixels) from the current
    location of an individual to the nearest patch edge
    Input:
    - indiv_xy_position: position (row, col) of an animal
    - landscape_habdist: matrix of distance to edges, in pixels (negative = inside patch; positive = into the matrix)
    Output:
    - distedge: distance of the position to the nearest habitat edge, in pixels
    """    

    row=int(indiv_xy_position[0])
    col=int(indiv_xy_position[1])
    #if row<=0:
    #    row=0
    #if row>=511:
    #    row=511
    #if col<=0:
    #    col=0
    #if col>=511:
    #    col=511
        
    distedgePix = landscape_habdist[row][col]
    return distedgePix