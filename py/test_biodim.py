#----------------------------------
# test list_landscapes_habitat

python

import os
import grass.script as grass

pydir = r'/home/leecb/Github/biodim/py'
os.chdir(pydir)
from landscape_modules import list_landscapes_habitat

# Test for random landscapes
list_landscapes_habitat(use_random_landscapes = True, habmat_pattern = '*HABMAT')

# Test for real landscapes
list_landscapes_habitat(use_random_landscapes = False, habmat_pattern = '*HABMAT')

#----------------------------------
# test list_landscape_variables

python

import os
import grass.script as grass

pydir = r'/home/leecb/Github/biodim/py'
os.chdir(pydir)
from landscape_modules import list_landscape_variables

# Test for random landscapes
var = ['edge_dist', 'pid', 'patch_area']

landscape_vars, var_types, list_mapsets = list_landscape_variables(use_random_landscapes = True, variables = var)
landscape_vars['edge_dist']
landscape_vars[var[1]]
landscape_vars['patch_area']

var_types

# Test for real landscapes
var = ['edge_dist', 'pid', 'patch_area', 'cross_pid', 'cross_patch_area']

landscape_vars, var_types, list_mapsets = list_landscape_variables(use_random_landscapes = False, variables = var)
landscape_vars['edge_dist']
landscape_vars

var_types
list_mapsets

#----------------------------------
# test pickup_one_landscape_garray

python

import os
import grass.script as grass

pydir = r'/home/leecb/Github/biodim/py'
os.chdir(pydir)
from landscape_modules import list_landscapes_habitat, list_landscape_variables, pickup_one_landscape_garray
import matplotlib.pyplot as plt
import numpy as np

from scipy import misc

# Test for random landscapes

# List of map names
list_habitat_map_names = list_landscapes_habitat(use_random_landscapes = True, habmat_pattern = '*HABMAT')
list_habitat_map_names

# Pick up one
landscape_name, landscape = pickup_one_landscape_garray(select_form = 'order', previous_landscape = 'simulation_000001_p029_h059_HABMAT', list_habitat_maps = list_habitat_map_names, 
                                                        exportPNG = True)
print landscape_name
print landscape

# order
#landscape_name, landscape = pickup_one_landscape_garray(select_form = 'order', previous_landscape = 'simulation_000001_p029_h059_HABMAT', list_habitat_maps = list_habitat_map_names, 
                                                        #exportPNG = True)
# always the same
#landscape_name, landscape = pickup_one_landscape_garray(select_form = 'same', previous_landscape = 'simulation_000001_p029_h059_HABMAT', list_habitat_maps = list_habitat_map_names, 
                                                        #exportPNG = True)

# Test for real landscapes

# List of map names
list_habitat_map_names = list_landscapes_habitat(use_random_landscapes = False, habmat_pattern = '*HABMAT')
list_habitat_map_names

# Pick up one
landscape_name, landscape = pickup_one_landscape_garray(select_form = 'order', previous_landscape = '', list_habitat_maps = list_habitat_map_names, 
                                                        exportPNG = True, null = -1, null_nan = True)
print landscape_name
print landscape
print landscape.shape

#misc.imsave('landscape.png', landscape)

# Show landscape
landscape_show = landscape[::4,::4]

plt.matshow(landscape_show, cmap = 'YlGn', 
            extent = (0,landscape_show.shape[1],landscape_show.shape[0],0)) 
plt.show()

#----------------------------------
# test pickup_one_landscape_garray and pickup_landscape_variables

python

import os
import grass.script as grass

pydir = r'/home/leecb/Github/biodim/py'
os.chdir(pydir)
from landscape_modules import list_landscapes_habitat, list_landscape_variables
from landscape_modules import pickup_one_landscape_garray, pickup_landscape_variables
import matplotlib.pyplot as plt
import numpy as np

# Test for random landscapes

# List of map names
list_habitat_map_names = list_landscapes_habitat(use_random_landscapes = True, habmat_pattern = '*HABMAT')
list_habitat_map_names

# Pick up one
landscape_name, landscape = pickup_one_landscape_garray(select_form = 'random', previous_landscape = '', list_habitat_maps = list_habitat_map_names, 
                                                        exportPNG = True)
print landscape_name
print landscape

# order
#landscape_name, landscape = pickup_one_landscape_garray(select_form = 'order', previous_landscape = 'simulation_000001_p029_h059_HABMAT', list_habitat_maps = list_habitat_map_names, 
                                                        #exportPNG = True)
# always the same
#landscape_name, landscape = pickup_one_landscape_garray(select_form = 'same', previous_landscape = 'simulation_000001_p029_h059_HABMAT', list_habitat_maps = list_habitat_map_names, 
                                                        #exportPNG = True)

# Show landscape
landscape_show = np.where(landscape > 1, 0, landscape)

plt.matshow(landscape_show, cmap = 'YlGn', 
            extent = (0,landscape_show.shape[1],landscape_show.shape[0],0)) 
plt.show()


# Variables
var = ['edge_dist', 'pid', 'patch_area']
var = ['patch_area']

# List of variable maps
landscape_vars, var_types, var_mapsets = list_landscape_variables(use_random_landscapes = True, variables = var)
landscape_vars['edge_dist']
landscape_vars[var[1]]
landscape_vars['patch_area']

var_types
var_mapsets

# Pick variables

loaded_var_names, var_maps = pickup_landscape_variables(habitat_map_name = landscape_name, variables = var, 
                                                        list_variable_maps = landscape_vars, 
                                                        variable_types = var_types, variable_mapsets = var_mapsets,
                                                        null = 0, null_nan = False,
                                                        exportPNG = True)

print loaded_var_names
print var_maps

# Look at the patch id map
patch_id_map = var_maps['pid']
patch_id_map.dtype

patch_id_map_show = np.where(patch_id_map == 0, np.nan, patch_id_map)
plt.matshow(patch_id_map_show, cmap = 'YlGn',
            extent = (0,patch_id_map_show.shape[1],patch_id_map_show.shape[0],0)) 
plt.show()

# Look at the patch area map
patch_area_map = var_maps['patch_area']

patch_area_map_show = np.where(patch_area_map == 0, np.nan, patch_area_map)
plt.matshow(patch_area_map_show, #cmap = 'RdYlBu',
            extent = (0,patch_area_map_show.shape[1],patch_area_map_show.shape[0],0)) 
plt.show()

# Test raw code
import grass.script as grass
import grass.script.array as garray
import numpy as np
import matplotlib.pyplot as plt

a = garray.array()
#a.read('simulation_000002_p050_h059_HABMAT_grassclump_AreaHA', null = np.nan)
a.read('simulation_000001_p029_h059_HABMAT_grassclump_AreaHA@MS_HABMAT_AREA', null = np.nan)
print a

plt.matshow(a, #cmap = 'RdYlBu',
            extent = (0,a.shape[1],a.shape[0],0)) 
plt.show()

# Test for real landscapes

# List of map names
list_habitat_map_names = list_landscapes_habitat(use_random_landscapes = False, habmat_pattern = '*HABMAT')
list_habitat_map_names

# Pick up one
landscape_name, landscape = pickup_one_landscape_garray(select_form = 'random', previous_landscape = '', list_habitat_maps = list_habitat_map_names, 
                                                        exportPNG = True, null = -1, null_nan = True)
print landscape_name
print landscape

# order
#landscape_name, landscape = pickup_one_landscape_garray(select_form = 'order', previous_landscape = 'simulation_000001_p029_h059_HABMAT', list_habitat_maps = list_habitat_map_names, 
                                                        #exportPNG = True)
# always the same
#landscape_name, landscape = pickup_one_landscape_garray(select_form = 'same', previous_landscape = 'simulation_000001_p029_h059_HABMAT', list_habitat_maps = list_habitat_map_names, 
                                                        #exportPNG = True)

# Show landscape
landscape_show = landscape[::4,::4]

plt.matshow(landscape_show, cmap = 'YlGn', 
            extent = (0,landscape_show.shape[1],landscape_show.shape[0],0)) 
plt.show()


# Variables
var = ['edge_dist', 'pid', 'patch_area', 'cross_pid', 'cross_patch_area']
var = ['pid', 'patch_area']

# List of variable maps
landscape_vars, var_types, var_mapsets = list_landscape_variables(use_random_landscapes = False, variables = var)

landscape_vars
var_types
var_mapsets

# Pick variables

loaded_var_names, var_maps = pickup_landscape_variables(habitat_map_name = landscape_name, variables = var, 
                                                        list_variable_maps = landscape_vars, 
                                                        variable_types = var_types, variable_mapsets = var_mapsets,
                                                        null = -1, null_nan = True,
                                                        exportPNG = True)

print loaded_var_names
print var_maps

# Look at the patch id map
patch_id_map = var_maps['pid']
patch_id_map_show = patch_id_map[::4,::4]

plt.matshow(patch_id_map_show, cmap = 'YlGn',
            extent = (0,patch_id_map_show.shape[1],patch_id_map_show.shape[0],0)) 
plt.show()

# Look at the patch area map
patch_area_map = var_maps['patch_area']
patch_area_map_show = patch_area_map[::4,::4]

plt.matshow(patch_area_map_show, #cmap = 'RdYlBu',
            extent = (0,patch_area_map_show.shape[1],patch_area_map_show.shape[0],0)) 
plt.show()


#----------------------------------
# test group_size

python

import os

pydir = r'/home/leecb/Github/biodim/py'
os.chdir(pydir)
from populate import group_size

Nind, group_sizes = group_size(Ngroups = 20, distribution = 'Poisson', mu = 5, minimum = 2)
Nind
group_sizes
group_sizes.mean()

#----------------------------------
# test conditions_monogramy

python 

import os

pydir = r'/home/leecb/Github/biodim/py'
os.chdir(pydir)
from populate import conditions_monogramy

group_list = [0,0,0,0,0,0]
conditions_monogramy(list_ind=group_list, assign_sex=False, assign_reproductive=False)

conditions_monogramy(list_ind=group_list, assign_sex=True, assign_reproductive=False)

conditions_monogramy(list_ind=group_list, assign_sex=False, assign_reproductive=True)

#----------------------------------
# test assign_sex and assign_sex_v2

python 

import os
import numpy as np

pydir = r'/home/leecb/Github/biodim/py'
os.chdir(pydir)
from populate import assign_sex, conditions_monogramy, group_size, assign_sex_not_efficient

# For individuals
Na = 20
sexes = assign_sex_not_efficient(Na, sex_ratio=0.5, group=False, group_sizes=None, condition=None)
sexes
np.mean(sexes)

sexes2 = assign_sex(Na, sex_ratio=0.5, group=False, group_sizes=None, condition=None)
sexes2
sexes2.mean()

# For groups
Nind, group_sizes = group_size(Ngroups = Na, distribution = 'Poisson', mu = 5, minimum = 2)
Nind
group_sizes

# Without monogamy
sexes = assign_sex_not_efficient(Na, sex_ratio=0.5, group=True, group_sizes=group_sizes, condition=None)
sexes
[np.mean(i) for i in sexes]
np.mean([np.mean(i) for i in sexes])

sexes2 = assign_sex(Na, sex_ratio=0.5, group=True, group_sizes=group_sizes, condition=None)
sexes2
sexes2.mean()

# With monogamy
sexes = assign_sex_not_efficient(Na, sex_ratio=0.5, group=True, group_sizes=group_sizes, condition='monogamy')
sexes
[np.mean(i) for i in sexes]
np.mean([np.mean(i) for i in sexes])

sexes2 = assign_sex(Na, sex_ratio=0.5, group=True, group_sizes=group_sizes, condition='monogamy')
sexes2
group_sizes

assign_sex(Na = 20, sex_ratio=0, group=True, group_sizes=group_sizes, condition='monogamy')

from timeit import timeit

timeit("assign_sex_not_efficient(Na, sex_ratio=0.5, group=True, group_sizes=group_sizes, condition='monogamy')", 
       setup ="from populate import assign_sex_not_efficient, group_size; Na = 2000; Nind, group_sizes = group_size(Ngroups = Na, distribution = 'Poisson', mu = 5, minimum = 2)", number = 1000)

timeit("assign_sex(Na, sex_ratio=0.5, group=True, group_sizes=group_sizes, condition='monogamy')", 
       setup ="from populate import assign_sex, group_size; Na = 2000; Nind, group_sizes = group_size(Ngroups = Na, distribution = 'Poisson', mu = 5, minimum = 2)", number = 1000)

#----------------------------------
# test assign_age_reproductive

python 

import os
import numpy as np

pydir = r'/home/leecb/Github/biodim/py'
os.chdir(pydir)
from populate import assign_age_reproductive, group_size

# For individuals
Na = 20
age, repro = assign_age_reproductive(Na, set_reproductive=True)
age
np.mean(age)
repro

# For groups
Nind, group_sizes = group_size(Ngroups = Na, distribution = 'Poisson', mu = 5, minimum = 2)
Nind
group_sizes

# With monogamy
age, repro = assign_age_reproductive(Na, maximum_age=16*12, set_reproductive=True, 
                                     group = True, group_sizes=group_sizes, condition='monogamy')
age
np.mean(age)
repro

#----------------------------------
# test get_habitat_prop_cells

python 

import os
import numpy as np

pydir = r'/home/leecb/Github/biodim/py'
os.chdir(pydir)
from landscape_modules import get_habitat_prop_cells, np_getForest_habmat

from timeit import timeit

# new version
timeit("get_habitat_prop_cells(mapa)", 
       setup ="from landscape_modules import get_habitat_prop_cells, np_getForest_habmat; import numpy as np; mapa = np.where(np.random.random((512,512)) < 0.5, 0, 1)", number = 1000)

# old version
timeit("np_getForest_habmat(mapa)", 
       setup ="from landscape_modules import get_habitat_prop_cells, np_getForest_habmat; import numpy as np; mapa = np.where(np.random.random((512,512)) < 0.5, 0, 1)", number = 1000)

#----------------------------------
# test populate

python 

import os
import numpy as np

pydir = r'/home/leecb/Github/biodim/py'
os.chdir(pydir)
from populate import populate_rowcol
from landscape_modules import get_habitat_prop_cells
from populate import group_size

# Create a binary landscape map
landscape_map = np.where(np.random.random((512,512)) > 0.5, 1, 0)
landscape_map = np.where(np.random.random((25,25)) > 0.5, 1, 0)

# Get habitat cells
pland, cells = get_habitat_prop_cells(landscape_map)
pland
cells

Na = 20
xy = populate_rowcol(Na, where=cells)
xy

# Show landscape and positions
import matplotlib.pyplot as plt

plt.matshow(landscape_map, cmap = 'YlGn', 
            extent = (0,landscape_map.shape[1],landscape_map.shape[0],0)) 

y = xy[:,0]
x = xy[:,1]
plt.scatter(x, y, c = 'red')
plt.show()

# For groups
Na = 20
Nind, group_sizes = group_size(Ngroups = Na)

xy = populate_rowcol(Na, where=cells, group=True, group_sizes=group_sizes)
print xy

#----------------------------------
# test initialize_genetics

python 

import os
import numpy as np

pydir = r'/home/leecb/Github/biodim/py'
os.chdir(pydir)
from genetics import initialize_genetics

Na = 20
n_loci = 5
gen = initialize_genetics(Na, n_loci=n_loci)
gen
gen[0]
np.max(gen, 0)

n_alelles = [2,2,4,3,7]
gen = initialize_genetics(Na, n_loci=n_loci, n_alelles=n_alelles)
print gen
print gen[0]
print np.max(gen, 0)
print np.mean(gen, 0)

#----------------------------------
# test mortality

python 

import os
import numpy as np
folder = r'/home/leecb/Github/biodim/py'
os.chdir(folder)
from mortality import mortality_general

age_classes = [1,2,4,19,20]
mortality_rate = [0.3, 0.2, 0.15, 0.14, 0.95]

individuals_alive = np.zeros(100, dtype = np.int8) + 1
individuals_age = np.random.uniform(0, 20, 100)

# constant mortality - arguments after mortality_options are ignored
mortality_general(individuals_alive, include_mortality=True, 
                 mortality_rate=[0.01], 
                 mortality_option='constant', 
                 individuals_age=individuals_age, age_classes=age_classes, 
                 habitat_types=[])

# age dependent mortality
mortality_general(individuals_alive, include_mortality=True, 
                 mortality_rate=mortality_rate, 
                 mortality_option='age_class', 
                 individuals_age=individuals_age, age_classes=age_classes, 
                 habitat_types=[])

# no mortality
mortality_general(individuals_alive, include_mortality=False)

#----------------------------------
# test reproduce

python 

import os
import numpy as np
folder = r'/home/leecb/Github/biodim/py'
os.chdir(folder)
from reproduction import reproduce, sample_offspring_size
from genetics import initialize_genetics, reproduce_genetics
import matplotlib.pyplot as plt

# Test offspring size
sample_offspring_size(n_agents = 50, offspring_size=[2], offspring_parameter='constant', 
                      zero_offspring_possible=False)

# Error
sample_offspring_size(n_agents = 50, offspring_size=[0], offspring_parameter='constant', 
                      zero_offspring_possible=False)

sample_offspring_size(n_agents = 50, offspring_size=[0], offspring_parameter='constant', 
                      zero_offspring_possible=True)

# Error
sample_offspring_size(n_agents = 50, offspring_size=[2], offspring_parameter='Gaussian', 
                      zero_offspring_possible=False)

sample_offspring_size(n_agents = 50, offspring_size=[1.8,1], offspring_parameter='Gaussian', 
                      zero_offspring_possible=False)
# plot
plt.hist(sample_offspring_size(n_agents = 50, offspring_size=[1.8,1], offspring_parameter='Gaussian', 
                               zero_offspring_possible=False))

# plot w/ zero
plt.hist(offspring_size(n_agents = 50, offspring_size=[1.8,1], offspring_parameter='Gaussian', 
              zero_offspring_possible=True))

# Error
sample_offspring_size(n_agents = 50, offspring_size=[1.8,1], offspring_parameter='Poisson', 
                      zero_offspring_possible=False)

sample_offspring_size(n_agents = 50, offspring_size=[1.8], offspring_parameter='Poisson', 
                      zero_offspring_possible=False)

# plot
plt.hist(sample_offspring_size(n_agents = 50, offspring_size=[1.8], offspring_parameter='Poisson', 
                               zero_offspring_possible=False))

# plot w/ zero
plt.hist(sample_offspring_size(n_agents = 50, offspring_size=[1.8], offspring_parameter='Poisson', 
                               zero_offspring_possible=True))

# Test reproduce_genetics

n_new_ind = 10
parents_genetics = initialize_genetics(30, n_loci=5, n_alelles=[2], diploid=True)
dad = np.arange(10)
mom = np.array([20,20,20,21,21,21,21,24,24,25])
individual_id = np.arange(30)

# 1st approach
np.in1d(individual_id, mom).nonzero()[0] # 4 values instead of 10. does not work if there are repeated values in mom
np.in1d(individual_id, dad).nonzero()[0] # for all different values in dad it works
# 2nd approach
np.where(individual_id == mom[:,None])[1]
np.where(individual_id == dad[:,None])[1]


new_genetics = reproduce_genetics(Nind = n_new_ind, individual_id = individual_id, 
                                  individual_genetics = parents_genetics, 
                                  who_is_dad = dad, who_is_mom = mom)
print new_genetics.shape
print new_genetics

# Test reproduce

Nind = 15 # number of inds
individual_id = np.arange(Nind) # ids
individual_group = np.array([0,0,0,0,0,1,1,1,1,2,2,2,2,2,2])
individual_sex = np.array([0,1,0,1,0,1,0,1,0,1,0,1,0,1,0])
individual_reproductive_status = np.array([1,1,0,0,0,0,1,1,0,0,0,0,0,1,1])
individual_positions = np.random.random((Nind,2))
probability_female_reproduce = 0.8
offspring_size = [2]
individual_genetics = initialize_genetics(Nind, n_loci=5, n_alelles=[2], diploid=True)

new_inds = reproduce(individual_id=individual_id, individual_sex=individual_sex, 
                     individual_reproductive_status=individual_reproductive_status, 
                     simulation_step=1, group=True, individual_group=individual_group, 
                     individual_positions=individual_positions, set_genetics=True, 
                     individual_genetics=individual_genetics, 
                     probability_female_reproduce=probability_female_reproduce,
                     offspring_size=offspring_size, offspring_parameter='Poisson', 
                     zero_offspring_possible=False, sex_ratio=0.5)

for key, val in new_inds.iteritems():
    print key, val


#----------------------------------
# test disperse_death_reproducer

python 

import os
import numpy as np
folder = r'/home/leecb/Github/biodim/py'
os.chdir(folder)
from mortality import mortality_general
from dispersal import disperse_death_reproducer
from populate import assign_age_reproductive, assign_sex, group_size, populate_rowcol
from landscape_modules import list_landscapes_habitat, list_landscape_variables, pickup_one_landscape_garray, pickup_landscape_variables, get_habitat_prop_cells


# Get habitat map list
list_habitat_map_names = list_landscapes_habitat(use_random_landscapes = True, habmat_pattern = '*HABMAT')
list_habitat_map_names

# Pick up one landscape
landscape_name, landscape = pickup_one_landscape_garray(select_form = 'random', previous_landscape = '', list_habitat_maps = list_habitat_map_names, 
                                                        exportPNG = True)
print landscape_name
print landscape

# Variables
variables = ['pid', 'patch_area']

# List of variable maps
# (maybe in the runs all the lists that will be used may be load only once)
landscape_vars, var_types = list_landscape_variables(use_random_landscapes = True, variables = variables)
for i in range(len(variables)):
    print landscape_vars[variables[i]]

# Pick variables
loaded_var_names, var_maps = pickup_landscape_variables(habitat_map_name = landscape_name, variables = variables, list_variable_maps = landscape_vars, 
                                                        variable_types = var_types,
                                                        exportPNG = True)
print loaded_var_names
print var_maps

# Create agents
Ngroups = 20

# Define group size
Nind, group_size_sample = group_size(Ngroups = Ngroups, distribution='Gaussian', mu=5.0, 
                               sd=1.0, minimum=2)
print Nind
print group_size_sample

individuals_alive = np.zeros(Nind, dtype = np.int8) + 1
print individuals_alive

# Individual id
individual_id = np.arange(Nind)

# Individual mom and dad
individual_dad = np.empty(Nind)
individual_dad.fill(np.nan)
individual_mom = np.empty(Nind)
individual_mom.fill(np.nan)

# Individuals are not dispersing
individual_dispersing = np.zeros(Nind)

# constant mortality - arguments after mortality_options are ignored
dead_individuals = mortality_general(individuals_alive, include_mortality=True, 
                                     mortality_rate=[0.3], 
                                     mortality_option='constant')
print dead_individuals

# define groups
individual_group = np.repeat(range(Ngroups), group_size_sample)
print individual_group

# define sex
individual_sex = assign_sex(Na = Nind, sex_ratio = 0.5, 
                            group = True, group_sizes = group_size_sample, 
                            condition = 'monogamy')
print individual_sex

# define reproductive status
individual_age, individual_reproductive_status = assign_age_reproductive(Na = Ngroups, mean_age = 4*12, sd_age = 1*12, maximum_age = 20*12, 
                                                             set_reproductive = True, reproductive_age = 4*12, 
                                                             group = True, group_sizes = group_size_sample, condition = 'monogamy')
print individual_reproductive_status
print individual_age

# Place agents on habitat
prop_habitat, habitat_cells = get_habitat_prop_cells(landscape)

individual_positions = populate_rowcol(Ngroups, where = habitat_cells,
                                       condition_populate = 'habitat', replace = False,
                                       group=True, group_sizes=group_size_sample)
print individual_positions

# Show landscape and positions
import matplotlib.pyplot as plt

landscape_show = np.where(landscape > 1, 0, landscape)

plt.matshow(landscape_show, cmap = 'YlGn', 
            extent = (0,landscape_show.shape[1],landscape_show.shape[0],0)) 
y, x = individual_positions.T
plt.scatter(x, y, c = 'red')
#plt.show()

# Look at the patch id map
patch_id_map = var_maps['pid']

patch_id_map = np.where(patch_id_map == 0, np.nan, patch_id_map)
plt.matshow(patch_id_map, 
            extent = (0,patch_id_map.shape[1],patch_id_map.shape[0],0)) 
plt.scatter(x, y, c = 'red')

#plt.show()

a, b, c, d, e, f = disperse_death_reproducer(
    dead_individuals = dead_individuals, 
    individual_reproductive_status = individual_reproductive_status, 
    individual_sex = individual_sex, 
    individual_group = individual_group, 
    individual_positions = individual_positions, 
    individual_age = individual_age, 
    individual_dispersing = individual_dispersing, 
    individual_id = individual_id, 
    individual_dad = individual_dad, 
    individual_mom = individual_mom, 
    reproductive_age = 1*12, 
    maximum_distance=100000.0, 
    who_can_replace='same_patch', 
    patch_id_map=patch_id_map)

#----------------------------------
# test dispersal_simple and choose_who_disperses

python

import os
import numpy as np
folder = r'/home/leecb/Github/biodim/py'
os.chdir(folder)
from mortality import mortality_general
from dispersal import disperse_death_reproducer, choose_who_disperses, dispersal_step_selection_simple, settle
from populate import assign_age_reproductive, assign_sex, group_size, populate_rowcol, define_home_range
from landscape_modules import list_landscapes_habitat, list_landscape_variables, pickup_one_landscape_garray, pickup_landscape_variables, get_habitat_prop_cells

# Create agents
Ngroups = 20

# Agent id
agent_id = np.arange(20)

# Define group size
Nind, group_size_sample = group_size(Ngroups = Ngroups, distribution='Gaussian', mu=5.0, 
                               sd=1.0, minimum=2)
print Nind
print group_size_sample

individuals_alive = np.zeros(Nind, dtype = np.int8) + 1
print individuals_alive

# Individual id
individual_id = np.arange(Nind)

# Individuals are not dispersing
individual_dispersing = np.zeros(Nind)
#individual_dispersing[[3,8]] = 1

# define groups
individual_group = np.repeat(range(Ngroups), group_size_sample)
print individual_group

# define sex
individual_sex = assign_sex(Na = Nind, sex_ratio = 0.5, 
                            group = True, group_sizes = group_size_sample, 
                            condition = 'monogamy')
print individual_sex

# define reproductive status
individual_age, individual_reproductive_status = assign_age_reproductive(Na = Ngroups, mean_age = 4*12, sd_age = 1*12, maximum_age = 20*12, 
                                                             set_reproductive = True, reproductive_age = 4*12, 
                                                             group = True, group_sizes = group_size_sample, condition = 'monogamy')
print individual_reproductive_status
print individual_age

# constant mortality - arguments after mortality_options are ignored
dead_individuals = mortality_general(individuals_alive, include_mortality=True, 
                                     mortality_rate=[0.05], 
                                     mortality_option='constant')
print dead_individuals

# Home ranges
home_range_sizes = define_home_range(Ngroups, distribution = 'Gaussian', 
                                     minimum_HRsize = 8, 
                                     mean_HRsize = 30, SD_HRsize = 5)

# Choose individuals which will disperse
individuals_dispersing = choose_who_disperses(p_disperse=0.05, individual_dispersing=individual_dispersing,
                                              dead_individuals = dead_individuals,
                                              individual_age=individual_age, dispersal_age=24, 
                                              reproductive_can_disperse=False, 
                                              individual_reproductive_status=individual_reproductive_status)

#----------
# Get habitat map list
list_habitat_map_names = list_landscapes_habitat(use_random_landscapes = True, habmat_pattern = '*HABMAT')
list_habitat_map_names

# Pick up one landscape
landscape_name, landscape = pickup_one_landscape_garray(select_form = 'random', previous_landscape = '', list_habitat_maps = list_habitat_map_names, 
                                                        exportPNG = True, null = np.nan)
print landscape_name
print landscape

# Variables
variables = ['pid', 'patch_area']

# List of variable maps
# (maybe in the runs all the lists that will be used may be load only once)
landscape_vars, var_types, var_mapsets = list_landscape_variables(use_random_landscapes = True, variables = variables)
for i in range(len(variables)):
    print landscape_vars[variables[i]]

# Pick variables
loaded_var_names, var_maps = pickup_landscape_variables(habitat_map_name = landscape_name, variables = variables, list_variable_maps = landscape_vars, 
                                                        variable_types = var_types, variable_mapsets = var_mapsets, null = np.nan,
                                                        exportPNG = True)
print loaded_var_names
print var_maps


# Place agents on habitat
prop_habitat, habitat_cells = get_habitat_prop_cells(landscape)

individual_positions = populate_rowcol(Ngroups, where = habitat_cells,
                                       condition_populate = 'habitat', replace = False,
                                       group=True, group_sizes=group_size_sample)
print individual_positions

# Show landscape and positions
import matplotlib.pyplot as plt

landscape_show = np.where(landscape > 1, 0, landscape)

plt.matshow(landscape_show, cmap = 'YlGn', 
            extent = (0,landscape_show.shape[1],landscape_show.shape[0],0)) 
y, x = individual_positions.T
plt.scatter(x, y, c = 'red')
plt.show()

# Look at the patch id map
patch_id_map = var_maps['pid']

patch_id_map = np.where(patch_id_map == 0, np.nan, patch_id_map)
plt.matshow(patch_id_map, cmap = 'YlGn',
            extent = (0,patch_id_map.shape[1],patch_id_map.shape[0],0)) 
plt.scatter(x, y, c = 'red')
plt.show()

# Look at the patch area map
patch_area_map = var_maps['patch_area']

patch_area_map = np.where(patch_area_map == 0, np.nan, patch_area_map)
plt.matshow(patch_area_map, #cmap = 'RdYlBu',
            extent = (0,patch_area_map.shape[1],patch_area_map.shape[0],0)) 
plt.scatter(x, y, c = 'red')
plt.show()

a, b, c, d, e, f, g = dispersal_step_selection_simple(individuals_dispersing = individuals_dispersing, 
                                            individual_positions = individual_positions, 
                                            dead_individuals = dead_individuals, 
                                            individual_group = individual_group,
                                            max_agent_id = Ngroups,
                                            ntries=50, nsteps=1, 
                                            distribution="Weibull", scale=100.0, shape=2.0, 
                                            landscape_map=landscape, landscape_values=[1])
print a, b, c, d, e, f, g

# update variables
max_agent_ID = f
agent_id = np.concatenate((agent_id, g))
home_range_sizes = np.concatenate((home_range_sizes, np.repeat(np.nan, repeats = g.shape[0])))

import matplotlib.pyplot as plt

# Changed positions
plt.matshow(landscape_show, cmap = 'YlGn', 
            extent = (0,landscape_show.shape[1],landscape_show.shape[0],0)) 
y, x = individual_positions.T
plt.scatter(x, y, c = 'red')

changed = np.where(c == individual_positions, np.nan, c)

yy, xx = changed.T
plt.scatter(xx, yy, c = 'blue')
plt.show()

# Settle
new_individuals_dispersing, new_individual_group, new_individual_positions, new_dead_individuals, new_individual_reproductive_status, new_home_range_sizes = settle(
    individuals_dispersing = individuals_dispersing, individual_group = e, 
    individual_positions = c, dead_individuals = d,
    individual_reproductive_status = individual_reproductive_status, individual_sex = individual_sex, 
    agent_id = agent_id, home_range_sizes = home_range_sizes, 
    distribution_HR = "Gaussian", mean_HRsize = 30.0, min_HRsize=10.0, SD_HRsize = 2.0, 
    maximum_distance=100000.0, p_enter_group = 0.15,
    who_can_mate = 'same_patch', patch_id_map = patch_id_map,
    patch_area_map = patch_area_map)

print new_individuals_dispersing
print new_individual_group
print new_individual_positions
print new_dead_individuals
print new_individual_reproductive_status
print new_home_range_sizes

#----------------------------------
# test classes Animal and GLT

python 

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
print animal.include_genetics
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
print animal2.include_reproduction
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

glts.set_initial_conditions(Na = 20, mean_age = 5 * 12, sex_ratio = 0.5,
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
plt.show()

area_tot = pland*landscape_map.shape[0]*landscape_map.shape[1]*30.0*30.0/10000

patch_area_map = np.where(landscape_map == 1, area_tot, 0)

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
               who_can_replace='any', patch_id_map=[], 
               ntries=50, nsteps=1, distribution="Weibull", 
               scale=100.0, shape=2.0, landscape_map=landscape_map, 
               landscape_values=[1])

#glts.dispersal(after_death_reproducer=False, disperse_regular=True, 
              #maximum_distance=8000.0, 
              #who_can_replace='same_patch', patch_id_map=[], 
              #ntries=50, nsteps=1, distribution="Weibull", 
              #scale=100.0, shape=2.0, landscape_map=landscape_map, 
              #landscape_values=[1])

print glts.positions
print glts.dispersing
print glts.dead
print glts.individual_group

# Changed positions
ax = plt.matshow(landscape_map, cmap = 'YlGn', 
            extent = (0,landscape_map.shape[1],landscape_map.shape[0],0)) 
y, x = glts.init_positions.T
plt.scatter(x, y, c = 'red')

changed = np.where(glts.positions == glts.init_positions, np.nan, glts.positions)

yy, xx = changed.T
dy, dx = (glts.positions - glts.init_positions).T

#plt.arrow(0, 0, 20, 20, head_width = 2, ec = 'k', fc = 'k')
for i in range(len(xx)):
    if not np.isnan(xx[i]):
        plt.arrow(x[i], y[i], dx[i], dy[i],
                  head_width=0.5, head_length=0.5, ec = 'r', fc = 'r')

        
plt.scatter(xx, yy, c = 'blue', s = 100)
plt.show()

glts.dispersal(to_settle = True, 
               maximum_distance=8000.0, 
               who_can_replace='any', landscape_map=landscape_map, patch_area_map=patch_area_map)

glts.dispersing
glts.dead
glts.individual_group
#glts.dispersal(to_settle = True,
               #maximum_distance=8000.0, 
               #who_can_replace='same_patch')

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

print glts.init_group_sizes.shape[0]
print glts.Ngroups
print glts.Na
print glts.agent_id
print glts.home_range
print glts.max_agent_ID

# Test mortality - age dependent
glts.mortality(mortality_rate=[0.05, 0.15], mortality_option='age_class', 
              age_classes=[5,glts.maximum_age])

print glts.alive
print glts.alive.shape
print glts.dead
print glts.dead_individual_id

# Test dispersal after mortality of reproducer
print glts.dead
print (glts.dead) & (glts.reproductive_status) # check if there will be dispersal

glts.dispersal(after_death_reproducer = True, who_can_replace='any')

# Settle if len(dispersing not dead ) > 0

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
glts.reproduction(simulation_step = 1, 
                  offspring_parameter='Poisson', offspring_size=[2])
glts.new_inds


# Test update
glts.update(current_step = 1, update_reproduction = True)
glts.age
glts.sex
glts.sex.shape[0]
glts.Nind
glts.Na
glts.genetics

# test times

python

from timeit import timeit

#from teste_velo import init
timeit(stmt="init()", setup = 'import os; os.chdir(r"/home/leecb/Github/biodim/py"); from teste_velo import init', number=10)

#----------------------------------
# test 20 loops with class GLT

python 

import os
import numpy as np

pydir = r'/home/leecb/Github/biodim/py'
os.chdir(pydir)
from class_animal import GLT
from populate import group_size
from landscape_modules import get_habitat_prop_cells

# Create a binary landscape map
landscape_map = np.where(np.random.random((50,50)) > 0.5, 1, 0)

# Get habitat cells
pland, cells = get_habitat_prop_cells(landscape_map)
pland
cells

area_tot = pland*landscape_map.shape[0]*landscape_map.shape[1]*30.0*30.0/10000

patch_area_map = np.where(landscape_map == 1, area_tot, 0)

# Create agents
glts = GLT(include_reproduction = True, maximum_age=16 * 12)

# Set itial conditions
glts.set_initial_conditions(Na = 500, mean_age = 5 * 12, sex_ratio = 0.5,
                            populate_where = cells)

print glts.Na
print glts.Nind
print glts.Ngroups

# Show landscape and positions
import matplotlib.pyplot as plt

plt.matshow(landscape_map, cmap = 'YlGn', 
            extent = (0,landscape_map.shape[1],landscape_map.shape[0],0)) 
y, x = glts.init_positions.T
plt.scatter(x, y, c = 'red')
plt.show()

for step in range(120):
    
    # mortality - constant
    glts.mortality()
    #print glts.alive
    #print glts.alive.shape
    #print glts.dead
    #print glts.dead_individual_id
    
    # Test dispersal after mortality of reproducer
    #print glts.dead
    #print (glts.dead) & (glts.reproductive_status) # check if there will be dispersal
    
    #print glts.times_dispersed
    #print glts.total_distance_dispersed
    
    glts.dispersal(after_death_reproducer = True, who_can_replace='any')
    
    #print glts.times_dispersed
    #print glts.total_distance_dispersed
    
    #print glts.reproductive_status
    #print glts.dispersing
    #print glts.individual_group
    #print glts.positions
    
    glts.dispersal(after_death_reproducer=False, disperse_regular=True, 
                   maximum_distance=8000.0, 
                   who_can_replace='any', patch_id_map=[], 
                   ntries=50, nsteps=1, distribution="Weibull", 
                   scale=100.0, shape=2.0, landscape_map=landscape_map, 
                   landscape_values=[1])
    
    #print glts.dispersing
    #print glts.positions
    #print glts.dead
    #print glts.individual_group
    
    # Changed positions
    #ax = plt.matshow(landscape_map, cmap = 'YlGn', 
                #extent = (0,landscape_map.shape[1],landscape_map.shape[0],0)) 
    #y, x = glts.init_positions.T
    #plt.scatter(x, y, c = 'red')
    
    #changed = np.where(glts.positions == glts.init_positions, np.nan, glts.positions)
    
    #yy, xx = changed.T
    #dy, dx = (glts.positions - glts.init_positions).T
    
    ##plt.arrow(0, 0, 20, 20, head_width = 2, ec = 'k', fc = 'k')
    #for i in range(len(xx)):
        #if not np.isnan(xx[i]):
            #plt.arrow(x[i], y[i], dx[i], dy[i],
                      #head_width=0.5, head_length=0.5, ec = 'r', fc = 'r')
    
            
    #plt.scatter(xx, yy, c = 'blue', s = 100)
    #plt.show()
    
    # Settle
    glts.dispersal(to_settle = True, 
                   maximum_distance=8000.0, 
                   who_can_replace='any', landscape_map=landscape_map,
                   patch_area_map = patch_area_map)
    
    
    # Test update
    glts.update(current_step = step, update_mortality=True)
    
    #print glts.alive
    #print glts.alive.shape
    #print glts.dead
    #print glts.dead_individual_id
    #print glts.dead_age
    
    #print glts.init_Nind
    #print glts.Nind
    print str(glts.init_Nind - glts.Nind)+' individuals died'
    
    #if (glts.init_Nind - glts.Nind) < 0:
        #break
    
    #print glts.init_group_sizes.shape[0]
    #print glts.Ngroups
    #print glts.Na
    #print glts.agent_id
    #print glts.home_range
    #print glts.max_agent_ID
    
    # Test mortality - age dependent
    #glts.mortality(mortality_rate=[0.05, 0.15], mortality_option='age_class', 
                  #age_classes=[5,glts.maximum_age])
    
    #print glts.alive
    #print glts.alive.shape
    #print glts.dead
    #print glts.dead_individual_id
    
    ## Test dispersal after mortality of reproducer
    #print glts.dead
    #print (glts.dead) & (glts.reproductive_status) # check if there will be dispersal
    
    #glts.dispersal(after_death_reproducer = True, who_can_replace='any')
    
    ## Settle if len(dispersing not dead ) > 0
    
    ## Test update
    #glts.update(current_step=2, update_mortality=True)
    
    #print glts.alive
    #print glts.alive.shape
    #print glts.dead
    #print glts.dead_individual_id
    #print glts.dead_age
    
    #print glts.init_Nind
    #print glts.Nind
    #print str(glts.init_Nind - glts.Nind)+' individuals died'
    
    # test reproduction
    if step % 8 == 0:
        glts.reproduction(simulation_step = 1, 
                          offspring_parameter='Poisson', offspring_size=[2])
        #glts.new_inds
    
        # Test update
        glts.update(current_step = step, update_reproduction = True)
    
    if glts.Nind <= 0:
        print 'population extinct!'
        break
    
    #glts.age
    #glts.sex
    #glts.sex.shape[0]
    #glts.Nind
    #glts.Na
    #glts.genetics
    

print glts.Na   
print glts.Nind
print glts.Ngroups

#----------------------------------
# test function read_write_input_parms

python 

import os
from collections import OrderedDict

pydir = r'/home/leecb/Github/biodim/py'
os.chdir(pydir)
from biodim_io import read_write_input_parms

# folder and filename
folder = r'/home/leecb/Github/biodim/temp'
fil = 'setup_test.txt'

# dictionary with parameters
dictio = OrderedDict([('par1', 10), ('par2', 20.0), ('par3', False), ('par4', None)])

# Test write
read_write_input_parms(folder_name = folder, file_name = fil, rw = 'w', parms=dictio)

# Test read
dictio2 = read_write_input_parms(folder_name = folder, file_name = fil, rw = 'r')
for i in dictio2:
    print i, dictio2[i], type(dictio2[i])


#----------------------------------
# test class biodim_simulation

python 

import os

pydir = r'/home/leecb/Github/biodim/py'
os.chdir(pydir)
from classes import biodim_simulation

# Write file
sim = biodim_simulation(save_setup_file='testeee')
print sim.setup['n_steps']
print sim.setup['time_step']
print sim.setup['time_unit']
print sim.steps
print sim.steps[0]
print sim.steps[0].year

# Read file
sim = biodim_simulation(load_file='biodim_setup_2017-11-06_13-28-26.txt', load_dir='.')
print sim.setup['n_steps']
print sim.steps

#----------------------------------
# test run a simulation

python 

import os
import numpy as np
import grass.script as grass

pydir = r'/home/leecb/Github/biodim/py'
os.chdir(pydir)
from class_animal import Animal, GLT
from landscape_modules import list_landscapes_habitat, list_landscape_variables, pickup_one_landscape_garray, pickup_landscape_variables, get_habitat_prop_cells

# Get habitat map list
list_habitat_map_names = list_landscapes_habitat(use_random_landscapes = True, habmat_pattern = '*HABMAT')
list_habitat_map_names

# Create GLT object
glts = GLT()

# Pick up one landscape
landscape_name, landscape = pickup_one_landscape_garray(select_form = 'random', previous_landscape = '', list_habitat_maps = list_habitat_map_names, 
                                                        exportPNG = True)
print landscape_name
print landscape

# order
#landscape_name, landscape = pickup_one_landscape_garray(select_form = 'order', previous_landscape = 'simulation_000001_p029_h059_HABMAT', list_habitat_maps = list_habitat_map_names, 
                                                        #exportPNG = True)
# always the same
#landscape_name, landscape = pickup_one_landscape_garray(select_form = 'same', previous_landscape = 'simulation_000001_p029_h059_HABMAT', list_habitat_maps = list_habitat_map_names, 
                                                        #exportPNG = True)

# Variables
glts.landscape_variables

# List of variable maps
# (maybe in the runs all the lists that will be used may be load only once)
landscape_vars, var_type, var_mapset = list_landscape_variables(use_random_landscapes = True, variables = glts.landscape_variables)
for i in range(len(glts.landscape_variables)):
    print landscape_vars[glts.landscape_variables[i]]

# Pick variables
loaded_var_names, var_maps = pickup_landscape_variables(habitat_map_name = landscape_name, variables = glts.landscape_variables, list_variable_maps = landscape_vars, 
                                                        variable_types = var_type, variable_mapsets = var_mapset,
                                                        exportPNG = True)
print loaded_var_names
print var_maps

# Get info about the landscape
prop_habitat, habitat_cells = get_habitat_prop_cells(landscape)

####################################
# Put later the condition to check if pop > K, and choose K instead

# Initialize agents in space
glts.set_initial_conditions(Na = 1000, mean_age = 5 * 12, sex_ratio = 0.5,
                            populate_where = habitat_cells)

# Show landscape and positions
import matplotlib.pyplot as plt

landscape_show = np.where(landscape > 1, 0, landscape)

plt.matshow(landscape_show, cmap = 'YlGn', 
            extent = (0,landscape_show.shape[1],landscape_show.shape[0],0)) 
y, x = glts.init_positions.T
plt.scatter(x, y, c = 'red')
plt.show()

## Test reproduction
#glts.reproduction(simulation_step = 1, 
                  #offspring_parameter='Poisson', offspring_size=[2])
#glts.new_inds

## Test update
#glts.update(current_step = 1, update_reproduction = True)
#glts.age
#glts.sex
#glts.sex.shape[0]
#glts.Nind
#glts.Na
#glts.genetics

#print glts.init_Nind
#print glts.Nind
#print str(glts.Nind - glts.init_Nind)+' were born'

## Test mortality - age dependent
#glts.mortality(mortality_rate=[0.2, 0.15, 0.12, 0.1, 0.95], mortality_option='age_class', 
              #age_classes=[1*12, 2*12, 4*12, 15*12,glts.maximum_age])

#print glts.alive
#print glts.alive.shape
#print glts.dead
#print glts.dead_individual_id

## Test update
#glts.update(current_step=1, update_mortality=True)

#print glts.alive
#print glts.alive.shape
#print glts.dead
#print glts.dead_individual_id
#print glts.dead_age

#print glts.init_Nind
#print glts.Nind
#print str(glts.init_Nind - glts.Nind)+' individuals died'

for step in range(120):
    
    # mortality - constant
    #glts.mortality()
    glts.mortality(mortality_rate=[0.2, 0.15, 0.12, 0.1, 0.95], mortality_option='age_class', 
                   age_classes=[1*12, 2*12, 4*12, 15*12, glts.maximum_age])    
    #print glts.alive
    #print glts.alive.shape
    #print glts.dead
    #print glts.dead_individual_id
    
    ##Test dispersal after mortality of reproducer
    #print glts.dead
    #print (glts.dead) & (glts.reproductive_status) # check if there will be dispersal
    
    #print glts.times_dispersed
    #print glts.total_distance_dispersed
    
    #reload()
    glts.dispersal(after_death_reproducer = True, who_can_replace='same_patch',
                   patch_id_map = var_maps['pid'])
    
    #print glts.times_dispersed
    #print glts.total_distance_dispersed
    
    #print glts.reproductive_status
    #print glts.dispersing
    #print glts.individual_group
    #print glts.positions
    
    glts.dispersal(after_death_reproducer=False, disperse_regular=True, 
                   maximum_distance=8000.0, 
                   who_can_replace='same_patch', patch_id_map = var_maps['pid'], 
                   ntries=50, nsteps=1, distribution="Weibull", 
                   scale=100.0, shape=2.0, landscape_map=landscape, 
                   landscape_values=[1])
    
    #print glts.positions
    #print glts.dispersing
    #print glts.dead
    #print glts.individual_group
    
    # Changed positions
    #landscape_show = np.where(landscape > 1, 0, landscape)
        
    #ax = plt.matshow(landscape_show, cmap = 'YlGn', 
                #extent = (0,landscape_show.shape[1],landscape_show.shape[0],0))
    #y, x = glts.init_positions.T
    #plt.scatter(x, y, c = 'red')
    
    #changed = np.where(glts.positions == glts.init_positions, np.nan, glts.positions)
    
    #yy, xx = changed.T
    #dy, dx = (glts.positions - glts.init_positions).T
    
    ##plt.arrow(0, 0, 20, 20, head_width = 2, ec = 'k', fc = 'k')
    #for i in range(len(xx)):
        #if not np.isnan(xx[i]):
            #plt.arrow(x[i], y[i], dx[i], dy[i],
                      #head_width=10, head_length=10, ec = 'r', fc = 'r')
    
            
    #plt.scatter(xx, yy, c = 'blue', s = 100)
    #plt.show()
    
    # Settle
    glts.dispersal(to_settle = True, 
                   maximum_distance=8000.0, 
                   who_can_replace='same_patch', landscape_map=landscape,
                   patch_id_map = var_maps['pid'],
                   patch_area_map = var_maps['patch_area'])
    
    
    # Test update
    glts.update(current_step = step, update_mortality=True)
    
    #print glts.alive
    #print glts.alive.shape
    #print glts.dead
    #print glts.dead_individual_id
    #print glts.dead_age
    
    #print glts.init_Nind
    #print glts.Nind
    print str(glts.init_Nind - glts.Nind)+' individuals died'
    
    #if (glts.init_Nind - glts.Nind) < 0:
        #break
    
    #print glts.init_group_sizes.shape[0]
    #print glts.Ngroups
    #print glts.Na
    #print glts.agent_id
    #print glts.home_range
    #print glts.max_agent_ID
    
    # Test mortality - age dependent
    #glts.mortality(mortality_rate=[0.05, 0.15], mortality_option='age_class', 
                  #age_classes=[5,glts.maximum_age])
    
    #print glts.alive
    #print glts.alive.shape
    #print glts.dead
    #print glts.dead_individual_id
    
    ## Test dispersal after mortality of reproducer
    #print glts.dead
    #print (glts.dead) & (glts.reproductive_status) # check if there will be dispersal
    
    #glts.dispersal(after_death_reproducer = True, who_can_replace='any')
    
    ## Settle if len(dispersing not dead ) > 0
    
    ## Test update
    #glts.update(current_step=2, update_mortality=True)
    
    #print glts.alive
    #print glts.alive.shape
    #print glts.dead
    #print glts.dead_individual_id
    #print glts.dead_age
    
    #print glts.init_Nind
    #print glts.Nind
    #print str(glts.init_Nind - glts.Nind)+' individuals died'
    
    # test reproduction
    if step % 9 == 0:
        glts.reproduction(simulation_step = 1, 
                          offspring_parameter='Poisson', offspring_size=[2])
        #glts.new_inds
    
        # Test update
        glts.update(current_step = step, update_reproduction = True)
    
    if glts.Nind <= 0:
        print 'population extinct!'
        break
    
    #glts.age
    #glts.sex
    #glts.sex.shape[0]
    #glts.Nind
    #glts.Na
    #glts.genetics




#----------------------------------
# test run a simulation through biodim_simulation class

python 

import os
import numpy as np
import grass.script as grass
    
pydir = r'/home/leecb/Github/biodim/py'
os.chdir(pydir)