# BioDIM GLT

# Import modules
import numpy as np

# Import
from populate import populate_xy, assign_sex, assign_age_reproductive, group_size, populate_rowcol, define_home_range
from reproduction import reproduce
from genetics import initialize_genetics
from mortality import mortality_general
from dispersal import disperse_death_reproducer, choose_who_disperses, dispersal_step_selection_simple, settle

#------------------------------------------
# Class Animal
# 
# This is the main class for animals, which define a generic animal population dynamics
class Animal():
    
    #--------------------------------
    # Load general characteristics of the animal
    # Function __init__
    def __init__(self, taxon, functional_group, group = False,
                 landscape_variables = [],
                 include_mortality = True, maximum_age = 10 * 12,
                 include_reproduction = True, reproductive_age = 4 * 12, reproductive_condition = None,
                 dist_HR = 'Gaussian', min_homerange_size = 10, mean_homerange_size = 30, SD_homerange_size = 3,
                 include_dispersal = True, dispersal_age = 2 * 12,
                 include_genetics = True, n_loci = 5, n_alelles = [2]):
        '''
        Function __init__
        
        This function loads which kind of animal is being simulated and its general characteristics
        (those that do not depend on ecological context, time or simulation). This characteristics are
        generally related to a species or functional group.
        
        Input:
        - 
        
        Output:
        '''
        
        # Taxon
        self.taxon = taxon
        # Functional Group
        self.functional_group = functional_group
        
        # Landscape variables to be used for the species profile
        self.landscape_variables = landscape_variables

        # Space use
        self.min_homerange_size = min_homerange_size
        self.mean_homerange_size = mean_homerange_size
        self.SD_homerange_size = SD_homerange_size
        self.distribution_HR = dist_HR
        
        # Daily movement
        
        # Dispersal
        self.include_dispersal = include_dispersal
        self.dispersal_age = dispersal_age

        # Do agents represent groups?
        self.group = group
        
        # Mortality
        self.include_mortality = include_mortality # If False, mortality is not included in the simulations
        self.maximum_age = maximum_age
        
        # Reproduction
        self.include_reproduction = include_reproduction # If False, reproduction is not included in the simulations
        self.reproductive_age = reproductive_age
        self.reproductive_condition = reproductive_condition
        
        # Genetics
        self.include_genetics = include_genetics # If False, reproduction is not included in the simulations
        self.n_loci = n_loci
        self.n_alelles = n_alelles
        
    #--------------------------------
    # Initial conditions
    # Function set_initial_conditions
    def set_initial_conditions(self, Na = 30, 
                               dist_group_size = "Gaussian", mu_group_size = 5.0, sd_group_size = 1.0, minimum_group_size = 2,
                               sex_ratio = 0.5,
                               mean_age = 5 * 12, sd_age = 2 * 12,
                               populate_where = None, condition_populate = 'habitat', populate_replace = False):
        '''
        Function set_initial_conditions
        
        This function initializes the state variables for agents/individuals to be simulated.
        
        Input:
        Na: integer; number of agents to be created.
        dist_group_size: string; distribution to be used for group size if agents represent groups (self.group == True).
            The options are 'Gaussian' (default), 'Possion', 'Empiric' (real data), or other implemented in the function group_size.
            If self.group == False, this variable is ignored.
        mu_group_size: positive float; expected (mean) number of individuals per group in the beginning of the simulation
            if agents represent groups (self.group == True). This variable is an argument to the function group_size.
            If self.group == False, this variable is ignored.
        sd_group_size: positive float; standard deviation of the group size in the beginning of the simulation
            if agents represent groups (self.group == True). This variable is an argument to the function group_size.
            If self.group == False, this variable is ignored.
        minimum_group_size: positive integer; minimum group size in the beginning of the simulation
            if agents represent groups (self.group == True). This variable is an argument to the function group_size.
            If self.group == False, this variable is ignored.
        sex_ratio: float between 0 and 1; probability of an individual be assigned as a female in the beginning of the simulation.
        mean_age: positive float; expected (mean) age of individuals in the beginning of the simulation.
        sd_age: positive float; standard deviation of the age of individuals in the beginning of the simulation.
        populate_where: array of integers with the coordinates [row, col] of cells in the landscape where individuals may start the simulation.
        condition_populate: string; condition specifying where individuals may be placed 
            (e.g. only in habitat, only in some patches, any). This defines the form the variable population_where must take.
        populate_replace: logical (True/False); whether two agents can (cannot) inhabit the same cell in the beginning of the simulation.
        
        Output:
        No values are returned. However, the following variables are created 
        as characteristics of the animal instance:
        - init_Na: number of agents in the beginning of the simulation.
        - Na: number of agents (changes along time).
        - agent_id: array with agent id. ### Check if it is worth it to keep both agent id, group id, and individual id
        - init_Nind: number of individuals in the beginning of the simulation (= init_Na if agents are not groups).
        - Nind: number of individuals (change along time) (= Na if agents are not groups).
        - individual_id: array with individual id (= agent_Na if agents are not groups).
        - init_group_sizes: array with the number of individuals per group in the beginning of the simulation (created only if agents represent groups).
        - group_sizes: array with the number of individuals per group (changes along time) (created only if agents represent groups).
        - init_individual_group: array with the number of the group each individual is part of (= None if agents are not groups)
            in the beginning of the simulation.
            For individuals that are born during the simulation, this also represents the natal group.
        - individual_group: array with the number of the group each individual is part of (= None if agents are not groups).
        - alive: array indicating whether individuals are alive (1) or not (0). ### maybe this may be removed...
        - dad: array indicating the id of the individual who is the dead of each individual/agent. 
            For individual in the beginning the simulation, this information is unknown, then NaN is recorded.
        - mom: array indicating the id of the individual who is the dead of each individual/agent. 
            For individual in the beginning the simulation, this information is unknown, then NaN is recorded.
        - step_born: array indicating in which step individuals were born (= 0 for individuals created in the beginning 
            of the simulation, although they were born before that).
        - dispersing: array indicating whether individuals are dispersing (1) or not (0).
        - sex: array with sex of individuals (1 = female, 0 = male).
        - age: array with floats, the age of individuals.
        - reproductive_status: array with reproductive status of individuals (1 = reproducive, 0 = non-reproductive).
            If self.include_reproduction == False, reproduction is not included in the simulations and this variable is initialized as None.
        - init_positions: array with floats representing the positions [row, col] of agents/individuals in the beginning of the simulation.
            For individuals that are born during the simulation, this represents also the born place.
        - positions: array with floats representing the positions [row, col] of agents/individuals (changes along time).
        
        If genetics are included in the simulation, then individuals also have the variables:
        - genetics: array with the genetics structure of each individual (with dimensions (Nind, number_genetics_strains, number_of_loci)).
        
        If mortality is included in the simulation, then the following variables are also initialized
        (empty) to save the state variables of individuals that diw along the simulation:
        - dead: array indicating if an alive individual dies in a given step (1 = died, 0 = keep alive).
            The array id reinitialized as an array of zeros in the end of every step.
        - dead_individual_id: id of the individuals that die.
        - dead_dispersing: whether the individuals were dispersing when died (1 = dispersing, 0 = not dispersing).
        - dead_sex: sex of the dead individual (1 = female, 0 = male).
        - dead_age: age of the individuals had when they died.
        - dead_reproductive_status: reproductive status of the individuals when they died.
        - dead_positions: position of the individuals when they died.
        - dead_step: simulation step individuals when they died.
        - dead_genetics: genetics of dead individuals (if genetics is included).
        - dead_group_id: id of the group individuals were part of when they died (if self.group == True).
        - dead_times_dispersed: number of times the individual dispersed.
        
        The following variables are not being updated along simulation steps (but may be):
        - init_group_sizes
        - group_sizes (they are not used in other functions... but may be important)
        '''
        
        self.init_Na = Na # Number of agents at the beginning of the simulation
        self.Na = Na  # Number of agents (changes along time)
        self.agent_id = np.arange(Na) # Agent id
                
        # Define number of individuals and individual id (and group size if group == True)
        if self.group:
            # Number of individuals, group size at the beginning of the simulation
            self.init_Nind, self.init_group_sizes = group_size(Ngroups = self.Na, distribution = dist_group_size, 
                                                                  mu = mu_group_size, sd = sd_group_size, minimum = minimum_group_size)
            self.Nind = self.init_Nind # Number of individuals (to change along the simulations)
            self.group_sizes = self.init_group_sizes # To change along the simulations
            
            # The group of each individual
            self.init_individual_group = np.repeat(self.agent_id, self.init_group_sizes) # Group number for each individual, at the beginning of the simulation
            self.individual_group = self.init_individual_group # Group number for each individual, to change along the simulations
            
            # Number of groups
            self.Ngroups = self.Na
            
            # Max agent_ID of an agent created
            self.max_agent_ID = self.agent_id.max()
            
            # If mortality will be included
            if self.include_mortality:
                # Initialize arrays to record information of dead individuals
                self.dead_group_id = np.empty(0, dtype=np.int32)
                self.dead_init_individual_group = np.empty(0, dtype=np.int32)
            
        else:
            # Number of individuals
            self.init_Nind = Na # At the beginning of the simulation
            self.Nind = Na # To change along the simulations
            
            # For non-group agents, this variable does not make sense. We just use it for assigning sex
            self.init_group_sizes = None
            
            # Initialize arrays to record information of dead individuals
            if self.include_mortality:
                self.dead_group_id = None
            
        # Individual ID
        self.individual_id = np.arange(self.Nind)
            
        # Whether individuals are alive
        self.alive = np.ones(self.Nind, dtype=np.int8)
        
        # Dad and mom of individuals (unknown in the beginning of the simulation)
        self.dad = np.empty(self.Nind)
        self.dad.fill(np.nan)
        self.mom = np.empty(self.Nind)
        self.mom.fill(np.nan)
        
        # Step when was born (=0; they were created in the beginning of the simulation)
        self.step_born = np.zeros(self.Nind)
        
        # Home range of each agent - initial and to be updated at each step
        self.init_home_range = define_home_range(self.Na, distribution = self.distribution_HR, 
                                                 minimum_HRsize = self.min_homerange_size, 
                                                 mean_HRsize = self.mean_homerange_size, SD_HRsize = self.SD_homerange_size)
        self.home_range = self.init_home_range
        
        # Whether individuals are dispersing
        self.dispersing = np.zeros(self.Nind, dtype=np.int8)

        # If include_dispersal == True, initialize variables that account for dispersal
        if self.include_dispersal:        
            # Number of times individuals dispersed
            self.times_dispersed = np.zeros(self.Nind, dtype=np.int16)
            # Total distance dispersed
            self.total_distance_dispersed = np.zeros(self.Nind)
        
        # Define individual sex  
        self.sex = assign_sex(Na = self.Na, sex_ratio = sex_ratio, 
                              group = self.group, group_sizes = self.init_group_sizes, 
                              condition = self.reproductive_condition)
        
        # Define individual age
        self.age, self.reproductive_status = assign_age_reproductive(Na = self.Na, mean_age = mean_age, sd_age = sd_age, maximum_age = self.maximum_age, 
                                                                     set_reproductive = self.include_reproduction, reproductive_age = self.reproductive_age, 
                                                                     group = self.group, group_sizes = self.init_group_sizes, condition = self.reproductive_condition)
        
        # Define agents initial positions
        self.init_positions = populate_rowcol(self.Na, where = populate_where, 
                                              condition_populate = condition_populate, replace = populate_replace,
                                              group = self.group, group_sizes = self.init_group_sizes)
        self.positions = self.init_positions
        
        # If include_reproduction == True, define new_inds for reproduction:
        if self.include_reproduction:
            # Initializes new_inds as an empty dictionary
            self.new_inds = {}            
        
        # Define initial genetics
        if self.include_genetics:
            self.genetics = initialize_genetics(self.Nind, n_loci = self.n_loci, n_alelles = self.n_alelles)        
        
        # If mortality will be included, initialize arrays of dead individuals and their characteristics
        if self.include_mortality:
            self.dead = np.zeros(self.Nind, dtype=np.int8)
        
            # Initialize arrays to record information of dead individuals
            self.dead_individual_id = np.empty(0, dtype=np.int32)
            self.dead_sex = np.empty(0, dtype=np.int8)
            self.dead_age = np.empty(0, dtype=np.int32)
            self.dead_reproductive_status = np.empty(0, dtype=np.int8)
            self.dead_positions = np.empty((0,2))
            self.dead_step = np.empty(0, dtype=np.int32)
            
            self.dead_dad = np.empty(0, dtype=np.int32)
            self.dead_mom = np.empty(0, dtype=np.int32)
            self.dead_step_born = np.empty(0, dtype=np.int32)
            self.dead_init_positions = np.empty((0,2))        
            
            # If include_dispersal == True
            if self.include_dispersal:
                self.dead_dispersing = np.empty(0, dtype=np.int8)
                self.dead_times_dispersed = np.empty(0, dtype=np.int32)
                self.dead_total_distance_dispersed = np.empty(0)
                
            # If include_genetics == True
            if self.include_genetics:
                shape_genetics = self.genetics.shape # Taking the shape of genetic structure
                self.dead_genetics = np.empty((0, shape_genetics[1], shape_genetics[2]), dtype=np.int16)
    
    #--------------------------------
    # Mortality
    # Function mortality
    def mortality(self, mortality_rate = [0.05], mortality_option = 'constant',
                  age_classes = [], habitat_types = []):
        '''
        Function mortality
        
        This function assess if each individual/agent alive will die or remain alive, given the mortality rates.
        
        Input:
        - mortality_rate: list with float values; single value if mortality is constant, or several values for 
            different habitats/matrices or different age classes, for instance. 
            Mortality rate must be parameterized given the time unit in the simulations.
        - mortality_option: string; the way mortality will be considered. It may be 'constant' (default), 'age_class', 'habitat_type', or other.
        - age_classes: array with floats, representing the above age of each age class; it is only taken into account if mortality_option == 'age_class'.
            It makes sense if the age of the last class is the maximum age for agents (you can choose a large number if this is not relevant).
            E.g.: age_classes = [1,2,4,10] indicates the age classes 0-1, 1-2, 2-4, 4-10, 10 being the maximum age possible
            (otherwise the mortality function does not work for these individuals).
        - habitat_types: array with floats, representing the above age of each habitat type in the landscape; 
            it is only taken into account if mortality_option == 'habitat_type'.
            
        Output:
        No output. 
        This function updates the variable self.dead, a list with individuals that died in a given step.
        '''
        
        if self.include_mortality:
            # Define which individuals died 
            dead_by_mortality = mortality_general(individuals_alive = self.alive, 
                                                  include_mortality = self.include_mortality, mortality_rate = mortality_rate,
                                                  mortality_option = mortality_option, individuals_age = self.age, 
                                                  age_classes = age_classes, habitat_types = habitat_types)
            np.minimum(self.dead + dead_by_mortality, 1, out=self.dead)
    
    #--------------------------------
    # Reproduction
    # Function reproduction
    def reproduction(self, simulation_step, probability_female_reproduce = 1, offspring_size = [2],
                     offspring_parameter = 'constant', zero_offspring_possible = False,
                     sex_ratio = 0.5):
        '''
        Function reproduction
        
        This function produces new individuals and their characteristics, given the reproductive 
        individuals that are alive and the reproductive parameters.
        
        Input:
        
        
        Output:
        '''
        
        if self.include_reproduction:
            self.new_inds = reproduce(individual_id = self.individual_id, individual_sex = self.sex, 
                                      individual_reproductive_status = self.reproductive_status, 
                                      simulation_step = simulation_step, 
                                      group = self.group, individual_group = self.individual_group, 
                                      individual_positions = self.positions, 
                                      set_genetics = self.include_genetics, individual_genetics = self.genetics, 
                                      probability_female_reproduce = probability_female_reproduce, 
                                      offspring_size = offspring_size, offspring_parameter = offspring_parameter, 
                                      zero_offspring_possible = zero_offspring_possible, sex_ratio = sex_ratio)
    
    
    #--------------------------------
    # Dispersal
    # Function dispersal
    def dispersal(self, after_death_reproducer = False, disperse_regular = False, to_settle = False,
                  maximum_distance = 8000.0, who_can_replace = 'any', patch_id_map = [], patch_area_map = [],
                  p_disperse = 0.05, reproductive_can_disperse = False,
                  p_enter_group = 0.1, 
                  ntries = 50, nsteps = 1, 
                  distribution = "Weibull", scale = 100.0, shape = 2.0,                  
                  landscape_map = [], landscape_values = [1]):
        
        '''
        Function dispersal
        
        Variables related to dispersal are already updated here, not in the update method
        '''
        
        if self.include_dispersal:
        
            # If we are considering common dispersal
            if disperse_regular:
                
                # Choose individuals which will disperse
                self.dispersing = choose_who_disperses(p_disperse = p_disperse, individual_dispersing = self.dispersing,
                                                       dead_individuals = self.dead,
                                                       individual_age = self.age, dispersal_age = self.dispersal_age, 
                                                       reproductive_can_disperse = reproductive_can_disperse, 
                                                       individual_reproductive_status = self.reproductive_status)
                
                # Disperse
                new_dispersed, new_distance_dispersed, new_individual_positions, new_dead_individuals, new_individual_group, new_max_id, new_agents_IDs = dispersal_step_selection_simple(
                    individuals_dispersing = self.dispersing, 
                    individual_positions = self.positions, 
                    dead_individuals = self.dead, 
                    individual_group = self.individual_group,
                    max_agent_id = self.max_agent_ID,
                    ntries = ntries, nsteps = nsteps, 
                    distribution = distribution, scale = scale, shape = shape, 
                    landscape_map = landscape_map, landscape_values = landscape_values)    
                
                # Update times and distance dispersed per individual
                self.times_dispersed += new_dispersed
                self.total_distance_dispersed += new_distance_dispersed
                            
                # Update population variables
                self.positions = new_individual_positions
                self.dead = new_dead_individuals 
                self.individual_group = new_individual_group
                
                # Update maximum agent ID
                self.max_agent_ID = new_max_id
                
                # Update agent IDs and homeranges (np.nan for agents dispersing)
                self.agent_id = np.concatenate((self.agent_id, new_agents_IDs))
                self.home_range = np.concatenate((self.home_range, np.repeat(np.nan, repeats = new_agents_IDs.shape[0])))
                
            # If we are considering settlement
            if to_settle:
                
                new_individuals_dispersing, new_individual_group, new_individual_positions, new_dead_individuals, new_individual_reproductive_status, new_home_range_sizes = settle(
                    individuals_dispersing = self.dispersing, individual_group = self.individual_group, 
                    individual_positions = self.positions, dead_individuals = self.dead,
                    individual_reproductive_status = self.reproductive_status, 
                    individual_sex = self.sex, 
                    agent_id = self.agent_id, home_range_sizes = self.home_range, 
                    distribution_HR = self.distribution_HR, mean_HRsize = self.mean_homerange_size, 
                    min_HRsize = self.min_homerange_size, SD_HRsize = self.SD_homerange_size, 
                    maximum_distance = maximum_distance, p_enter_group = p_enter_group,
                    who_can_mate = who_can_replace, landscape_map = landscape_map, patch_id_map = patch_id_map,
                    patch_area_map = patch_area_map)
                
                # Update population variables
                self.dispersing = new_individuals_dispersing
                self.individual_group = new_individual_group
                self.positions = new_individual_positions
                self.dead = new_dead_individuals
                self.reproductive_status = new_individual_reproductive_status
                
                # Update homerange of new individuals who dispersed and settled
                self.home_range = new_home_range_sizes                
    
    #--------------------------------
    # Updating individual state variables
    # Function update
    def update(self, current_step = -1, update_mortality = False, update_reproduction = False, 
               update_movement = False, update_dispersal = False,
               next_step = False):
        '''
        Function update
        
        This function updates the individuals and their state variables after events of mortality,
        movement, dispersal, and reproduction (or other) occur.
        
        Input:
        - current_step: integer; the current step of the simulation.
        - update_mortality: 
        - update_reproduction
        - update_movement
        - update_dispersal
        - update_other_vars:
        
        Output:
        
        '''
        
        # Update mortality
        if update_mortality and self.include_mortality and self.Nind > 0:
            # Update individuals alive
            died = self.dead.astype(bool)
            
            # Update id of individuals alive and dead
            self.dead_individual_id = np.concatenate((self.dead_individual_id, self.individual_id[died])) # Add new dead individual id to the list of dead's ids
            self.individual_id = self.individual_id[~died] # keep only individuals that remain alive
            
            # Update info of individuals dispersing
            self.dead_dispersing = np.concatenate((self.dead_dispersing, self.dispersing[died])) # Add new dead individual dispersal info to the list of dead's dispersal
            self.dispersing = self.dispersing[~died] # keep only individuals that remain alive            
            
            # If dispersal is considered:
            if self.include_dispersal:
                # Update info of times individuals dispersed
                self.dead_times_dispersed = np.concatenate((self.dead_times_dispersed, self.times_dispersed[died]))
                self.times_dispersed = self.times_dispersed[~died]           
                
                # Update info of total distance dispersed by individuals
                self.dead_total_distance_dispersed = np.concatenate((self.dead_total_distance_dispersed, self.total_distance_dispersed[died]))
                self.total_distance_dispersed = self.total_distance_dispersed[~died]                           
            
            # Update sex of dead individuals
            self.dead_sex = np.concatenate((self.dead_sex, self.sex[died]))
            self.sex = self.sex[~died]
            
            # Update age of dead individuals
            self.dead_age = np.concatenate((self.dead_age, self.age[died]))
            self.age = self.age[~died]
            
            # Update reproductive status of dead individuals
            self.dead_reproductive_status = np.concatenate((self.dead_reproductive_status, self.reproductive_status[died]))
            self.reproductive_status = self.reproductive_status[~died]
                        
            # Update positions of dead individuals, and their initial position
            self.dead_positions = np.concatenate((self.dead_positions, self.positions[died]))
            self.positions = self.positions[~died]
            
            self.dead_init_positions = np.concatenate((self.dead_init_positions, self.init_positions[died]))
            self.init_positions = self.init_positions[~died]
            
            # Update step in which animals died, and step in which animals were born
            self.dead_step = np.concatenate((self.dead_step, np.repeat(current_step, died.sum())))
            
            self.dead_step_born = np.concatenate((self.dead_step_born, self.step_born[died]))
            self.step_born = self.step_born[~died]
            
            # Update list of dad and mom, considering dead and live individuals
            self.dead_dad = np.concatenate((self.dead_dad, self.dad[died]))
            self.dad = self.dad[~died]
            
            self.dead_mom = np.concatenate((self.dead_mom, self.mom[died]))
            self.mom = self.mom[~died]
            
            # Update individuals alive
            self.alive = self.alive[~died]
        
            # Update other variables
            self.Nind = self.alive.sum()
                        
            # Update group id (if self.group == True), agent id, and Na
            if self.group:
                self.dead_group_id = np.concatenate((self.dead_group_id, self.individual_group[died]))
                self.individual_group = self.individual_group[~died]
                
                self.dead_init_individual_group = np.concatenate((self.dead_init_individual_group, self.init_individual_group[died]))
                self.init_individual_group = self.init_individual_group[~died]
                
                # Get the id of the agents, number of agents, id of groups, and number of groups
                
                # Agents that are still present
                remaining_agents = np.unique(self.individual_group)
                # Agents that did not desapeared (groups extinct, dispering individuals that entered a group)
                agents_alive = np.in1d(self.agent_id, remaining_agents)
                # Index of agents alive
                index_agents_alive = np.where(agents_alive == True)
                # New array of agent IDs
                self.agent_id = self.agent_id[index_agents_alive]
                
                # Number of agents
                self.Na = self.agent_id.shape[0]
                
                # Group sizes
                if self.Na > 0:
                    self.group_sizes, bins = np.histogram(self.individual_group, bins = np.concatenate((self.agent_id, np.array([self.agent_id.max()+1]))))
                
                # Home ranges - take only the values for individuals alive
                self.home_range = self.home_range[index_agents_alive]
                
                # Get the id of groups, and number of groups
                # Number of groups = Number of agents that are not dispersing
                # Dispersing individual have home range == np.nan, which is not finite
                #self.Ngroups = self.agent_id[~np.isnan(self.home_range)].shape[0]
                self.Ngroups = self.agent_id[np.isfinite(self.home_range)].shape[0]
            
            # If self.group == False (agents are not groups)
            else:
                self.Na = self.Nind
                self.agent_id = self.individual_id
            
            # Update genetics
            if self.include_genetics:
                self.dead_genetics = np.concatenate((self.dead_genetics, self.genetics[died]))
                self.genetics = self.genetics[~died]
            
            # Re-initialize number of dead individuals = 0 for the following step
            self.dead = np.zeros(self.Nind, dtype=np.int8)
            
        # Update reproduction
        if update_reproduction and self.include_reproduction:
            
            # Update individuals alive
            self.alive = np.concatenate((self.alive, self.new_inds['new_inds_alive']))
                        
            # Update id of individuals alive
            ids = self.new_inds['new_inds_id'] + self.Nind + self.dead_individual_id.shape[0]
            self.individual_id = np.concatenate((self.individual_id, ids))
            
            # Update info of individuals dispersing
            self.dispersing = np.concatenate((self.dispersing, self.new_inds['new_inds_dispersing']))

            # If dispersal is considered:
            if self.include_dispersal:
                # Update info of times individuals dispersed
                self.times_dispersed = np.concatenate((self.times_dispersed, np.repeat(0, self.new_inds['new_inds_dispersing'].shape[0])))
                
                # Update info of total distance dispersed by individuals
                self.total_distance_dispersed = np.concatenate((self.total_distance_dispersed, np.repeat(0.0, self.new_inds['new_inds_dispersing'].shape[0])))
            
            # Update sex of individuals
            self.sex = np.concatenate((self.sex, self.new_inds['new_inds_sex']))
            
            # Update age of individuals
            self.age = np.concatenate((self.age, self.new_inds['new_inds_age']))
            
            # Update reproductive status of individuals
            self.reproductive_status = np.concatenate((self.reproductive_status, 
                                                       self.new_inds['new_inds_reproductive_status']))
                        
            # Update positions of individuals
            self.positions = np.concatenate((self.positions, self.new_inds['new_inds_positions']))
            
            # Update initial positions
            self.init_positions = np.concatenate((self.init_positions, self.new_inds['new_inds_positions']))            
            
            # Update step in which animals died
            self.step_born = np.concatenate((self.step_born, self.new_inds['new_inds_step_born']))
            
            # Update individual mom and dad
            self.mom = np.concatenate((self.mom, self.new_inds['new_inds_mom']))
            self.dad = np.concatenate((self.dad, self.new_inds['new_inds_dad']))
            
            # Update other variables
            self.Nind = self.alive.sum()            
            
            # Update group id, initial group_id (if self.group == True), agent id, and Na
            if self.group:
                self.individual_group = np.concatenate((self.individual_group, self.new_inds['new_inds_individual_group']))
                self.init_individual_group = np.concatenate((self.init_individual_group, self.new_inds['new_inds_individual_group']))
                
                # Id and number of agents, number of groups, and group home range
                # do not change when the new individuals keep within the groups
                
                # Group sizes
                self.group_sizes, bins = np.histogram(self.individual_group, bins = np.concatenate((self.agent_id, np.array([self.agent_id.max()+1]))))
                
                ################
                # Record the indexes of the groups alive/dead?
                # Include it in the set_init_conditions?         
            
            # If self.group == False (agents are not groups)    
            else:
                self.Na = self.Nind
                self.agent_id = self.individual_id
            
            # Update genetics
            if self.include_genetics: 
                self.genetics = np.concatenate((self.genetics, self.new_inds['new_inds_genetics']))                        
            
            # Re-initialize number of dead individuals = 0 for the following step
            self.dead = np.zeros(self.Nind, dtype=np.int8)            
            
            # Reinitializes new_inds as an empty dictionary
            self.new_inds = {}           
            
        # Update other vars before the next step
        if next_step:
            
            # Update age
            self.age = self.age + 1



class GLT(Animal):
    
    # Load general characteristics of the animal
    def __init__(self, minimum_group_size = 2, 
                 group = True, landscape_variables = ['pid', 'patch_area'], 
                 maximum_age = 16 * 12, reproductive_age = 4 * 12, reproductive_condition = 'monogamy',
                 n_loci = 14, n_alelles = [9,10,9,3,8,3,4,9,4,8,6,6,8,6], 
                 **kwargs):
        
        # we put explicitly here values for the variables that cannot change. 
        # The other values are up on the __init__ call.
        Animal.__init__(self, taxon = 'GoldenLionTamarin', functional_group = 'GoldenLionTamarin', 
                        group = group, landscape_variables = landscape_variables, 
                        maximum_age = maximum_age, reproductive_age = reproductive_age, 
                        reproductive_condition = reproductive_condition, 
                        n_loci = n_loci, n_alelles = n_alelles, **kwargs)
        
        # Minimum, mean, and SD, and distribution for group size
        self.minimum_group_size = minimum_group_size
        self.mean_group_size = 5.0
        self.sd_group_size = 1.0
        self.dist_group_size = 'Poisson'
    
    #--------------------------------
    # Initializing the simulation environment
    # Function set_initial_conditions
    def set_initial_conditions(self, Na, **kwargs):
                
        Animal.set_initial_conditions(self, Na,  
                                      dist_group_size=self.dist_group_size, mu_group_size=self.mean_group_size, sd_group_size=self.sd_group_size,
                                      minimum_group_size=self.minimum_group_size, **kwargs) 

    def mortality(self, mortality_rate = [0.05], mortality_option = 'constant',
                 age_classes = [16], habitat_types=[]):
        
        Animal.mortality(self, mortality_rate = mortality_rate, mortality_option = mortality_option, 
                        age_classes = age_classes, habitat_types = habitat_types)
    
    # Method reproduction not defined, inherited as it is from class Animal  
    
    #--------------------------------
    # Dispersal
    # Function dispersal    
    def dispersal(self, after_death_reproducer = False, disperse_regular = False, to_settle = False,
                  maximum_distance = 8000.0, who_can_replace = 'same_patch', 
                  patch_id_map = [], patch_area_map = [],
                  p_disperse = 0.05, reproductive_can_disperse = False,
                  p_enter_group = 0.15, 
                  ntries = 50, nsteps = 1, 
                  distribution = "Weibull", scale = 500.0, shape = 2.0,                  
                  landscape_map = [], landscape_values = [1], **kwargs):
        
        # If the dispersal follows the death of reproducers, make the individuals disperse!
        if after_death_reproducer:
            
            new_dispersed, new_distance_dispersed, new_individual_reproductive_status, new_individual_group, new_individual_positions, new_individual_dispersing, new_max_id, new_agents_IDs = disperse_death_reproducer(
                dead_individuals = self.dead, 
                individual_reproductive_status = self.reproductive_status, 
                individual_sex = self.sex, 
                individual_group = self.individual_group, 
                individual_positions = self.positions, 
                individual_age = self.age, 
                individual_dispersing = self.dispersing, 
                individual_id = self.individual_id, 
                individual_dad = self.dad, 
                individual_mom = self.mom, 
                reproductive_age = self.reproductive_age,
                max_agent_id = self.max_agent_ID,
                maximum_distance = maximum_distance, 
                who_can_replace = who_can_replace, 
                patch_id_map = patch_id_map)
            
            # Update times and distance dispersed per individual
            self.times_dispersed += new_dispersed
            self.total_distance_dispersed += new_distance_dispersed
            
            # Update population variables
            self.reproductive_status = new_individual_reproductive_status
            self.individual_group = new_individual_group
            self.positions = new_individual_positions
            self.dispersing = new_individual_dispersing
            
            # Update maximum agent ID
            self.max_agent_ID = new_max_id
            
            # Update agent IDs and homeranges (np.nan for agents dispersing)
            self.agent_id = np.concatenate((self.agent_id, new_agents_IDs))
            self.home_range = np.concatenate((self.home_range, np.repeat(np.nan, repeats = new_agents_IDs.shape[0])))
            
        Animal.dispersal(self, after_death_reproducer = after_death_reproducer, 
                         disperse_regular = disperse_regular, to_settle = to_settle,
                         maximum_distance = maximum_distance, who_can_replace = who_can_replace, 
                         patch_id_map = patch_id_map, patch_area_map = patch_area_map,
                         p_disperse = p_disperse, reproductive_can_disperse = reproductive_can_disperse,
                         p_enter_group = p_enter_group,
                         ntries = ntries, nsteps = nsteps, 
                         distribution = distribution, scale = scale, shape = shape, 
                         landscape_map = landscape_map, landscape_values = landscape_values, **kwargs)
    
    # Method update not defined, inherited as it is from class Animal    
    #def update(self, current_step=-1, update_mortality=False, 
              #update_reproduction=False, update_movement=False, 
              #update_dispersal=False, update_other_vars=False):
        
        
