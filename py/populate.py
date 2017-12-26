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

def populate_rowcol(Na, where = None, condition_populate = 'habitat', replace = False,
                    group = False, group_sizes = []):
    '''
    
    replace: logical (True/False); whether two agents can (cannot) inhabit the same cell.
    '''
    
    # If a spatial reference was defined to populate the environment with agents
    if where is not None:
        
        # If the number of agents if greater than the number of available cells 
        # and two agents cannot inhabit the same cell
        if Na > len(where) and replace == False:
            raise ValueError('There are too much agents for this landscape!')        
        # If the number of agents and the available cells are ok 
        else:        
            
            # If agents represent groups, check if there is a group size value for each agent
            if group == True and Na != group_sizes.shape[0]:
                raise ValueError('The number of groups is different from the number of group size values! Please check it.')
            
            # If only habitat will be populated (in this case, where should be an array of habitat cells)
            if condition_populate == 'habitat':
    
                # Test if it is an array with two columns
                            
                # Sample locations
                # This samples rows of the array of available cells
                populated_pixels = where[np.random.choice(where.shape[0], Na, replace=replace)]
                
                # Add noise in the interval [0,1) to the initial position
                xy = populated_pixels + np.random.random((Na, 2))
                
                # Check if it is group, and define all individuals with the same location
                if group:
                    xy = np.repeat(xy, group_sizes, axis = 0)
                
                return xy
            else:
                raise ValueError('You should define the condition where the agents should be placed.')
    else:
        return None
        
    
    


#----------------------------------------------------------
# New functions

def group_size(Ngroups, distribution = 'Gaussian', mu = 5.0, sd = 1.0, minimum = 2, file_dist = ''):
    '''
    This function defines the number of individuals per group.
    
    Input: 
    Ngroups: Number of groups/agents.
    distribution: kind of distribution from where number of individuals should be sampled. May be: Gaussian, Possion, Empiric.
    mu: mean of the Gaussian distribution.
    sd: standard deviation of the Gaussian distribution.
    minimum: minimum number of individuals per group.
    file_dist: name of a file with the distribution of group sizes from which to sample.
    
    Output:
    Returns total number of individuals, and a list of group sizes
    '''
    
    # Draw random group sizes from a distribution
    if distribution == 'Gaussian':
        group_sizes = np.random.normal(loc = mu, scale = sd, size = Ngroups).astype(int)
    elif distribution == 'Poisson':
        group_sizes = np.random.poisson(lam = mu, size = Ngroups)
    elif distribution == 'Empiric':
        # implement when needed
        # read from file_read
        pass
    else:
        raise Exception('The distribution for group sizes should be Gaussian, Poisson, or Empiric.')
    
    # Add individuals if he number is lower than minimum
    np.maximum(group_sizes, minimum, out=group_sizes)
    #group_sizes = np.where(group_sizes < minimum, minimum, group_sizes)
    
    # Return total number of individuals, and a list of group sizes
    return group_sizes.sum(), group_sizes
    

#def compose_group(Nind, pergroup = True, Ngroups = 1, persize = False, mu = 5, sd = 1, )

def conditions_monogramy(list_ind = [], assign_sex = False, assign_reproductive = False):
    '''
    This function defines the first two individuals of a group [represented by an array of values]
    as the reproductive individuals (assign sex - male=0/female=1 or assign reproductive - reproductive=1)
    '''
    if len(list_ind) < 2:
        raise ValueError('The list of individuals must be longer than 2.')
    else:
        # For assigning sex
        if assign_sex:
            list_ind[0:2] = [0,1] # The first two individuals are defined as reproductive male (0) and female (1)
            return list_ind # Return the list of sexes for the group
        # For assigning if the individual is reproductive
        elif assign_reproductive:
            list_ind[0:2] = [1,1] # The first two individuals are defined as reproductive male (0) and female (1)
            return list_ind # Return the list of sexes for the group        

def assign_sex_not_efficient(Na, sex_ratio = 0.5, group = False, group_sizes = None, condition = None):
    '''
    This function attributes sex (0 = male, 1 = female) for agents/individuals.
    
    Input:
    Na: Number of agents - individuals or groups (if group == True).
    sex_ratio: float between 0 and 1. Ratio (number females/number males).
    group: logical; whether agents are groups.
    group_sizes: numpy array of ints; group sizes (in case group == True).
    condition: any special condition such as monogamy, for groups.
    
    Output:
    An array of sexes (for group == False) or an array of (groups) arrays of sexes (for group == True).
    '''
    
    # Check if sex_ratio is in the interval [0,1]
    if sex_ratio >= 0 and sex_ratio <= 1:
        # Probability of choosing male or female
        prob_choose_sex = [1 - sex_ratio, sex_ratio] # (prob males, prob females)
    else:
        raise ValueError('Sex ratio must be in the interval [0,1].')
    
    # For groups, define sex for each individual
    if group:
        
        # Sample for all individuals in a single array
        sexes_allgroups = np.random.choice([0, 1], size = group_sizes.sum(), p = prob_choose_sex)
        # Split the array to respect group size
        split = group_sizes.cumsum()[0:-1]
        # Splits into groups
        sex = np.split(sexes_allgroups, split)
        
        # If monogamy, the first individual of each group is assingned as a couple (male=0/female=1)
        if condition == 'monogamy':
            sex = [conditions_monogramy(i, assign_sex = True) for i in sex]
        
        # Return a list of arrays, one for each group
        return sex
    
    # Define sex for each individual
    else:
        # Return a list of sexes, one element for each individual
        return np.random.choice([0, 1], size = Na, p = prob_choose_sex).tolist() # 0 = male; 1 = female
    

def assign_sex(Na, sex_ratio = 0.5, group = False, group_sizes = None, condition = None):
    '''
    This function attributes sex (0 = male, 1 = female) for agents/individuals.
    
    Input:
    Na: Number of agents - individuals or groups (if group == True).
    sex_ratio: float between 0 and 1. Ratio (number females/number males).
    group: logical; whether agents are groups.
    group_sizes: numpy array of ints; group sizes (in case group == True).
    condition: any special condition such as monogamy, for groups.
    
    Output:
    An array of sexes (for group == False) or an array of (groups) arrays of sexes (for group == True).
    '''
    
    # Check if sex_ratio is in the interval [0,1]
    if sex_ratio >= 0 and sex_ratio <= 1:
        # Probability of choosing male or female
        prob_choose_sex = [1 - sex_ratio, sex_ratio] # (prob males, prob females)
    else:
        raise ValueError('Sex ratio must be in the interval [0,1].')
    
    # For groups, define sex for each individual
    if group:
        
        # Sample for all individuals in a single array
        sex = np.random.choice([0, 1], size = group_sizes.sum(), p = prob_choose_sex) # 0 = male; 1 = female
        
        # If monogamy, the first individual of each group is assingned as a couple (male=0/female=1)
        if condition == 'monogamy':
            # Identify index of males and females per group
            indexes_male = np.append(np.zeros(1, dtype = np.int8), group_sizes.cumsum()[0:-1]) # First individual of each group
            indexes_female = indexes_male + 1            
            
            # Set the first individual of each group as male
            sex[indexes_male] = 0
            # Set the second individual of each group as female
            sex[indexes_female] = 1
        
        # Return a list of arrays, one for each group
        return sex
    
    # Other conditions to be implemented.
    
    # Define sex for each individual
    else:
        # Return a list of sexes, one element for each individual
        return np.random.choice([0, 1], size = Na, p = prob_choose_sex) # 0 = male; 1 = female
    
    
def define_home_range(Na, distribution = 'Gaussian', minimum_HRsize = 0, mean_HRsize = 10, SD_HRsize = 2):
    '''
    home ranges in hectares
    distribution = 'Gaussian', 'constant'
    '''
    
    # Draw random home range sizes from a distribution
    
    # Gaussian distribution
    if distribution == 'Gaussian':
        home_ranges = np.random.normal(loc = mean_HRsize, scale = SD_HRsize, size = Na)
        
        # If there are values smaller than the minimum HRsize, try to resample them
        cont = 0
        less_than_minimum = (home_ranges < minimum_HRsize)
        while np.any(less_than_minimum == True):
            # Draw a new random sample
            new_sample = np.random.normal(loc = mean_HRsize, scale = SD_HRsize, size = 10*Na)
            # Take only values > minimum HRsize
            new_sample_valid = new_sample[new_sample >= minimum_HRsize]
            
            # Check how many values are < minimum in the original dataset
            indexes = np.where(less_than_minimum)
            n_less = indexes[0].shape[0]
            
            # Update values
            if n_less <= new_sample_valid.shape[0]:
                home_ranges[indexes] = new_sample_valid[n_less]
            else:
                home_ranges[indexes][0:new_sample_valid.shape[0]] = new_sample_valid
                
            # Update counter and check if the are still values less than minimum
            cont += 1
            less_than_minimum = (home_ranges < minimum_HRsize)
            
            if cont > 30:
                raise Exception('It is impossible to generate valid home ranges with the parameters given.')
    
    # Constant value for all agents  
    elif distribution == 'constant':
        
        # If mean_HRsize is zero, negative, or smaller than the minimum
        if mean_HRsize < minimum_HRsize or mean_HRsize <= 0:
            # Raise error
            raise ValueError('The home range size must be greater than zero and greater than the minimum home range size.')
        # If not, go on
        else:
            home_ranges = np.repeat(mean_HRsize, Na)
            
    # Empiric distribution
    elif distribution == 'Empiric':
        # implement when needed
        # read from file_read
        pass
    else:
        raise Exception('The distribution for group sizes should be Gaussian, constant, or Empiric.')
        
    # Return array of home ranges, one for each agent
    return home_ranges

        
def assign_age_reproductive(Na, mean_age = 5 * 12, sd_age = 2 * 12, maximum_age = 10 * 12, 
                            set_reproductive = None, reproductive_age = 4 * 12, 
                            group = False, group_sizes = None, condition = None):
    '''
    This function attributes age and the status of reproductive (0 = non-reproductive, 1 = reproductive) 
    for agents/individuals for beginning the simulation.
    
    Input:
    Na: int; Number of agents - individuals or groups (if group == True).
    mean_age: float; mean age of individuals at the beginning of the simulation. ### we can put a condition - if mean = 0, set all 0.
    sd_age: float; standard deviation of age of individuals at the beginning of the simulation.
    maximum_age: float; maximum age of an individual (if dies if it is older).
    set_reproductive: logical (True/False); if True, the reproductive status of individuals is defined.
    reproductive_age: float; the minimum age for individuals to reproduce. It is considered only if set_reproductive == True.
    group: logical (True/False); whether agents are groups.
    group_sizes: numpy array of ints; group sizes (in case group == True).
    condition: string (or None); any special condition such as monogamy, for groups.
    
    Output:
    An array of sexes (for group == False) or an array of (groups) arrays of sexes (for group == True).
    '''
    
    # For groups, define age and reproductive status for each individual
    if group:
        
        # Set ages randomly for each individual
        ages = np.random.normal(loc = mean_age, scale = sd_age, size = group_sizes.sum()).round(2) # in months
        
        # If monogamy, the first individual of each group is assingned as a couple (male=0/female=1)
        if condition == 'monogamy':
            
            # If one wants to set the reproductive status of agents
            if set_reproductive:
                # Identify index of males and females per group
                indexes_male = np.append(np.zeros(1, dtype = np.int8), group_sizes.cumsum()[0:-1]) # First individual of each group - male
                indexes_female = indexes_male + 1 # Second individual of each group - female                
                
                # Set all individuals as non-reproductive
                repro = np.zeros(group_sizes.sum(), dtype = np.int8)
                # Set the first and second individuals of each group as reproductive
                repro[indexes_male] = repro[indexes_female] = 1
                
                # Set ages of reproductive individuals as between reproductive age and maximum age
                #ages[(repro == 1) & (ages < reproductive_age)] = reproductive_age
                np.maximum(ages, reproductive_age, where=(repro==1), out = ages)
        
        # Other conditions to be implemented.
        else:
            if set_reproductive:
                repro = np.random.random_integers(0, 1, size = group_sizes.sum()) # 1 = reproductive, 0 = non-reproductive

        if not set_reproductive:
            repro = None
            
        # Check minimum and maximum values for age
        np.clip(ages, 0.5 * 12, maximum_age - (0.5 * 12), out = ages) # Clip values between 6 and maximum_age - 6 months
        
        # Return arrays of ages and reproductive state
        return ages, repro        
    
    # Define age and reproductive status for each individual
    else:
        # Array of ages, one element for each individual
        ages = np.random.normal(loc = mean_age, scale = sd_age, size = Na).round(2) # in months
        np.clip(ages, 0.5 * 12, maximum_age - (0.5 * 12), out = ages) # Clip values between 6 and maximum_age - 6 months
        #ages = np.where(ages > maximum_age, maximum_age - (ages % maximum_age), ages) # Check if any age is greater than maximum age
        #ages = np.where(ages < 0, abs(ages), ages) # Check if any age is smaller than zero
        
        # If one wants to set the reproductive status of agents
        if set_reproductive:
            # Reproductive status
            repro = np.random.random_integers(0, 1, size = Na) # 1 = reproductive, 0 = non-reproductive
        else:
            repro = None
        
        # Return arrays of ages and reproductive state
        return ages, repro


def estimate_popsize_K(landscape, pland, min_homerange_size):
    '''
    This function estimates the start population size, given the size of the landscape,
    the proportion of habitat in the landscape, and the minimum indivial homerange size.
    Input:
    - landscape_matrix: matrix/map of habitat/matrix or map of habitat(HQ,MQ)/matriz(LQ)
    - pland: percentage of habitat in the landscape (0 - 100)
    - homerangesize: minimum homerange size for an agent/individual
    - spatialresolution: size of the map pixels
    Output:
    - tmp_starting_popsize: start population size, considering the population
      at the carrying capacity of the landscape
    '''

    # put two options: put individuals considering only landscape amount of habitat, randomly; put individuals considering patch size
    
    pland_0_1 = float(pland)/100.0
    
    PixelAreaHA=float(spatialresolution*spatialresolution)/10000.0
    LandscapePixels=len(landscape_matrix)*len(landscape_matrix[0])
    tmp_starting_popsize=int(pland_0_1*LandscapePixels*PixelAreaHA/homerangesize)+1
    
    return tmp_starting_popsize