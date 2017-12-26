import random
import numpy as np
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

def mortality_general(individuals_alive, include_mortality = True, 
                      mortality_rate = [0.05], mortality_option = 'constant',
                      individuals_age = [], age_classes = [], habitat_types = []):
    '''
    This function calculates the mortality rate, for a given species profile and position in the landscape,
    and randomly defines if an individual will keep alive or die, given this mortality rate.
    
    Input:
    individuals_alive: numpy array with int values; array of values indicating whether each individual is alive (1) or dead (0).
    include_mortality: (True/False) logical; if True, mortality is considered; if False, individuals do not die.
    mortality_rate: list with float values; single value if mortality is constant, or several values for different habitats/matrices or different age classes, for instance.
    ### variation with distance from edge: to be implemented
    mortality_option: string; the way mortality will be considered. It may be 'constant', 'age_class', 'habitat_type', or other.
    individuals_age: numpy array with floats, representing individual age; it is only taken into account if mortality_option == 'age_class'.
    age_classes: array with floats, representing the above age of each age class; it is only taken into account if mortality_option == 'age_class'.
        It makes sense if the age of the last class is the maximum age for agents (you can choose a large number if this is not relevant).
        E.g.: age_classes = [1,2,4,10] indicates the age classes 0-1, 1-2, 2-4, 4-10, 10 being the maximum age possible
        (otherwise the mortality function does not work for these individuals).
    habitat_types: array with floats, representing the above age of each habitat type in the landscape; 
        it is only taken into account if mortality_option == 'habitat_type'.
    
    Output:
    A numpy array indicating whether individuals died (1) or not (0 - may be still alive or have died before).
    '''
    
    if any([(i > 1 or i < 0) for i in mortality_rate]):
        raise ValueError('Mortality rate should be within the interval [0,1]!')
    
    # If mortality is to be included in the simulations, calculate it
    if include_mortality:
        
        # If mortality rate is contant for individuals and locations, calculate it
        if mortality_option == 'constant':
            
            # If mortality rate is constant but there is more than one value in the list of mortality rates, raises error
            # We could also only warn the user and get the first value
            if len(mortality_rate) > 1:
                raise ValueError('You set mortality to be constant, but there is more than one mortality rate value. Please check and retry.')
            # If mortality rate is constant and there is only one value for it, carry on
            else:
                # Checks if random values in the interval [0,1) are smaller than mortality rate, and return 1 (0) if it is (not)
                return np.where(np.random.random(individuals_alive.shape) < mortality_rate[0], 1, 0)
        
        # If mortality rate depend on individual age class, calculate it
        elif mortality_option == 'age_class':
            
            # If mortality rate depends on age class but the number of mortality values is different 
            # from number of age classes, raise error
            if len(mortality_rate) != len(age_classes):
                raise ValueError('You set mortality to be age dependent, but the length in number of \
                mortality rate values and age classes differ. Please check and retry.')
            
            # If mortality rate depends on age class but the number of individuals is different 
            # in the list of individuals alive and the list of individual ages, raise error
            elif individuals_alive.shape != individuals_age.shape:
                raise ValueError('You set mortality to be age dependent, but the number of individuals must \
                be the same in the list of individuals alive and individual ages. Please check and retry.')
            
            # If mortality rate is age dependent and their values as ok, carry on
            else:
                # Create a first array of probability of dying with all values = 0
                prob_die = np.zeros(individuals_alive.shape)
                # For each age class 
                for i in range(len(age_classes)):
                    # Define the minimum age of the age class (0 for the first, the previous maximum for the following ones)
                    age_below = 0 if i == 0 else age_classes[(i-1)]
                    # When the age of individuals is within the age class, put the mortality rate for this age class 
                    # in the array of probability of dying
                    np.copyto(prob_die, mortality_rate[i], where=(individuals_age >= age_below) & (individuals_age < age_classes[i]))
                
                # Finally, generate random numbers and check whether individuals die or not, after accounting for
                # age class
                return np.where(np.random.random(individuals_alive.shape) < prob_die, 1, 0)                
                
        # Other situations
        else:
            # Implement dist edges and habitat types later, when necessary
            raise ValueError('Mortality option must be "constant" or "age_class".')
                  
    # If mortality is not to be included in the simulations, return a numpy array with zeros for all individuals (no mortality)
    else:
        return np.zeros(individuals_alive.shape, dtype = np.int8)


