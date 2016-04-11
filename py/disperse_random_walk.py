import random
import numpy as np
from check_landscaperange import check_landscaperange

def disperse_random_walk(landscape_matrix, indiv_xy, avg_movement_dist_meters, spatialresolution, indiv_totaldistance, test=False):
    '''
    This function generates random displacements for a list of animals and update their spatial locations, based on an average distance
    animals move per time step. The function also accounts for distances traveled and update the cumulative distance traveled by each animal.
    Finally, the function checks if animals have crossed map borders and updates animals' positions based on periodic contour conditions.
    Input:
    - landscape_matrix: quality (or binary forest/non-forest) map (what matters here is only the dimensions of the matrix, not its content)
    - indiv_xy: list of animals' spatial locations ([row,col]) 
    - avg_movement_dist_meters: average distance animals move, in meters
    - spatialresolution: spatial resolution of the map, in meters
    - indiv_totaldistance: cumulative distance animals moved so far
    - test: option used only for unit testing (see below); in this case, test=True; in other cases, this argument should be ignored
    Output:
    - modified_indiv_xy: new list of animals' locations [row, col] 
    - indiv_totaldistance: updated list of cumulative (total) distance traveled by animals
    - step_length: list of step length of each animal after the displacement
    - changed_quadrant: list of values (-1,0,+1) stating if each animal has crossed the map borders, in the form [south-north, west-lest]
    
    For tests, run: 
    python disperse_random_walk.py -test [-v]
    
    >>> np.random.seed(0)
    >>> landscape_matrix = np.random.randint(1, size=(512,512))
    >>> indiv_xy = np.random.randint(512, size=(8,2)).tolist()
    >>> avg_movement_dist_meters = 35
    >>> spatialresolution = 30
    >>> indiv_totaldistance = [0.0] * 8
    >>> print disperse_random_walk(landscape_matrix, indiv_xy, avg_movement_dist_meters, spatialresolution, indiv_totaldistance, test=True)
    ([[172.8431116689539, 45.777646683477684], [116.03904870297971, 193.61934504840482], [323.2320267734155, 250.86676693218476], [194.77482366356398, 359.35962162744204], [10.271670194536117, 212.81563242157137], [276.22984011240743, 241.5489752834985], [291.25668768096943, 88.52044919785139], [70.68749556550951, 472.2825181112337]], [1.4849191616850197, 1.883004455926262, 0.26755835614136786, 0.42430189419187886, 2.216679086817165, 0.8925074494657775, 1.6924180827648756, 0.7432809938174787], [1.4849191616850197, 1.883004455926262, 0.26755835614136786, 0.42430189419187886, 2.216679086817165, 0.8925074494657775, 1.6924180827648756, 0.7432809938174787], [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]])
    
    For time tests, run:
    python disperse_random_walk.py -time
    '''
    
    if test: # this argument shoud be used only for testing
        np.random.seed(0123456)
            
    avg_movement_dist_pixel = float(avg_movement_dist_meters)/float(spatialresolution) # number of pixels of the average movement distance
    xy = np.array(indiv_xy)
    
    displacements = np.random.normal(0.0, avg_movement_dist_pixel, (len(xy), len(xy[0])))
    modified_indiv_xy = (xy + displacements).tolist()
    #step_length = np.linalg.norm(displacements, axis=1)
    # the line above is fast, but we need numpy 1.8 or later - how do we install it in grass environment?
    step_length = []
    for point in displacements:
        step_length.append(np.sqrt(point[0]**2 + point[1]**2))
    
    #indiv_totaldistance = (np.array(indiv_totaldistance) + step_length).tolist()
    indiv_totaldistance = (np.array(indiv_totaldistance) + np.array(step_length)).tolist()
    
    modified_indiv_xy, changed_quadrant = check_landscaperange(modified_indiv_xy, landscape_matrix)
    
    #return modified_indiv_xy, indiv_totaldistance, step_length.tolist(), changed_quadrant
    return modified_indiv_xy, indiv_totaldistance, step_length, changed_quadrant

# This one is not being used anymore
def disperse_random_walk_original(landscape_matrix, indiv_xy, movement_dist_sigma_pixel, indiv_totaldistance):
    '''
    This function generates random 
    '''
    '''on landscape_matrix 1=HQ / 2=MQ / 3=LQ'''
    
    modified_indiv_xy=[]
    for i in range(len(indiv_xy)):
        modified_indiv_xy.append(indiv_xy[i])
   
    for xp in range(len(modified_indiv_xy)):
        modified_indiv_xy[xp][0]+=random.normalvariate(mu=0,sigma=movement_dist_sigma_pixel)   # random xpos
        modified_indiv_xy[xp][1]+=random.normalvariate(mu=0,sigma=movement_dist_sigma_pixel)   # random ypos

    modified_indiv_xy, changed_quadrant = check_landscaperange(modified_indiv_xy, landscape_matrix)
    
    return modified_indiv_xy, indiv_totaldistance, changed_quadrant

# unit test
import sys    
if len(sys.argv) > 1 and sys.argv[1] == "-test":
    import doctest
    doctest.testmod()
    
# time test    
if len(sys.argv) > 1 and sys.argv[1] == "-time":
    import time
    
    landscape_matrix = np.random.randint(1, size=(512,512))
    indiv_xy = np.random.randint(512, size=(500,2)).tolist()
    avg_movement_dist_meters = 35
    spatialresolution = 30
    indiv_totaldistance = 0.0    
    
    start_new= time.clock()
    for i in range(1000):
        disperse_random_walk(landscape_matrix, indiv_xy, avg_movement_dist_meters, spatialresolution, indiv_totaldistance)        
    end_new= time.clock()
    time_new= (end_new-start_new)/1000
    
    start_old= time.clock()
    for i in range(1000):
        disperse_random_walk_original(landscape_matrix, indiv_xy, avg_movement_dist_meters/spatialresolution, indiv_totaldistance)        
    end_old= time.clock()
    time_old= (end_old-start_old)/1000
    
    print "original function time: " + repr(time_old) + "s" 
    print "new function time: " + repr(time_new) + "s"
    print "new function is " + repr(time_old/time_new) + " times faster the the original one"

# Trash test
#
#import numpy as np
#np.random.seed(0)
#landscape_matrix = np.random.randint(1, size=(512,512))
#indiv_xy = np.random.randint(512, size=(8,2)).tolist()
#avg_movement_dist_meters = 35
#spatialresolution = 30
#indiv_totaldistance = [0.0] * 8
#print disperse_random_walk(landscape_matrix, indiv_xy, avg_movement_dist_meters, spatialresolution, indiv_totaldistance, test=True)