# BioDIM GLT

# Import modules
import os
import grass.script as grass

pydir = r'/home/leecb/Github/biodim/py'
os.chdir(pydir)
from select_landscape_grassnames import list_landscapes_habitat, list_landscape_variables
from pickup_one_landscape import pickup_one_landscape_garray, pickup_landscape_variables

#INITIALIZE LANDSCAPE - CLASS OR function

class Environment():
    
    def __init__(self, use_random_landscapes = True, habmat_pattern = '*HABMAT',
                 select_form = 'random', previous_landscape = '',
                 landscape_variables = [],
                 exportPNG = True):
        
        # List of habitat map names
        self.list_habitat_map_names = list_landscapes_habitat(use_random_landscapes = use_random_landscapes, habmat_pattern = habmat_pattern)
        
        # Pick up one
        self.landscape_name, self.landscape_map = pickup_one_landscape_garray(select_form = select_form, previous_landscape = previous_landscape, list_habitat_maps = self.list_habitat_map_names,
                                                                          exportPNG = exportPNG)
        # Update 'previous' landscape
        self.previous_landscape = self.landscape_name
        
        # List of variable maps
        self.list_variable_map_names = list_landscape_variables(use_random_landscapes = use_random_landscapes, variables = landscape_variables)
        
        # Pick up variables for the chosen map
        self.landscape_variable_map_names, self.landscape_variable_maps = pickup_landscape_variables(habitat_map_name = self.landscape_name, variables = landscape_variables, list_variable_maps = self.list_variable_map_names, 
                                                                                           exportPNG = exportPNG)
        
        
        
    
    