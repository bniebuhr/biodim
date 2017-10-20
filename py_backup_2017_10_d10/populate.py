import random
import numpy as np


def populate_random(forest, nPop):
    '''
    This function populates the landscape with 'nPop' individuals inside habitat/forest.
    Important: it returns the cell, not the position itself inside the cell!
    Input:
    - forest: cells (row, col) of the map that correspond to habitat/forest.
    - nPop: initial population (number of individuals)
    Output:
    - list of positions (cell) of each individual
    '''
    
    populated_pixels = np.array(random.sample(forest, nPop)) # no replacement; max one individual per pixel
    pos_inside_pixel = np.random.random((nPop, 2))
    
    xy = np.empty((nPop, 2))
    xy[:,0] = populated_pixels[:,0] + pos_inside_pixel[:,0]    
    xy[:,1] = populated_pixels[:,1] + pos_inside_pixel[:,1]
        
    return xy.tolist()



def populate_xy(forest, nPop, spatialresolution, x_west, y_north):
    '''
    This function populates the landscape with 'nPop' individuals inside habitat/forest.
    Important: it returns the cell, not the position itself inside the cell!
    Input:
    - forest: cells (row, col) of the map that correspond to habitat/forest.
    - nPop: initial population (number of individuals)
    Output:
    - list of positions (cell) of each individual
    '''
    
    populated_pixels = np.array(random.sample(forest, nPop)) # no replacement; max one individual per pixel
    pos_inside_pixel = spatialresolution * np.random.random((nPop, 2))
    
    xy = np.empty((nPop, 2))
    xy[:,0] = x_west + spatialresolution*populated_pixels[:,1] + pos_inside_pixel[:,1]
    xy[:,1] = y_north - spatialresolution*populated_pixels[:,0] - pos_inside_pixel[:,0]
    
    return xy.tolist()
