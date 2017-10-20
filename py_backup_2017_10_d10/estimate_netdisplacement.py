import math

def estimate_netdisplacement(input_xy_initpos, input_xy, input_xy_quadrant, landscape_matrix):
    """
    This function calculates the distance between the initial (at the beginning of the simulation)
    and current/final position of the individuals, for each individual (the effective distance)
    Input:
     input_xy_initpos: list of individual initial positions (x, y) [at the beginning of the simulation]
     input_xy: list of individual current/final positions (x, y) [after some time of simulation]
     input_xy_quadrant: final number of times each animal crossed map borders - accounts for real net displacement
    Output:
     nd: net displacement, list of distances between initial and current locations, for each individual
    """    
    nd=[]
    
    for indiv in range(len(input_xy_initpos)):
        row_initpos=input_xy_initpos[indiv][0]
        col_initpos=input_xy_initpos[indiv][1]
        row_adjfact=input_xy_quadrant[indiv][0]
        col_adjfact=input_xy_quadrant[indiv][1]
        row_current=input_xy[indiv][0]
        col_current=input_xy[indiv][1]        
        
        row_finalpos=row_current-row_adjfact*len(landscape_matrix)
        col_finalpos=col_current+col_adjfact*len(landscape_matrix)

        dist=math.sqrt((row_initpos-row_finalpos)*(row_initpos-row_finalpos)+(col_initpos-col_finalpos)*(col_initpos-col_finalpos))

        nd.append(dist)
    return nd