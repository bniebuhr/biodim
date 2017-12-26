#---------------------------------------------------
# Landscape functions for BioDIM
#---------------------------------------------------

# Import modules
import numpy as np
import warnings

# Import grass.script module, if within GRASS GIS
# Otherwise, maps must be created/loaded without GRASS
try:
    import grass.script as grass
    from grass.script import array as garray
except:
    warnings.warn('You are not inside GRASS GIS, so the functions leading with GRASS maps will not run.')

#---------------------------------------------------
# Functions for listing habitat and landscape variable map names within GRASS

def list_landscapes_habitat(use_random_landscapes = True, habmat_pattern = '*HABMAT'):
    '''
    New function: this function returns the list of landscapes in GRASS database locations
    
    Input:
    use_random_landscapes: if True, seach for maps in the GRASS database of random landscapes; otherwise, use real landscapes
    '''
    
    # If the user is going to use the database of random landscapes
    if use_random_landscapes:
        mapset_habmat = 'MS_HABMAT'
    # Or, if the user is going to use read landscapes
    else:
        # Assessing the name of the current mapset
        mapset_habmat = grass.read_command('g.mapset', flags = 'p').replace('\n','').replace('\r','')
        
    # List of maps of habitat
    list_binary_maps = grass.list_grouped('rast', pattern = habmat_pattern) [mapset_habmat]
    
    return list_binary_maps


def list_landscape_variables(use_random_landscapes = True, variables = []):
    
    '''
    New function: this function returns the list of landscapes in GRASS database locations
    
    Input:
    use_random_landscapes: if True, seach for maps in the GRASS database of random landscapes; otherwise, use real landscapes
    variables: variables to be registered. Options: 'edge_dist', 'pid', 'patch_area', 'fid', 'frag_area', 'cross1_pid', 'cross1_patch_area', 'cross2_pid', 'cross2_patch_area'
    '''
        
    # Lists of landscape variable names
    list_names = {}
    list_types = {}
    list_mapsets = {}
    
    # Correspondent possible mapsets and possible patterns
    
    # If random maps will be used
    if use_random_landscapes:
        # Possible variables
        variables_options = ['edge_dist', 'pid', 'patch_area', 'fid', 'frag_area', 
                             'cross1_pid', 'cross1_patch_area', 'cross2_pid', 'cross2_patch_area']
            
        # Types of variable
        variable_types = [np.float64, np.int64, np.int64, np.int64, np.int64,
                          np.int64, np.int64, np.int64, np.int64]        
        
        # Possible mapsets
        mapset_names = ['MS_HABMAT_DIST', 'MS_HABMAT_PID', 'MS_HABMAT_AREA', 
                        'MS_HABMAT_FRAG_PID', 'MS_HABMAT_FRAG_AREA',
                        'MS_HABMAT_DILA01_PID', 'MS_HABMAT_DILA01_AREA',
                        'MS_HABMAT_DILA02_PID', 'MS_HABMAT_DILA02_AREA']
        
        # Possible patterns
        possible_patterns = ['*DIST', '*PID', '*grassclump_AreaHA', '*FRAG_PID', '*FRAG_AreaHA',
                             '*dila01_clean_PID', '*dila01_clean_AreaHA', '*dila02_clean_AreaHA', '*dila02_clean_AreaHA']
        # update possibilities of quality etc for BioDIM birds
    
    # If real maps will be used
    else:
        # Possible variables
        variables_options = ['edge_dist', 'pid', 'patch_area', 'fid', 'frag_area', 
                             'cross_pid', 'cross_patch_area']#, 'cross2_pid', 'cross2_patch_area']
        
        # Types of variable
        variable_types = [np.float64, np.int64, np.int64, np.int64, np.int64,
                          np.int64, np.int64]#, np.int64, np.int64]
        
        # Assessing the name of the current mapset - this may be used within the metrics functions
        current_mapset = grass.read_command('g.mapset', flags = 'p').replace('\n','').replace('\r','')        
        
        # Possible mapsets
        mapset_names = [current_mapset] * len(variables_options)
        
        # Possible patterns
        possible_patterns = ['*edge_dist', '*HABMAT_pid', '*patch_AreaHA', '*fid', '*fragment_AreaHA',
                             '*func_connect_pid', '*func_connect_AreaHA']#, '*dila02_clean_AreaHA', '*dila02_clean_AreaHA']
    
    
    # For each variable
    for i in variables:
        
        # If the variable is one of the possible ones
        if i in variables_options:
            
            # Get index of the variable i in the list of variable options
            index = variables_options.index(i)
            # Define the list of map names as a dictionary entry
            list_names[i] = grass.list_grouped('rast', pattern = possible_patterns[index]) [mapset_names[index]]
            # Define the type of variable to be loaded
            list_types[i] = variable_types[index]
            # Difine mapset
            list_mapsets[i] = mapset_names[index]
            
            # Check if the list has at least one map; otherwise there may be a problem
            if len(list_names[i]) == 0:
                raise Exception('There are no maps with the pattern '+possible_patterns[index]+' in the mapset '+mapset_names[index]+'! Please check it.')
            
        # If the variable in another, gives a warning
        else:
            raise Exception('There is some issue with maps related to variable '+i+'! Please check it.')
        
    return (list_names, list_types, list_mapsets)


#---------------------------------------------------
# Functions for choosing one habitat and some related landscape variable maps from GRASS

def pickup_one_landscape_garray(select_form = 'random', previous_landscape = '', list_habitat_maps = [], 
                                null = 0, null_nan = False, exportPNG = True):
    '''
    exportPNG not implemented yet
    '''

    # Check if a list of habitat maps was passed as input
    if len(list_habitat_maps) == 0:
        raise Exception('You need to first load the list of habitat maps.')

    # Select a landscape name from the list of habitat map names:

    # If select_form == random, pick up a random map (the first if no one was chosen before)
    if select_form == 'random':
        if previous_landscape == '':
            habitat_map_name = list_habitat_maps[0]
        else:
            habitat_map_name = random.sample(list_habitat_maps, 1)[0]
    # If select_form == order, pick up the next one in the list (the first if no one was chosen before or if it is the last one)
    elif select_form == 'order':              
        if previous_landscape == '' or previous_landscape == list_habitat_maps[(len(list_habitat_maps)-1)]:
            habitat_map_name = list_habitat_maps[0]
        else:
            index = list_habitat_maps.index(previous_landscape)
            habitat_map_name = list_habitat_maps[(index+1)]
    # If select_form == type, pick up the a fixed landscape typed by the user (always the same)
    elif select_form == 'same':
        habitat_map_name = previous_landscape
    else:
        raise Exception('You must select a landscape according to random, order, or type rule.')

    # Now, load it using grass.script.array

    # Define region
    grass.run_command('g.region', raster = habitat_map_name)

    # Load map
    landscape_map = garray.array(dtype = np.int8)
    landscape_map.read(habitat_map_name, null = null)
    
    if null_nan:
        landscape_map = np.where(landscape_map == null, np.nan, landscape_map)    

    return habitat_map_name, landscape_map

def pickup_landscape_variables(habitat_map_name, variables = [], list_variable_maps = {}, 
                               variable_types = {}, variable_mapsets = {}, null = 0, null_nan = False, exportPNG = True):
    '''
    exportPNG not implemented yet
    '''

    # Check if a list of variables and a list of names of map variables was passed as input
    if len(variables) == 0 or len(list_variable_maps) == 0:
        raise Exception('You need to first load the variables and the list of variable maps.')

    # Initialize dictionary of variable names and maps
    landscape_variable_map_names = {}
    landscape_variable_maps = {}

    # Define region
    grass.run_command('g.region', raster = habitat_map_name)    

    # Select variables according to the habitat map name
    for i in variables:

        try:
            landscape_variable_map_names[i] = [name for name in list_variable_maps[i] if habitat_map_name in name][0]
            var_type = variable_types[i]
            mapset = variable_mapsets[i]
        except:
            raise Exception('There is no map with a pattern '+habitat_map_name+' in the list of maps for variable '+i+'. Please check it.')

        # Initialize grass.array and read it from GRASS into a numpy array
        landscape_variable_maps[i] = garray.array()#(dtype = var_type)
        landscape_variable_maps[i].read(landscape_variable_map_names[i]+'@'+mapset, null = null)
        print 'Loading spatial variables: '+landscape_variable_map_names[i]        
        
        if null_nan:
            landscape_variable_maps[i] = np.where(landscape_variable_maps[i] == null, np.nan, landscape_variable_maps[i])

    return landscape_variable_map_names, landscape_variable_maps


#---------------------------------------------------
# Functions for getting information about landscape and spatial variables

def get_habitat_prop_cells(landscape_map, habitat_val = 1):
    '''
    This function returns the percentage of habitat/forest in the landscape and which cells (row,col)
    of the map correspond to habitat/forest. This function is equal to getForest, but designed to 
    user (real) maps that do not have quality on it. It is based on a binary map of habitat (1) 
    matrix (0) only.
    This function uses numpy arrays instead of python lists.
    Input:
    - landscape_matrix: table/map of habitat, considering 1 = forest and 0 = matrix.
    Ouput:
    - pland: percentage of habitat/forest in the landscape
    - forest: sequence of cells (row, column) that correspond to habitat/forest
    
    implement the quality later
    '''    

    # Take indexes of habitat cells
    ind_habitat_cells = np.where(landscape_map == habitat_val)
    # Transform those indexes in an array of dimension (n_cells, 2), in which
    # cols = [row, column] of the landscape_map
    habitat_cells_sorted = np.vstack(ind_habitat_cells).transpose()
    
    # Get proportion of habitat in the landscape
    n_habitat = len(habitat_cells_sorted)
    
    prop_habitat = float(n_habitat)/landscape_map.size
    
    return prop_habitat, habitat_cells_sorted

def np_getForest_habmat(landscape_matrix):
    '''
    This function returns the percentage of habitat/forest in the landscape and which cells (row,col)
    of the map correspond to habitat/forest. This function is equal to getForest, but designed to 
    user (real) maps that do not have quality on it. It is based on a binary map of habitat (1) 
    matrix (0) only.
    This function uses numpy arrays instead of python lists.
    Input:
    - landscape_matrix: table/map of habitat, considering 1 = forest and 0 = matrix.
    Ouput:
    - pland: percentage of habitat/forest in the landscape
    - forest: sequence of cells (row, column) that correspond to habitat/forest
    '''    

    forest = []
    cont = 0.0
    for row in range(len(landscape_matrix)):
        for col in range(len(landscape_matrix[0])):
            feature = landscape_matrix[row][col]
            if feature == 1: 
                forest.append([row,col])
                cont += 1
                
    pland = int(100*cont/float(len(landscape_matrix)*len(landscape_matrix[0])))
    
    return pland, forest

