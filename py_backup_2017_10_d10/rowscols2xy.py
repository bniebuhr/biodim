import numpy as np

def rowscols2xy(xy_rowscols, spatialresolution, x_west, y_north):
    '''
    This function takes a series of rows and columns in which animals are located, and use map information to define
    the real (x,y) position of the animals, given a Datum and a Reference Coordinare System
    Input:
    - xy_rowscols: list of animal positions, in the format [row, col] - allows fractions of row and col values ([1.13, 7.12]) 
    - spatialresolution: resolution/grain of the landscape (pixel size)
    - x_west: western limit of the map
    - y_north: northern limit of the map
    Output:
    - xy.tolist(): list of animal positions, in the format [x, y] (in meters)
    '''
    
    nPop = len(xy_rowscols)
    rowscols = np.array(xy_rowscols)

    xy = np.empty((nPop, 2))
    xy[:,0] = x_west + spatialresolution*rowscols[:,1]
    xy[:,1] = y_north - spatialresolution*rowscols[:,0]
    
    return xy.tolist()
