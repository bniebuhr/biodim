# teste

def init():
    
    import os
    import numpy as np
    
    pydir = r'/home/leecb/Github/biodim/py'
    os.chdir(pydir)
    from class_animal import Animal, GLT
    from populate import group_size
    from landscape_modules import get_habitat_prop_cells
    
    animal = Animal('bird', 'bird')
    print animal.taxon
    print animal.group
    print animal.n_alelles
    
    animal.set_initial_conditions(Na = 50)
    print animal.Nind
    print animal.individual_id
    print animal.sex
    print animal.age
    print animal.reproductive_status
    
    animal2 = Animal('bird', 'flockbird', group = True)
    print animal2.taxon
    print animal2.functional_group
    print animal2.group
    
    animal2.set_initial_conditions(Na = 50)
    print animal2.agent_id
    print animal2.individual_id
    print animal2.init_group_sizes
    print animal2.sex
    print animal2.age
    print animal2.reproductive_status
    print animal2.alive
    print animal2.init_positions
    
    # Create a binary landscape map
    landscape_map = np.where(np.random.random((50,50)) > 0.5, 1, 0)
    
    # Get habitat cells
    pland, cells = get_habitat_prop_cells(landscape_map)
    pland
    cells
    
    glts = GLT()
    glts = GLT(include_reproduction = True, maximum_age=16 * 12)
    print glts.taxon
    print glts.group
    print glts.landscape_variables
    print glts.minimum_group_size
    print glts.maximum_age
    print glts.reproductive_condition
    
    group_size(Ngroups = 20, distribution = glts.dist_group_size, mu = 5.0, sd = 1.0, minimum = glts.minimum_group_size)
    
    glts.set_initial_conditions(Na = 1000, mean_age = 5 * 12, sex_ratio = 0.5,
                                populate_where = cells)
    print glts.agent_id
    print glts.individual_id
    print glts.init_group_sizes
    print glts.group_sizes
    print glts.sex
    print glts.individual_group
    
    print glts.Na
    print glts.dist_group_size
    
    print glts.age
    glts.age.mean()
    print glts.reproductive_status
    
    print glts.alive
    print glts.init_positions
    print glts.positions
    
    # Show landscape and positions
    import matplotlib.pyplot as plt
    
    plt.matshow(landscape_map, cmap = 'YlGn', 
                extent = (0,landscape_map.shape[1],landscape_map.shape[0],0)) 
    y, x = glts.init_positions.T
    plt.scatter(x, y, c = 'red')
    #plt.show()
    
    # Test mortality - constant
    glts.mortality()
    print glts.alive
    print glts.alive.shape
    print glts.dead
    print glts.dead_individual_id
    
    # Test dispersal after mortality of reproducer
    print glts.dead
    print (glts.dead) & (glts.reproductive_status) # check if there will be dispersal
    
    print glts.times_dispersed
    print glts.total_distance_dispersed
    
    glts.dispersal(after_death_reproducer = True, who_can_replace='any')
    
    print glts.times_dispersed
    print glts.total_distance_dispersed
    
    print glts.reproductive_status
    print glts.dispersing
    print glts.individual_group
    print glts.positions
    
    glts.dispersal(after_death_reproducer=False, disperse_regular=True, 
                  maximum_distance=8000.0, 
                  who_can_replace='same_patch', patch_id_map=[], 
                  ntries=50, nsteps=1, distribution="Weibull", 
                  scale=100.0, shape=2.0, landscape_map=landscape_map, 
                  landscape_values=[1])
    
    print glts.dispersing
    print glts.positions
    
    
    # Test update
    glts.update(current_step=1, update_mortality=True)
    
    print glts.alive
    print glts.alive.shape
    print glts.dead
    print glts.dead_individual_id
    print glts.dead_age
    
    print glts.init_Nind
    print glts.Nind
    print str(glts.init_Nind - glts.Nind)+' individuals died'
    
    # Test mortality - age dependent
    glts.mortality(mortality_rate=[0.05, 0.1], mortality_option='age_class', 
                  age_classes=[5,glts.maximum_age])
    
    print glts.alive
    print glts.alive.shape
    print glts.dead
    print glts.dead_individual_id
    
    # Test dispersal after mortality of reproducer
    print glts.dead
    print (glts.dead) & (glts.reproductive_status) # check if there will be dispersal
    
    # Test update
    glts.update(current_step=2, update_mortality=True)
    
    print glts.alive
    print glts.alive.shape
    print glts.dead
    print glts.dead_individual_id
    print glts.dead_age
    
    print glts.init_Nind
    print glts.Nind
    print str(glts.init_Nind - glts.Nind)+' individuals died'
    
    # test reproduction
    #glts.reproduction(simulation_step = 1, 
    #                  offspring_parameter='Poisson', offspring_size=[2])
    #glts.new_inds
    
    # Test update
    #glts.update(current_step = 1, update_reproduction = True)
    glts.age
    glts.sex
    glts.sex.shape[0]
    glts.Nind
    glts.Na
    glts.genetics