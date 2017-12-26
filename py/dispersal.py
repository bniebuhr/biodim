#---------------------------------------------------
# Dispersal functions for BioDIM GLT
#---------------------------------------------------

import numpy as np
from check_landscaperange import check_landscaperange_np
from populate import define_home_range

def choose_who_disperses(p_disperse, individual_dispersing, dead_individuals, 
                         individual_age, dispersal_age = 1,
                         reproductive_can_disperse = False, individual_reproductive_status = []):
    
    # Individual can be chosen to disperse if they are not dispersing yet, 
    # if they are above the minimum dispersal age, and if they are alive
    # Plus, if reproductive individuals can (cannot) disperse, this is not (is) taken into account
    if reproductive_can_disperse:
        can_disperse = (individual_age >= dispersal_age) & (individual_dispersing == 0) & (dead_individuals == 0)
    else:
        can_disperse = (individual_age >= dispersal_age) & (individual_dispersing == 0) & (dead_individuals == 0) & (individual_reproductive_status == 0)
        
    # Transform array of individuals that can disperse in a vector of probabilities of dispersing
    can_disperse_prob = np.where(can_disperse == True, p_disperse, 0)
    
    # Randomly select which of the individuals that can disperse will disperse
    # And also considers those individuals which are already dispersing
    will_disperse = np.where(np.bitwise_or(np.random.random(can_disperse.shape) < can_disperse_prob,
                                           individual_dispersing == 1), 1, 0)
    
    # Return a vector of individuals that will disperse (emmigrate)
    return will_disperse


def settle(individuals_dispersing = [], individual_group = [], individual_positions = [],
           dead_individuals = [], individual_reproductive_status = [], individual_sex = [],
           agent_id = [], home_range_sizes = [],
           distribution_HR = 'Gaussian', mean_HRsize = 15.0, min_HRsize = 0.0, SD_HRsize = 2.0,
           maximum_distance = 100000.0, p_enter_group = 0.1,
           who_can_mate = 'any', landscape_map = [], patch_id_map = [], patch_area_map = []):
    '''
    who_can_mate may be equal to 'any', 'same_patch'
    '''
    
    # Initialize variables to be updated
    new_individuals_dispersing = np.array(individuals_dispersing)
    new_individual_group = np.array(individual_group)
    new_individual_positions = np.array(individual_positions)
    new_dead_individuals = np.array(dead_individuals)
    new_individual_reproductive_status = individual_reproductive_status
    new_home_range_sizes = np.array(home_range_sizes)
    
    # Identify individuals that can settle - which are alive and dispersing
    can_settle = np.where(np.bitwise_and(individuals_dispersing == 1, dead_individuals == 0))[0]
    
    # Get rows and cols from positions
    pos = new_individual_positions.astype(int)
    rows = pos[:,0]
    cols = pos[:,1]    
    
    # Take information on patch id and patch area if who_can_mate == same_patch
    if who_can_mate == 'same_patch':
        
        # Get individual pid from positions
        individual_pid = patch_id_map[rows,cols]
        
    elif who_can_mate == 'any':
        
        # Get habitat for all individuals
        individual_habitat = landscape_map[rows, cols]
        
    # Get patch area of the patch where individuals are, from their positions
    individual_parea = patch_area_map[rows, cols]    
    
    # Check whether each individual will settle, where, and how
    # For each individual alive dispersing:
    while len(can_settle) > 0:
        
        # Variables indicating what can happen with individuals
        die = 0
        join_group = 0
            
        # The focal individual is the first in the row
        i = can_settle[0]
            
        # Remove individual i from the list of inds than can settle in new groups
        can_settle = can_settle[can_settle != i]
        
        # Sex of the individual
        sex = individual_sex[i]
        
        if who_can_mate == 'same_patch':
            pid = individual_pid[i]
            parea = individual_parea[i]
        elif who_can_mate == 'any':
            habitat = individual_habitat[i]
            parea = individual_parea[i]
        
        # If one of these are null, the individual is in the matrix - it dies - for same patch
        if who_can_mate == 'same_patch' and (pid == 0 or parea == 0 or np.isnan(pid) or np.isnan(parea)):
            die = 1
            ######### this may be changed later to keep individuals dispersing
        elif who_can_mate == 'any' and (habitat != 1):
            die = 1
            ######### this may be changed later to keep individuals dispersing
        
        # If pid and parea are valid
        else:
            # List of individuals dispersing that are potential mates; they must be alive and be of the opposite sex
            if who_can_mate == 'any':
                potential_mates = np.where((individuals_dispersing == 1) & (dead_individuals == 0) &
                                           (individual_sex != sex))[0]
                # In case only he same patch is being considered, patch_id must be taken into account also
            elif who_can_mate == 'same_patch':
                potential_mates = np.where((individuals_dispersing == 1) & (dead_individuals == 0) &
                                       (individual_sex != sex) & (individual_pid == pid))[0]
                # If other option, raise error
            else:
                raise ValueError('who_can_mate must assume the values "any" or "same_patch". Please check itand retry.')
            
            
            # List of individuals in the groups in the same patch, if only the same patch is being considered
            # In case of 'any', all groups are considered
            if who_can_mate == 'any':
                groups_around_inds = np.where((individuals_dispersing == 0) & (dead_individuals == 0))[0]
                # In case only he same patch is being considered, patch_id must be taken into account also
            elif who_can_mate == 'same_patch':
                groups_around_inds = np.where((individuals_dispersing == 0) & (dead_individuals == 0) &
                                              (individual_pid == pid))[0]
                # If other option, raise error
            else:
                raise ValueError('who_can_mate must assume the values "any" or "same_patch". Please check itand retry.')        
        
            # List of groups in the same patch
            groups_around = np.unique(individual_group[groups_around_inds])
            groups_around_index = np.where(agent_id == groups_around[:,None])[1]
            
            # Check if there are other individuals dispersing nearby that are potential mates
            # If there are, try to form a new group (if there is space in the patch)
            if potential_mates.shape[0] > 0:
                
                # Home range of groups in the same patch
                HR_groups_around = home_range_sizes[groups_around_index]
                # Total space occupied by those groups
                total_HR_occupied = HR_groups_around.sum()
                
                # Check if there is enough space left in the patch
                space_left = parea - total_HR_occupied
                
                if space_left > min_HRsize:
                    
                    # If there is, choose one of the potential mates to form a group
                    mate = np.random.choice(potential_mates, size = 1)
                
                    # Form a group <3
                    
                    # Update group information
                    agent_id_index = np.where(agent_id == individual_group[i])
                    HR = define_home_range(Na = 1, distribution = distribution_HR, 
                                                                            minimum_HRsize = min_HRsize, 
                                                                            mean_HRsize = mean_HRsize, SD_HRsize = SD_HRsize)
                    new_home_range_sizes[agent_id_index] = np.minimum(space_left, HR)
                    
                    # Individual 1
                    new_individuals_dispersing[i] = 0 # not dispersing anymore
                    new_individual_reproductive_status[i] = 1 # now it is reproducer
                    #new_individual_group is the same for ind 1
                    #new_individual_positions is the same for ind 1
                    
                    # Check other individuals dispersing together
                    together1 = np.where((individual_group == individual_group[i]) & 
                                         (individuals_dispersing == 1))[0]
                    together1 = together1[together1 != i]
                    
                    # Check if there are individuals dispersing together
                    if together1.shape[0] > 0:
                        # Not dispersing anymore
                        new_individuals_dispersing[together1] = 0
                        # Remove individual together1 from the list of inds than can settle in new groups
                        can_settle = can_settle[can_settle != together1]                        
                        
                    # Individual2
                    
                    # Check other individuals dispersing together
                    together2 = np.where((individual_group == individual_group[mate]) & 
                                         (individuals_dispersing == 1))[0]
                    together2 = together2[together2 != mate]
                    
                    # Check if there are individuals dispersing together
                    if together2.shape[0] > 0:
                        # Not dispersing anymore
                        new_individuals_dispersing[together2] = 0
                        # Remove individual together1 from the list of inds than can settle in new groups
                        can_settle = can_settle[can_settle != together2]                                            
                    
                    # Update main individual2
                    new_individuals_dispersing[mate] = 0 # not dispersing anymore
                    new_individual_reproductive_status[mate] = 1 # now it is reproducer                    
                    new_individual_group[mate] = individual_group[i]
                    new_individual_positions[mate] = new_individual_positions[i]
                    
                    # Remove individual 2 from the list of inds than can settle in new groups
                    can_settle = can_settle[can_settle != mate]
                    
                # If there is no space for new groups, try to join a group    
                else:
                    join_group = 1
            
            # If there are no individuals dispersing nearby, try to join a group
            else:
                join_group = 1
        
        # If the individual is going to try joining an existing group nearby
        if join_group:        
            
            # Check if there are groups 
            if groups_around.shape[0] > 0:            
                
                # We can still see what groups are really nearby, closer than max_distance
                # Try to join
                # Choose a group
                random_group_nearby = np.random.choice(groups_around_index, size = 1)
                
                # Will enter?
                will_enter = np.random.random(1) < p_enter_group
                
                # If the individual was successful, join the group
                if will_enter:
                    # Update variables - whether the individual is dispersing
                    new_individuals_dispersing[i] = 0
                    # Its position
                    inds_group_index = np.where(individual_group == agent_id[random_group_nearby])[0]
                    new_individual_positions[i] = new_individual_positions[inds_group_index[0]]
                    # Its group
                    new_individual_group[i] = agent_id[random_group_nearby]
                # If the individual was not successful in entering the group
                else:
                    die = 1
                    ######### this may be changed later to keep individuals dispersing
                    
        # If there are no groups or individual is not supposed to join a group
        else:
            die = 1
            ######### this may be changed later to keep individuals dispersing
        
        # If die == 1, die
        if die:
            # Individual dies
            new_dead_individuals[i] = 1
            
        # If none of the options before, the individual continues to disperse
        # Go to next individual
        
    # Return values
    return new_individuals_dispersing, new_individual_group, new_individual_positions, new_dead_individuals, new_individual_reproductive_status, new_home_range_sizes



def dispersal_step_selection_simple(individuals_dispersing = [], individual_positions = [], 
                                    dead_individuals = [], individual_group = [],
                                    max_agent_id = 0,
                                    ntries = 50, nsteps = 1, 
                                    distribution = "Weibull", scale = 100.0, shape = 2.0,
                                    landscape_map = [], landscape_values = [1]):
    
    
    # Copy of numpy arrays to be modified and returned
    new_individual_positions = np.array(individual_positions)
    new_dead_individuals = np.array(dead_individuals)
    new_individual_group = np.array(individual_group)
    
    # Create variable max_id, that will be updated if new agents (dispering individuals) are created
    max_id = max_agent_id
    
    # ID of the new agents to be created representing dispersing individuals
    new_agents_IDs = np.empty(0, dtype = np.int64)    
    
    # Initialize a count of number and distance of dispersals to be summed to the overall dispersal statistics
    dispersed = np.zeros(individuals_dispersing.shape, dtype = np.int8)
    distance_dispersed = np.zeros(individuals_dispersing.shape)
    
    # Number of individuals dispersing
    inds = individuals_dispersing.sum()
    who = np.where(individuals_dispersing)[0]
    
    # Generate ntries random distances to be dispersed, from a distribution
    nsamples = ntries * inds
    
    # Draw distances from a Weibull distribution
    if distribution == "Weibull":
        distance_samples = scale*np.random.weibull(shape, nsamples)
        
    # Draw random angles
    angles = 2*np.pi*np.random.rand(nsamples)
    
    displacement_xy = np.empty(shape = (nsamples, 2))
    displacement_xy[:,0] = distance_samples * np.cos(angles)
    displacement_xy[:,1] = distance_samples * np.sin(angles)
       
    # Counter for the number of the individuals disperser
    cont = 0
    
    # For each of the dispersers, select i as the first line
    for i in np.arange(1, nsamples, ntries):
        # Select random distances for the first individual
        dists = displacement_xy[i:(i+ntries)]
        
        # Takes the starting point for this individual
        start_point = individual_positions[who[cont]]
        # Sums distance in x and y to represent the possible displacements
        end_points = start_point + dists
        
        # Check if new end positions are within the landscape and 
        # replace values outside the landscape by np.NaN
        end_points_mod = check_landscaperange_np(list_of_xy = end_points, 
                                                 landscape_shape = landscape_map.shape,
                                                 option = 'no_cross')
        
        # Removing rows with NaN in any of the columns
        end_points_mod = end_points_mod[np.bitwise_and(np.isnan(end_points_mod[:,0]) == False,
                                                       np.isnan(end_points_mod[:,1]) == False)]
        
        # Get rows and cols from positions
        pos = end_points_mod.astype(int)
        rows = pos[:,0]
        cols = pos[:,1]
                    
        # Get landscape_class/value from positions in the landscape map
        landscape_class = landscape_map[rows,cols]
        
        # Check which positions are within a valid "habitat" value of the landscape_values list
        mask = np.in1d(landscape_class, landscape_values)
        possible_new_positions = end_points_mod[mask,:]
        
        # If there is at least one position in a valid landscape element, choose the 1st as the dispersal site
        if possible_new_positions.shape[0] > 0:
            # Select the first as the new position
            new_individual_positions[who[cont]] = possible_new_positions[0]
            # Updates number of dispersal events and distance dispersed
            dispersed[who[cont]] = 1
            distance_dispersed[who[cont]] = np.linalg.norm(possible_new_positions[0] - start_point)
            # Updates individual group - it takes a new value for dispersing individuals
            new_individual_group[who[cont]] = max_id + 1
            # Update the number of total agents
            max_id += 1
            # Update new IDs of dispersing agents
            new_agents_IDs = np.concatenate((new_agents_IDs, np.array([max_id])))                                    
            
        # If there is no displacements to habitat, the animal died
        else:
            new_dead_individuals[who[cont]] = 1
            
        # Increase individual counter
        cont += 1
        
    return dispersed, distance_dispersed, new_individual_positions, new_dead_individuals, new_individual_group, max_id, new_agents_IDs
    

#----------------------------------------------------------------------
def disperse_death_reproducer(dead_individuals, individual_reproductive_status, individual_sex,
                              individual_group, individual_positions, individual_age, individual_dispersing,
                              individual_id, individual_dad, individual_mom, reproductive_age = 2,
                              max_agent_id = 0,
                              maximum_distance = 100000.0,
                              who_can_replace = 'any', patch_id_map = []):
    '''

    who_can_replace = any, same_patch
    '''

    # Initialize a count of number and distance of dispersals to be summed to the overall dispersal statistics
    dispersed = np.zeros(individual_id.shape, dtype = np.int8)
    distance_dispersed = np.zeros(individual_id.shape)
    
    # Initalize variables to be modified
    new_individual_reproductive_status = np.array(individual_reproductive_status)
    new_individual_group = np.array(individual_group)
    new_individual_positions = np.array(individual_positions)
    new_individual_dispersing = np.array(individual_dispersing)
    
    # Create variable max_id, that will be updated if new agents (dispering individuals) are created
    max_id = max_agent_id
    
    # ID of the new agents to be created representing dispersing individuals
    new_agents_IDs = np.empty(0, dtype = np.int64)
    
    # Check if any reproducer has died
    reproducer_died = (dead_individuals == 1) & (new_individual_reproductive_status == 1)
        
    # If no reproducer died, return a list with zeros 
    if np.all(reproducer_died == 0):
        pass
    
    # If any of the reproducers died
    else:
        # Get index of the dead individuals
        index_died = np.where(reproducer_died)[0]
                
        if who_can_replace == 'same_patch':
            
            # Get rows and cols from positions
            pos = new_individual_positions.astype(int)
            rows = pos[:,0]
            cols = pos[:,1]
            
            # Get individual pid from positions
            individual_pid = patch_id_map[rows,cols]
                
        # For each dead individual, check the sex and replace the reproducer(s)
        while len(index_died) > 0:
            
            # Initialize variables related to selecting one or two individuals to replace reproducers
            choose_one_reproducer = 0 # in case only 1 reproducer dies
            choose_two_reproducers = 0 # in case both reproducer die (or 1 die and the male disperse)
            
            # The focal individual is the first in the row
            i = index_died[0]
            
            # Remove individual i from the list of index_died
            index_died = index_died[index_died != i]
            
            # Get group of the dead individiual
            group_died = new_individual_group[i]
            # Get sex of the dead individual
            sex_died = individual_sex[i]
            
            if who_can_replace == 'same_patch':
                # Patch of the group of the individual who died
                pid_died = individual_pid[i]
            
            # Check who (the index) is the other reproducer of the group
            other_reprod = np.where((new_individual_group == group_died) & (individual_sex != sex_died) & (new_individual_reproductive_status == 1))
            
            # Check if the other reproducer is alive (it is not in the list of dead as 1)
            if dead_individuals[other_reprod] == 0:
                
                # If the dead individual is a male and the female reproducer is alive
                if sex_died == 0:
                
                    # The female reproducer keeps the same.
                    chosen1 = other_reprod # keep the index of the first reproducer
                    # We should search for a non-related male to the group.
                    choose_one_reproducer = 1 # we still need one reproducer
                    sex_reprod2 = 0 # a male is needed
                
                # If the dead individual is a female and the male reproducer is alive
                else:
                    
                    # Check if there is an alive female in the group, in reproductive age, which is not related 
                    # (mom, daughter, sibling) to the reproductive male
                    potential_females = np.where((new_individual_group == group_died) & (individual_sex == sex_died) & (individual_age >= reproductive_age) & (dead_individuals == 0) & # alive and on reprodutive age
                                                 (individual_id != individual_mom[other_reprod]) & # it is not mom
                                                 (individual_dad != individual_id[other_reprod]) & # it is not daughter
                                                 (individual_dad != individual_dad[other_reprod]) & # not siblings - dad
                                                 (individual_mom != individual_mom[other_reprod])) # not siblings - mom
                    
                    # If there is any female in this categories:
                    if potential_females[0].shape[0] > 0:
                        
                        # The male reproducer keeps the same.
                        chosen1 = other_reprod
                        # One of the potential females is randomly chosen as the new female reproducer of the group
                        chosen2 = np.random.choice(potential_females[0], 1)
                        # Change de reproductive status of this female to 1
                        new_individual_reproductive_status[chosen2] = 1
                        
                    # If there is no female in the group unrelated to the surviving reproductive male
                    else:
                        
                        # The male disperses and is not reproductive anymore; its group now is a new agent dispersing
                        new_individual_reproductive_status[other_reprod] = 0
                        new_individual_dispersing[other_reprod] = 1
                        new_individual_group[other_reprod] = max_id + 1
                        # Update max_id
                        max_id += 1
                        # Update new IDs of dispersing agents
                        new_agents_IDs = np.concatenate((new_agents_IDs, np.array([max_id])))

                        # New reproducers must be chosen
                        choose_two_reproducers = 1
                        
            # If the other reproducer is also dead - both died in the same time step
            else:
                
                if other_reprod[0].shape[0] > 0:
                
                    # Remove this individual from the list index_died
                    index_died = index_died[index_died != other_reprod[0]]
                    # New reproducers must be chosen
                    choose_two_reproducers = 1
                
            # If both reproducers died or the female died and the male dispersed,
            # two new reproducers must be chosen
            if choose_two_reproducers == 1:
                
                # Check individuals alive in the group, which are above the reproductive age (potential reproducers)
                alive_individuals_reprod = np.where((new_individual_group == group_died) & (dead_individuals == 0) & (individual_age > reproductive_age))
                
                # If the number of individuals above reproductive age is > 0, choose one them to be the first reproducer
                if alive_individuals_reprod[0].shape[0] > 0:
                    # Choose one of them randomly
                    chosen1 = np.random.choice(alive_individuals_reprod[0], 1)
                    # Change the reproductive status of this female to 1
                    new_individual_reproductive_status[chosen1] = 1
                    
                    # Now we should search for a non-related individual of the opposive sex the group.
                    choose_one_reproducer = 1 # we still need one reproducer
                    sex_reprod2 = np.where(individual_sex[chosen1] == 1, 0, 1)[0] # an individual of the opposite sex is needed                    
                    
                # If the number of individuals above reproductive < 1, check group size
                else:
                    
                    # Check individuals alive in the group
                    alive_individuals = np.where((new_individual_group == group_died) & (dead_individuals == 0))
                    
                    # If group size is > 0, individuals disperse and the group has gone extinct.
                    ################################################
                    ## I CAN STILL ADD INDIVIDUALS DIVIDING INTO GROUPS OF 1, 2 OR 3, BUT I DID NOT DO THAT NOW
                    if alive_individuals[0].shape[0] > 0:
                        # The individuals disperse to try joining a group; their group is now a new dispersing agent
                        new_individual_reproductive_status[alive_individuals] = 0
                        new_individual_dispersing[alive_individuals] = 1
                        new_individual_group[alive_individuals] = max_id + 1
                        # Update max_id
                        max_id += 1
                        # Update new IDs of dispersing agents
                        new_agents_IDs = np.concatenate((new_agents_IDs, np.array([max_id])))                        
                                                                  
                    # If group size is == 0, the group has just gone extinct!
            
            # If one of the reproducers is already decided, the other reproducer must be chosen            
            if choose_one_reproducer == 1:
                
                # List the potential second reproducers in the same group that are not related to the 
                # first reproducer (mom, daughter, sibling) 
                potential_second_reprod_group = np.where((new_individual_group == group_died) & (individual_sex == sex_reprod2) & # same group and sex of the reproducer 2
                                                         (individual_age >= reproductive_age) & (dead_individuals == 0) & # alive and on reprodutive age
                                                         (individual_id != individual_mom[chosen1]) & # it is not mom
                                                         (individual_id != individual_dad[chosen1]) & # it is not dad
                                                         (individual_dad != individual_id[chosen1]) & # it is not daughter
                                                         (individual_mom != individual_id[chosen1]) & # it is not daughter
                                                         (individual_dad != individual_dad[chosen1]) & # not siblings - dad
                                                         (individual_mom != individual_mom[chosen1])) # not siblings - mom
                                    
                # If there is any individual in this categories:
                if potential_second_reprod_group[0].shape[0] > 0:
                                        
                    # One of the potential individuals is randomly chosen as the second reproducer of the group
                    chosen2 = np.random.choice(potential_second_reprod_group[0], 1)
                    # Change de reproductive status of this individual to 1
                    new_individual_reproductive_status[chosen2] = 1
                                        
                # If there is no individual in the group unrelated to the first reproductive individual
                else:
                    
                    # Check index of individuals who are in the same patch as the first reproducer      
                    if who_can_replace == 'same_patch':
                        inds_same_patch = (individual_pid == pid_died)
                    # If who_can_replace == 'any', all individuals are here
                    else:
                        inds_same_patch = np.ones(individual_id.shape).astype(bool)
                        
                    # Check if there is an individual of the opposite sex, in the neighboring groups, 
                    # non-reproducer but in reproductive age, alive, to disperse and turn into reproducer in this group
                    potential_second_reprod_out_group = np.where((new_individual_group != group_died) & (individual_sex == sex_reprod2) & # same group and sex of the reproducer 2
                                                                 (individual_age >= reproductive_age) & (dead_individuals == 0) & # alive and on reprodutive age
                                                                 (new_individual_reproductive_status == 0) & (inds_same_patch)) # non-reproducer, it is in the same patch
                    
                    # Compute distance of individuals to the first reproducers' position
                    dists = np.linalg.norm(new_individual_positions[potential_second_reprod_out_group] - new_individual_positions[chosen1], axis=1)
                    
                    # Check potential dispersers who are not so far
                    close_potential_second_reprod = potential_second_reprod_out_group[0][dists < maximum_distance]
                    
                    # If there are at least one individual in other group which is close enough, 
                    # select one of them as the second reproducer
                    if close_potential_second_reprod.shape[0] > 0:
                        # Choose one of them randomly
                        chosen2 = np.random.choice(close_potential_second_reprod, 1)
                        # Quantify the dispersal times
                        dispersed[chosen2] += 1
                        # Quantify dispersal distance
                        distance_dispersed[chosen2] += np.linalg.norm(new_individual_positions[chosen2] - new_individual_positions[chosen1])
                        ### If other dispersal variables must be calculated, put them here.
                        
                        # Change the reproductive status of this individual to 1
                        new_individual_reproductive_status[chosen2] = 1
                        # Change the group of the individual
                        new_individual_group[chosen2] = new_individual_group[chosen1]
                        # Change the position of the individual
                        new_individual_positions[chosen2] = new_individual_positions[chosen1]
                        new_individual_dispersing[chosen2] = 0
                    
                    # If there are no individuals in other groups which are close enough, 
                    # the fate of the group is exctintion + dispersal or endogamy
                    else:
                        
                        # List the potential second reproducers in the same group, at reproductive age,
                        # now ignoring the relatedness
                        potential_endogamy = np.where((new_individual_group == group_died) & (individual_sex == sex_reprod2) & # same group and sex of the reproducer 2
                                                      (individual_age >= reproductive_age) & (dead_individuals == 0)) # alive and on reprodutive age
                        
                        # If there is any individual in this categories:
                        if potential_endogamy[0].shape[0] > 0:
                                                                
                            # One of the potential individuals is randomly chosen as the second reproducer of the group
                            chosen2 = np.random.choice(potential_endogamy[0], 1)
                            # Change de reproductive status of this individual to 1
                            new_individual_reproductive_status[chosen2] = 1   
                            ### here we could quantify the number of events of endogamy, if we wanted
                            
                        # If there are not, the group has gone exctint and the individuals disperse
                        else:
                             
                            # Check remaining individuals alive in the group
                            alive_individuals = np.where((new_individual_group == group_died) & (dead_individuals == 0))
                    
                            # If group size is > 0, individuals disperse and the group has gone extinct.
                            ################################################
                            ## I CAN STILL ADD INDIVIDUALS DIVIDING INTO GROUPS OF 1, 2 OR 3, BUT I DID NOT DO THAT NOW
                            if alive_individuals[0].shape[0] > 0:
                                # The individuals disperse to try joining a group; their group is now np.nan
                                new_individual_reproductive_status[alive_individuals] = 0
                                new_individual_dispersing[alive_individuals] = 1
                                new_individual_group[alive_individuals] = max_id + 1
                                # Update max_id
                                max_id += 1
                                # Update new IDs of dispersing agents
                                new_agents_IDs = np.concatenate((new_agents_IDs, np.array([max_id])))                                
                                                                  
                            # If group size is == 0, the group has just gone extinct!
                                
    return dispersed, distance_dispersed, new_individual_reproductive_status, new_individual_group, new_individual_positions, new_individual_dispersing, max_id, new_agents_IDs
                                    
            
        