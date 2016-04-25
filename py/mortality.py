import random
from check_landscaperange import check_landscaperange

def get_safetyness_mortality(tab_in, species_profile, distMeters, spatialresolution):
    '''
    This function gets the mortality of safetyness of an individual, given a table of mortality/safetyness
    probability and the distance an animal is from habitat edges (towards inside or outside pathces)
    Mortality/safetyness also depends on species ecological profile
    Input:
    - tab_in: table of mortality or safetyness
    - species_profile: ecological profile of the species
    - distMeters: distance the animal is from habitat edges, in meters
    - spatialresolution: spatial resolution of the map (or grain, the size of the pixels)
    Output:
    - tab_in[][]: Mortality/safetyness value, given a position and a species profile (it is an element of the table)
    '''
    
    if distMeters>0: # for positive values (outside forest patches)
        distMeters = float(distMeters) + float(spatialresolution)
    
    for line in range(len(tab_in)):
        line_dist=tab_in[line][0]
        if float(distMeters) < float(line_dist):
            if line==0:
                if species_profile=="Core dependent":
                    return tab_in[line][1]
                elif species_profile=="Frag. dependent":
                    return tab_in[line][2]
                elif species_profile=="Habitat dependent":
                    return tab_in[line][3]
                elif species_profile=="Moderately generalist":
                    return tab_in[line][4]
                elif species_profile=="Highly generalist":
                    return tab_in[line][5]
                else:
                    return 0
                    
            else:
                if species_profile=="Core dependent":
                    return tab_in[line-1][1]
                elif species_profile=="Frag. dependent":
                    return tab_in[line-1][2]
                elif species_profile=="Habitat dependent":
                    return tab_in[line-1][3]
                elif species_profile=="Moderately generalist":
                    return tab_in[line-1][4]
                elif species_profile=="Highly generalist":
                    return tab_in[line-1][5]
    return 0


def estimate_movement_cost(tab_safetyness, landscape_matrix, species_profile, aux_xy, include_habitatquality, landscape_hqmqlq_quality, distfromedge, spatialresolution):
    protecdness = get_safetyness_mortality(tab_in=tab_safetyness, species_profile=species_profile, distMeters=distfromedge, spatialresolution=spatialresolution)
    
    aux=[aux_xy]
    aux, changed_quadrant = check_landscaperange(aux, landscape_matrix)
    YY=aux[0][0]
    XX=aux[0][1]        # leads with spatial resolution - PIXELS
    row=int(YY)
    col=int(XX)
    
    if include_habitatquality == "HabitatQuality_YES":
        habqualyOnPosition=landscape_hqmqlq_quality[row][col]
    else:
        habqualyOnPosition=1.0

    if protecdness<0.05:
        protecdness=0.05
    if protecdness>1:
        protecdness=1.0
    if habqualyOnPosition<0.05:
        habqualyOnPosition=0.05
    if habqualyOnPosition>1:
        habqualyOnPosition=1.0
    
    cost=1.0/(protecdness*habqualyOnPosition)
    
    return cost


def kill_individual_new(tab_mortality, sp_profile, distfromedge, spatialres):
    '''
    This function calculates the mortality rate, for a given species profile and position in the landscape,
    and randomly defines if an individual will keep alive or die, given this mortality rate.
    Input:
    - tab_mortality: mortality table (a matrix)
    - sp_profile: ecological profile of the species
    - distfromedgePix: minimum distance from the animal's position to habitat edges, in pixels
    - spatialres: spatial resolution of the landscape map (or grain, the size of the pixels)
    Output:
    - continuealive: a variable stating whether the animal is still alive (1) or not (0)
    '''
    
    prob_die=get_safetyness_mortality(tab_in=tab_mortality, species_profile=sp_profile, distMeters=distfromedge, spatialresolution=spatialres)
    
    prob_dieMAX=0.2 ## ???
    prob_dieMAX_target=0.001 ### ???
    prob_die_corrected=prob_die/prob_dieMAX*prob_dieMAX_target

    if prob_die_corrected > random.uniform(0,1):
        continuealive=0
    else:
        continuealive=1

    return continuealive