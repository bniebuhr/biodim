#!/c/Python25 python
import random
#from scipy.stats import wrapcauchy
import numpy as np

def choose_direction_crw(correlation_parameter = 0.001, size = 1):
    '''
    This function...
    '''
    
    angle = wrapcauchy.rvs(c=correlation_parameter, size=size)
    xdir = np.cos(angle)
    ydir = np.sin(angle)
    
    return xdir, ydir
    

def choose_dispersaldirection():
    """
    COMPLETE!
    """    
    direction_MIN=random.uniform(-1,0.75)
    direction_MAX=direction_MIN+0.5
    return [direction_MIN,direction_MAX]