# reproduction.py

import numpy as np
from populate import assign_sex
from genetics import reproduce_genetics

####### COLOCAR DISTRIBUICAO REAL!!
def sample_offspring_size(n_agents, offspring_size = [2], offspring_parameter = 'constant',
                   zero_offspring_possible = False):

    # Generate offspring size for all agents/females/groups 
    # (even if some of them will not reproduce successfully)
    # Later on these sizes are sampled for each agent

    # If offspring size is constant, generate array with these sizes
    if offspring_parameter == 'constant':

        # Checks if there is only one value
        if len(offspring_size) > 1:
            raise Exception('For constant offspring size, there must be only one size value. Please check it and retry.')

        # Takes the constant number of cubs
        const = offspring_size[0]

        # Checks if offspring size is positive
        # If it is negative, raise Error
        if const < 0:
            raise ValueError('Offspring size cannot be negative. Please check and retry.')
        # If offspring size is zero and zero offspring is not allowed, raise Error
        elif const == 0 and zero_offspring_possible == False:
            raise ValueError('Offspring size must be greater than zero. Please check and retry.')
        # If offspring size is positive or is zero and zero offspring is allowed
        else:
            # Round offspring size (in case it is float), generates array and return it
            return np.repeat(int(const), n_agents)

    # If the arguments are mean and sd of offspring size, and they follow a Gaussian distribution
    elif offspring_parameter == 'Gaussian':

        # Checks if there is only one value
        if len(offspring_size) != 2:
            raise Exception('For Gaussian sampling of offspring size, there must be exactly two values on offspring size array: mean and SD. Please check it and retry.')        

        #offspring_size = [5,2]
        # Mean of offspring size Gaussian distribution
        mu = offspring_size[0]
        # SD of offspring size Gaussian distribution
        sd = offspring_size[1]

        # Generate offspring size for each agent/group
        off_size_sample = np.random.normal(loc = mu, scale = sd, size = n_agents)

        # If zero is possible and there are numbers below zero, resample them
        if np.any(off_size_sample < 0) and zero_offspring_possible:
            # Create alternative offspring sizes and take only positive values
            alternative_off_size_sample = np.random.normal(loc = mu, scale = sd, size = n_agents * 50)
            alternative_off_size_sample = alternative_off_size_sample[alternative_off_size_sample > 0]

            # Then replace negative values for other positive samples from the same distribution
            try:    
                off_size_sample = np.where(off_size_sample < 0, alternative_off_size_sample[0:off_size_sample.shape[0]], off_size_sample)
            except:
                raise ValueError('There is some problem with your mean and scale values for offspring size. We could not generate enough positive values of offspring size.')

        # If zero is not possible and there are numbers below or equal 0.5 (that will be rounded to zero), resample them
        elif np.any(off_size_sample <= 0.5) and zero_offspring_possible == False:
            # Create alternative offspring sizes and take only values > 0.5
            alternative_off_size_sample = np.random.normal(loc = mu, scale = sd, size = n_agents * 50)
            alternative_off_size_sample = alternative_off_size_sample[alternative_off_size_sample > 0.5]            

            # Then replace negative/zero values for other positive samples from the same distribution
            try:    
                off_size_sample = np.where(off_size_sample <= 0.5, alternative_off_size_sample[0:off_size_sample.shape[0]], off_size_sample)
            except:
                raise ValueError('There is some problem with your mean and scale values for offspring size. We could not generate enough positive values of offspring size.')            

        return off_size_sample.round().astype(np.int)

    # If the arguments are mean and sd of offspring size, and they follow a Gaussian distribution
    elif offspring_parameter == 'Poisson':

        # Checks if there is only one value
        if len(offspring_size) > 1:
            raise Exception('For Poisson sampling of offspring size, there must be exactly one size value - the rate parameter of Poisson distribution. Please check it and retry.')

        #offspring_size = [5]
        # Rate of offspring size Poisson distribution (mean = 1/rate)
        rate = offspring_size[0]

        # Generate offspring size for each agent/group
        off_size_sample = np.random.poisson(lam = rate, size = n_agents)

        # If zero is not possible and there are numbers equal 0, resample them
        if np.any(off_size_sample < 1) and zero_offspring_possible == False:
            # Create alternative offspring sizes and take only values > 0
            alternative_off_size_sample = np.random.poisson(lam = rate, size = n_agents * 50)
            alternative_off_size_sample = alternative_off_size_sample[alternative_off_size_sample > 0]            

            # Then replace zero values for other positive samples from the same distribution
            try:    
                off_size_sample = np.where(off_size_sample < 1, alternative_off_size_sample[0:off_size_sample.shape[0]], off_size_sample)
            except:
                raise ValueError('There is some problem with your mean and scale values for offspring size. We could not generate enough positive values of offspring size.')            

        return off_size_sample

    else:
        # IMPLEMENT OTHER FUNCTIONS IF NECESSARY
        raise ValueError('Offspring parameter must be one of the following options: "constant", "Gaussian", or "Poisson".')


def reproduce(individual_id, individual_sex, individual_reproductive_status, simulation_step,
              group = False, individual_group = [], individual_positions = [], 
              set_genetics = False, individual_genetics = [],
              probability_female_reproduce = 1, offspring_size = [2],
              offspring_parameter = 'constant', zero_offspring_possible = False,
              sex_ratio = 0.5):
    
    # If group == True
    # (maybe we also need to create a condition for monogamy here)
    if group:
        #group_males, index_males = np.unique(individual_group, return_index=True)
        #group_females, index_females = (group_males, index_males+1)
        
        #index_males = individual_id[(individual_sex == 0) & (individual_reproductive_status == 1)]
        #index_females = individual_id[(individual_sex == 1) & (individual_reproductive_status == 1)]
        
        index_males = (individual_sex == 0) & (individual_reproductive_status == 1)
        index_females = (individual_sex == 1) & (individual_reproductive_status == 1)
                
        groups = np.unique(individual_group[index_males])
        
        groups_order_m = np.argsort(individual_group[index_males])
        index_males_sort = np.nonzero(index_males)[0][groups_order_m]
        #individual_id[index_males][groups_order_m]
        #group_id = individual_group[index_males][groups_order_m]
        group_id = individual_group[index_males_sort]
        
        groups_order_f = np.argsort(individual_group[index_females])
        #index_females_sort = index_females[groups_order_f]
        index_females_sort = np.nonzero(index_males)[0][groups_order_m]
        group_id_f = individual_group[index_females_sort] # just to check
        
        if not np.all(group_id == group_id_f):
            raise ValueError('The number of reproductive females and males in each group is not the same! Please check it.')
        else:
            # Sample which agents will reproduce, taking into account the probability of females to reproduce
            will_reproduce = np.where(np.random.random(group_id.shape) < probability_female_reproduce, True, False)
            
            # Select only the number of groups that reproduced
            groups_will_reproduce = group_id[will_reproduce]
            
            # Sample offspring size for each group
            off_size = sample_offspring_size(n_agents = groups_will_reproduce.shape[0], 
                                             offspring_size = offspring_size,
                                             offspring_parameter = offspring_parameter, 
                                             zero_offspring_possible = zero_offspring_possible)
            
            # Total number of cubs in all the populations
            total_new_inds = off_size.sum()
            
            # Individual ID - temporary
            # The true ID will be updated later when we check how many
            # individuals there were already created in the simulation
            new_inds_id = np.arange(1, total_new_inds+1)
            
            # Define group of each new individual
            new_inds_individual_group = np.repeat(groups_will_reproduce, off_size)
            # Define group where each new individual was born
            new_inds_individual_group_born = new_inds_individual_group
            # Define age of each new individual (1 time unit)
            new_inds_age = np.repeat(1, total_new_inds)
            # Define which individual is mom
            # individual_id[index_females_sort[will_reproduce]] = id of females that will reproduce
            new_inds_mom = np.repeat(individual_id[index_females_sort[will_reproduce]], off_size)
            # Define which individual is dad
            # individual_id[index_males_sort[will_reproduce]] = id of females that will reproduce
            new_inds_dad = np.repeat(individual_id[index_males_sort[will_reproduce]], off_size)
            
            # Define individual sex
            new_inds_sex = assign_sex(Na = total_new_inds, sex_ratio = sex_ratio)
            # Define whether individuals are alive (of course!)
            new_inds_alive = np.repeat(1, total_new_inds)
            # Define whether individuals are dispersing (no!)
            new_inds_dispersing = np.repeat(0, total_new_inds)
            # Define reproductive status (non reproductive!)
            new_inds_reproductive_status = np.repeat(0, total_new_inds)
            # Define positions (the same of the mom/dad group)
            # This is also the positions where the individuals were born - init_positions
            new_inds_positions = np.repeat(individual_positions[will_reproduce], off_size, axis = 0)
            
            # Define simulation step in which the individual was born
            new_inds_step_born = np.repeat(simulation_step, total_new_inds)
            
            # If genetics are being computed
            if set_genetics:
                # Define genetics of new individuals
                new_inds_genetics = reproduce_genetics(Nind = total_new_inds, individual_id = individual_id,
                                                       individual_genetics = individual_genetics, 
                                                       who_is_dad = new_inds_dad, who_is_mom = new_inds_mom)
            else:
                new_inds_genetics = None
                
            
            # Create dictionary with all the information
            var_names = ['off_size', 'total_new_inds', 'new_inds_id', 'new_inds_step_born',
                   'new_inds_individual_group', 'new_inds_mom', 'new_inds_dad', 'new_inds_age', 'new_inds_sex',
                   'new_inds_alive', 'new_inds_dispersing', 'new_inds_reproductive_status',
                   'new_inds_positions', 'new_inds_genetics']
            var = [off_size, total_new_inds, new_inds_id, new_inds_step_born,
                   new_inds_individual_group, new_inds_mom, new_inds_dad, new_inds_age, new_inds_sex,
                   new_inds_alive, new_inds_dispersing, new_inds_reproductive_status,
                   new_inds_positions, new_inds_genetics]
            new_inds = dict(zip(var_names, var))
            
            return new_inds
    
    # For individuals that do not live in groups, implement later
    else:
        raise ValueError('Reproduction for agents that do not live in groups must still be implemented!')
    
