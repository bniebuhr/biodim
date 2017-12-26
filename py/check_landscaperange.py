
# Import modules
import numpy as np

def check_landscaperange(list_of_xy, landscape_matrix):
    '''
    This function...
    '''
    
    map_rows = len(landscape_matrix)
    map_cols = len(landscape_matrix[0])
    
    list_of_xy_modified=[]
    for i in range(len(list_of_xy)):
        list_of_xy_modified.append(list_of_xy[i])
    
    changed_quadrant=[]
    for indiv in range(len(list_of_xy)):
        #let row be ok
        ns=0
        ew=0
        
        if list_of_xy_modified[indiv][0] < 0:
            list_of_xy_modified[indiv][0] = list_of_xy_modified[indiv][0] + map_rows
            ns=+1 #gone to North
        if list_of_xy_modified[indiv][0] > map_rows:
            list_of_xy_modified[indiv][0] = list_of_xy_modified[indiv][0] - map_rows
            ns=-1 #gone to South
        #let col be ok  
        if list_of_xy_modified[indiv][1] > map_cols:
            list_of_xy_modified[indiv][1] = list_of_xy_modified[indiv][1] - map_cols
            ew=+1 #gone to East        
        if list_of_xy_modified[indiv][1] < 0:
            list_of_xy_modified[indiv][1] = list_of_xy_modified[indiv][1] + map_cols
            ew=-1 #gone to West
        changed_quadrant.append([ns,ew])
        
    return list_of_xy_modified, changed_quadrant


def check_landscaperange_np(list_of_xy, landscape_shape, option = 'no_cross'):
    
    # Copy of the list of positions
    modified_list_of_xy = np.array(list_of_xy)
    
    # Individual die/disapear if they cross the boundaries of the landscape
    if option == 'no_cross':
        
        # Transform positions outside ranges (in y - rows) into NaN
        modified_list_of_xy[:,0] = np.where(np.bitwise_or(modified_list_of_xy[:,0] < 0,
                                                          modified_list_of_xy[:,0] > landscape_shape[0]),
                                            np.nan, modified_list_of_xy[:,0])
        
        # Transform positions outside ranges (in x - cols) into NaN
        modified_list_of_xy[:,1] = np.where(np.bitwise_or(modified_list_of_xy[:,1] < 0,
                                                          modified_list_of_xy[:,1] > landscape_shape[1]),
                                            np.nan, modified_list_of_xy[:,1])
    
    # Error if the option typed is not valid
    else:
        raise ValueError('The only option implemented is "no_cross". Please check it or implement another one.')
    
    # Return the modified list of positions
    return modified_list_of_xy