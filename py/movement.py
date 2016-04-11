#---------------------------------------------------------------------------------------
"""
 BioDIM - Biologically scaled Dispersal Model
 
 Movement module

 Functions:
 - get_listofposition
 - OnHabitat
 - disperse_habitat_dependent
 - disperse_random_walk
 
"""
#---------------------------------------------------------------------------------------

import random
import math
import numpy as np
from check_landscaperange import check_landscaperange
from identify_patchid import identify_patchid

#----------------------------------------------------------------------
def get_listofposition(landscape_matrix, modified_indiv_xy_startpos, avg_movement_dist_meters, spatialresolution):
    '''
    This function generates a list of "n_positions" random locations inside a square of side 2x"avg_movement_dist_meters" centered in the animal
    position; this locations are possible moves given by the animal in its routine movement regime
    Input:
    - landscape_matrix: map of habitat/non-habitat (used only for getting landscape dimensions)
    - modified_indiv_xy_startpos: position of the individual
    - avg_movement_dist_meters: average step length of an animal, in meters
    - spatialresolution: spatial resolution (grain) of the landscape (size of the pixel)
    Output:
    - listofpositions: list of random possible locations for the animal move
    '''
    
    n_positions=20
    
    avg_movement_dist_pixel = float(avg_movement_dist_meters)/float(spatialresolution) # number of pixels of the average movement distance
    
    listofpositions=[]
    for pos in range(n_positions):
        deltaX=random.uniform(-avg_movement_dist_pixel, avg_movement_dist_pixel)
        deltaY=random.uniform(-avg_movement_dist_pixel, avg_movement_dist_pixel)
        listofpositions.append([modified_indiv_xy_startpos[0]+deltaX, modified_indiv_xy_startpos[1]+deltaY])

    listofpositions, changed_quadrante_psicologic = check_landscaperange(listofpositions, landscape_matrix)
    
    return listofpositions

#----------------------------------------------------------------------
def OnHabitat(landscape_habdist, landscape_frag_pid, species_profile, listposition): # leads with spatial resolution - PIXELS AND DISTANCE
    '''
    This function...
    '''
    
    aux=[]
    for i in range(len(listposition)):
        aux.append([listposition[i][0],listposition[i][1]])
        
    OnHabitatList=[] #X, Y
    OnHabitatEdgedistList=[] #DIST from edge
    
    for position in range(len(aux)):
        # The line below is not necessary, since this was done in the end of the function get_listofposition
        #aux, changed_quadrante=check_landscaperange(aux, Form1.landscape_matrix)
        YY=aux[position][0]
        XX=aux[position][1]        
        row=int(YY)
        col=int(XX)
        distfromedge = landscape_habdist[row][col]
        # the line below is to differentiate between habitat and fragment dependent
        # if frag_id > 0, it is habitat for fragment dependent species
        frag_pid = identify_patchid([XX, YY], patchid_map=landscape_frag_pid)

        ##'Random walk','Core dependent','Frag. dependent', 'Habitat dependent', 'Moderately generalist'
        
        if distfromedge <= 0 and species_profile == "Habitat dependent":
            # <=0 above means the the full patch is considered.. 
            # corridor (<60m) IS INCLUDED as "habitat patch"
            OnHabitatList.append([YY,XX])
            OnHabitatEdgedistList.append(distfromedge)
            
        if distfromedge <= 0 and frag_pid > 0 and species_profile == "Frag. dependent":
        
            # < (-30) means 30 meters from edge
            # so only the fragment is considered.. corridor (<60m)
            # is NOT INCLUDED as "habitat patch"
            OnHabitatList.append([YY,XX])
            OnHabitatEdgedistList.append(distfromedge)

        if distfromedge <(-30) and species_profile == "Core dependent":
            ### I COPYED THIS PART FROM ABOVE ON FEV2010 - CHECK CHECK CHECK m
            #####  check -30 !!!!
            # < (-30) means 30 meters from edge
            # so only the fragment is considered.. corridor (<60m)
            # is NOT INCLUDED as "habitat patch"
            OnHabitatList.append([YY,XX])
            OnHabitatEdgedistList.append(distfromedge)
            
        if distfromedge <= (+30) and species_profile == "Moderately generalist":
            # <=+30 above means the the full patch is considered.. 
            # corridor (<60m) IS INCLUDED as "habitat patch"
            # Positions <30 of ANY HABITAT PATCH is considered within habitat patch"
            
            OnHabitatList.append([YY,XX])
            OnHabitatEdgedistList.append(distfromedge)
            
        if distfromedge <= (+60) and species_profile == "Highly generalist":
            # <=+60 above means the the full patch is considered.. 
            # corridor (<60m) IS INCLUDED as "habitat patch"
            # Positions <60 of ANY HABITAT PATCH is considered within habitat patch"
            
            OnHabitatList.append([YY,XX])
            OnHabitatEdgedistList.append(distfromedge)

    return OnHabitatList, OnHabitatEdgedistList


#----------------------------------------------------------------------
def disperse_habitat_dependent(distance_matrix, frag_pid_matrix, indiv_xy, species_profile, indiv_isdispersing, indiv_totaldistance, avg_movement_dist_meters, spatialresolution, when_dispersing_distance_factor, indiv_movdirectionX, indiv_movdirectionY):
    '''
    This function ...
    '''
    
    modified_indiv_xy=[]
    for i in range(len(indiv_xy)):
        modified_indiv_xy.append([indiv_xy[i][0],indiv_xy[i][1]])
   
    step_length = []
    for indiv in range(len(modified_indiv_xy)):
        x1=modified_indiv_xy[indiv][0]
        y1=modified_indiv_xy[indiv][1]
        if indiv_isdispersing[indiv] == 0:
            modified_indiv_xy_listposition = get_listofposition(distance_matrix, modified_indiv_xy[indiv], avg_movement_dist_meters, spatialresolution)
            modified_indiv_xy_listposition, distfromedge = OnHabitat(distance_matrix, frag_pid_matrix, species_profile, modified_indiv_xy_listposition)
            
            if len(modified_indiv_xy_listposition)>0:
                PROB_go_core_region=0

                if species_profile=="Highly generalist":
                    PROB_go_core_region=0.05                
                if species_profile=="Moderately generalist":
                    PROB_go_core_region=0.05
                if species_profile=="Habitat dependent":
                    PROB_go_core_region=0.1
                if species_profile=="Frag. dependent":
                    PROB_go_core_region=0.3 
                if species_profile=="Core dependent":
                    PROB_go_core_region=0.7
                    
                if np.all(np.array(distfromedge)) < (-90):
                    #when position in relation to edge is > (-) 80 m 
                    #then the individual can move freely
                    #Based on Hansbauer et al 2008 - for C.caudata species
                    PROB_go_core_region=0.05
                    
                if random.uniform(0,1) < PROB_go_core_region: #FORCE go to core of habitats
                    max_distfromedge=min(distfromedge)
                    #### MAX DIST FROM EDGE is equal to min(distfromedgePix)
                    
                    for OnHabitatPosition in range(len(modified_indiv_xy_listposition)):
                        if distfromedge[OnHabitatPosition]==max_distfromedge:
                            modified_indiv_xy[indiv][0]=modified_indiv_xy_listposition[OnHabitatPosition][0]
                            modified_indiv_xy[indiv][1]=modified_indiv_xy_listposition[OnHabitatPosition][1]
                else: #pickup a random distance THAT is OnHabitatList
                    modified_indiv_xy[indiv][0]=modified_indiv_xy_listposition[0][0]
                    modified_indiv_xy[indiv][1]=modified_indiv_xy_listposition[0][1]
        elif indiv_isdispersing[indiv]==1:
            
            #indiv_dispdirectionX, indiv_dispdirectionY = choose_direction_crw(correlation_parameter=0.8, size=1)
            
            disdir_aux_XMIN = indiv_movdirectionX[indiv][0]
            disdir_aux_XMAX = indiv_movdirectionX[indiv][1]
            disdir_aux_YMIN = indiv_movdirectionY[indiv][0]
            disdir_aux_YMAX = indiv_movdirectionY[indiv][1]
            
            avg_movement_dist_pixel = float(avg_movement_dist_meters)/float(spatialresolution) # number of pixels of the average movement distance
            
            #################
            # modificar isso aqui!!!!!!!!!
            if random.uniform(0,1) < 0.2:  #50% of a movements of the dispersing individual will follow a main direction
                modified_indiv_xy[indiv][0]+=random.uniform(disdir_aux_XMIN,disdir_aux_XMAX)*avg_movement_dist_pixel*when_dispersing_distance_factor   # random xpos BUT with preferencial direction
                modified_indiv_xy[indiv][1]+=random.uniform(disdir_aux_YMIN,disdir_aux_YMAX)*avg_movement_dist_pixel*when_dispersing_distance_factor   # random xpos BUT with preferencial direction
            else:
                modified_indiv_xy[indiv][0]+=random.normalvariate(mu=0,sigma=avg_movement_dist_pixel)*when_dispersing_distance_factor   # random xpos
                modified_indiv_xy[indiv][1]+=random.normalvariate(mu=0,sigma=avg_movement_dist_pixel)*when_dispersing_distance_factor   # random ypos
            
        x2=modified_indiv_xy[indiv][0]
        y2=modified_indiv_xy[indiv][1]        
        dist=math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
        if abs(dist)>500 or dist<0: #CHECK - I need to check when the distance is computed wrongly
            #print "error on Total Distance estimation\n"
            dist=0
        indiv_totaldistance[indiv]+=dist
        step_length.append(dist)        

        # creio que nao precise disso...
        #x2y2=[[modified_indiv_xy[indiv][0],modified_indiv_xy[indiv][1]]]
        #x2y2, changed_quadrant_psico = check_landscaperange(x2y2, distance_matrix)
        #x2=x2y2[0][0]
        #y2=x2y2[0][1]
        
        #if changed_quadrant_psico[0][0] != 0:
            #x2 = x2 - changed_quadrant_psico[0][0]*511
        #if changed_quadrant_psico[0][1] != 0:
            #y2 = y2 - changed_quadrant_psico[0][0]*511        
        ##if changed_quadrant_psico[0][0]==1:
            ##x2=x2-511
        ##if changed_quadrant_psico[0][0]==-1:
            ##x2=x2+511
        ##if changed_quadrant_psico[0][1]==1:
            ##y2=y2-511
        ##if changed_quadrant_psico[0][1]==-1:
            ##y2=y2+511            
        ##y2=modified_indiv_xy[indiv][1]
        #dist=math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
        #if abs(dist)>500 or dist<0: #CHECK - I need to check when the distance is computed wrongly
            ##print "error on Total Distance estimation\n"
            #dist=0
        #indiv_totaldistance[indiv]+=dist
        
    modified_indiv_xy, changed_quadrant = check_landscaperange(modified_indiv_xy, distance_matrix)
    return modified_indiv_xy, indiv_totaldistance, step_length, changed_quadrant


#----------------------------------------------------------------------
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
