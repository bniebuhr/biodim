import random
import re
import os
import grass.script as grass

def select_landscape_grassnames(select_form = 'random', previous_landscape = ''):
    '''This part read HABMAT file list and return the grassname
       for HABMAT, as well as the index for landscape matrix.
       After also return other grassnames to use used on simulations
    '''
    #.... grab HABMAT grassname and landscape index
       
    file_habmat=open("simulados_HABMAT.txt","r")
    habmat=file_habmat.readlines()
    file_habmat.close()
    if select_form == 'random':
        if previous_landscape == '':
            landscape_grassname_habmat=habmat[0].replace("\n","")
        else:
            landscape_grassname_habmat=random.sample(habmat, 1)[0].replace("\n","")
    elif select_form == 'order':              
        if previous_landscape == '' or previous_landscape == habmat[(len(habmat)-1)].replace("\n",""):
            landscape_grassname_habmat=habmat[0].replace("\n","")
        else:
            index = habmat.index(previous_landscape+'\n')
            landscape_grassname_habmat=habmat[(index+1)].replace("\n","")
    elif select_form == 'type':
        landscape_grassname_habmat=previous_landscape
    landscape_index=landscape_grassname_habmat[11:17]
    
    
    #.... return grassname for HABDIST (Distance from EDGE of habitat)
    #.... and on this case, distance are in PIXELS, where positive
    #.... values represent distance on MATRIX direction, and
    #.... negative values are on CORE direction
    ##simulation_000001_p029_h059_HABMAT_DIST
    file_habdist=open("simulados_HABMAT_DIST.txt","r")
    habdist=file_habdist.readlines()
    file_habdist.close()
    for i in habdist:
        if re.search(landscape_index, i):
            landscape_grassname_habdist=i.replace("\n","")


    #.... return grassname for HQMQLQ (HQ=High Quality;
    #.... MQ=Medium Quality and LQ=Low Quality
    ##simulation_000001_p029_h059_HQ026_MQ002_LQ070
    file_hqmqlq=open("simulados_HQMQLQ.txt","r")
    hqmqlq=file_hqmqlq.readlines()
    file_hqmqlq.close()
    for i in hqmqlq:
        if re.search(landscape_index, i):
            landscape_grassname_hqmqlq=i.replace("\n","")

    ##simulation_000001_p029_h059_HABMAT_grassclump_PID
    file_habmat_pid=open("simulados_HABMAT_grassclump_PID.txt","r")
    habmat_pid=file_habmat_pid.readlines()
    file_habmat_pid.close()
    for i in habmat_pid:
        if re.search(landscape_index, i):
            landscape_grassname_habmat_pid=i.replace("\n","")

    ##simulation_000001_p029_h059_HABMAT_grassclump_AREApix
    file_habmat_areapix=open("simulados_HABMAT_grassclump_AREApix.txt","r")
    habmat_areapix=file_habmat_areapix.readlines()
    file_habmat_areapix.close()
    for i in habmat_areapix:
        if re.search(landscape_index, i):
            landscape_grassname_habmat_areapix=i.replace("\n","")

    ##simulation_000001_p029_h059_HQMQLQ_quality
    file_hqmqlq_quality=open("simulados_HQMQLQ_quality.txt","r")
    hqmalq_quality=file_hqmqlq_quality.readlines()
    file_hqmqlq_quality.close()
    for i in hqmalq_quality:
        if re.search(landscape_index, i):
            landscape_grassname_hqmqlq_quality=i.replace("\n","")            

    ##simulation_000001_p029_h059_HQMQLQ_AREAqual
    file_hqmqlq_AREAqual=open("simulados_HQMQLQ_AREAqual.txt","r")
    hqmalq_AREAqual=file_hqmqlq_AREAqual.readlines()
    file_hqmqlq_AREAqual.close()
    for i in hqmalq_AREAqual:
        if re.search(landscape_index, i):
            landscape_grassname_hqmqlq_AREAqual=i.replace("\n","")            

    ##simulation_000001_p029_h059_HABMAT_FRAG_PID
    file_frag_pid=open("simulados_HABMAT_FRAC_PID.txt","r")
    frag_pid=file_frag_pid.readlines()
    file_frag_pid.close()
    for i in frag_pid:
        if re.search(landscape_index, i):
            landscape_grassname_frag_pid=i.replace("\n","")

    ##simulation_000001_p029_h059_HABMAT_FRAG_AREApix
    file_frag_AREApix=open("simulados_HABMAT_FRAC_AREApix.txt","r")
    frag_AREApix=file_frag_AREApix.readlines()
    file_frag_AREApix.close()
    for i in frag_AREApix:
        if re.search(landscape_index, i):
            landscape_grassname_frag_AREApix=i.replace("\n","")

    ##simulation_000001_p029_h059_HABMAT_FRAG_AREAqual
         ### USING THE SAME INPUT FILE AS AREApix!!!!
    landscape_grassname_frag_AREAqual=landscape_grassname_frag_AREApix.replace("AreaHA","AREAqualHA")

    
  
    ### STILLLL CHECK... Need I load COMPLETE maps?! yes !!!!
    #---------------------- DILA01
    ##simulation_000001_p029_h059_HABMAT_grassclump_dila01_clean_PID
    file_dila01clean_pid=open("simulados_HABMAT_grassclump_dila01_clean_PID.txt","r")
    dila01clean_pid=file_dila01clean_pid.readlines()
    file_dila01clean_pid.close()
    for i in dila01clean_pid:
        if re.search(landscape_index, i):
            landscape_grassname_dila01clean_pid=i.replace("\n","")
            
    ##simulation_000001_p029_h059_HABMAT_grassclump_dila01_complete_AREApix
    file_dila01clean_AREApix=open("simulados_HABMAT_grassclump_dila01_clean_AREApix.txt","r")
    dila01clean_AREApix=file_dila01clean_AREApix.readlines()
    file_dila01clean_AREApix.close()
    for i in dila01clean_AREApix:
        if re.search(landscape_index, i) and 'clean' in i:
            landscape_grassname_dila01clean_AREApix=i.replace("\n","")

    ##simulation_000001_p029_h059_HABMAT_DILA01_AREAqual
         ### USING THE SAME INPUT FILE AS AREApix!!!!
    landscape_grassname_dila01clean_AREAqual=landscape_grassname_dila01clean_AREApix#.replace("AreaHA","AREAqualHA")
    

    #---------------------- DILA02
    ##simulation_000001_p029_h059_HABMAT_grassclump_dila02_clean_PID
    file_dila02clean_pid=open("simulados_HABMAT_grassclump_dila02_clean_PID.txt","r")
    dila02clean_pid=file_dila02clean_pid.readlines()
    file_dila02clean_pid.close()
    for i in dila02clean_pid:
        if re.search(landscape_index, i):
            landscape_grassname_dila02clean_pid=i.replace("\n","")
            
    ##simulation_000001_p029_h059_HABMAT_grassclump_dila02_complete_AREApix
    file_dila02clean_AREApix=open("simulados_HABMAT_grassclump_dila02_clean_AREApix.txt","r")
    dila02clean_AREApix=file_dila02clean_AREApix.readlines()
    file_dila02clean_AREApix.close()
    for i in dila02clean_AREApix:
        if re.search(landscape_index, i) and 'clean' in i:
            landscape_grassname_dila02clean_AREApix=i.replace("\n","")

    ##simulation_000001_p029_h059_HABMAT_DILA02_AREAqual
         ### USING THE SAME INPUT FILE AS AREApix!!!!
    landscape_grassname_dila02clean_AREAqual=landscape_grassname_dila02clean_AREApix#.replace("AreaHA","AREAqualHA")
    
    return landscape_grassname_habmat, landscape_grassname_hqmqlq, landscape_grassname_habdist, landscape_grassname_habmat_pid, landscape_grassname_habmat_areapix, landscape_grassname_hqmqlq_quality, landscape_grassname_hqmqlq_AREAqual, landscape_grassname_frag_pid, landscape_grassname_frag_AREApix, landscape_grassname_frag_AREAqual, landscape_grassname_dila01clean_pid, landscape_grassname_dila01clean_AREApix, landscape_grassname_dila01clean_AREAqual, landscape_grassname_dila02clean_pid, landscape_grassname_dila02clean_AREApix, landscape_grassname_dila02clean_AREAqual


def select_landscape_grassnames_userbase(select_form = 'random', previous_landscape = ''):
    '''This part read HABMAT file list and return the grassname
       for HABMAT, as well as the index for landscape matrix.
       After also return other grassnames to use used on simulations
    '''
    #.... grab HABMAT grassname and landscape index
    ## lndscp_0001_Mapa0001_tif_HABMAT   
    file_habmat=open("simulados_HABMAT.txt","r")
    habmat=file_habmat.readlines()
    file_habmat.close()
    if select_form == 'random':
        if previous_landscape == '':
            landscape_grassname_habmat=habmat[0].replace("\n","")
        else:
            landscape_grassname_habmat=random.sample(habmat, 1)[0].replace("\n","")
    elif select_form == 'order':              
        if previous_landscape == '' or previous_landscape == habmat[(len(habmat)-1)].replace("\n",""):
            landscape_grassname_habmat=habmat[0].replace("\n","")
        else:
            index = habmat.index(previous_landscape+'\n')
            landscape_grassname_habmat=habmat[(index+1)].replace("\n","")
    elif select_form == 'type':
        if previous_landscape == '':
            landscape_grassname_habmat=habmat[0].replace("\n","")
        else:
            landscape_grassname_habmat=previous_landscape
    landscape_index=landscape_grassname_habmat[0:11]
    
    #.... return grassname for HABDIST (Distance from EDGE of habitat)
    #.... and on this case, distance are in PIXELS, where positive
    #.... values represent distance on MATRIX direction, and
    #.... negative values are on CORE direction
    ## lndscp_0001_Mapa0001_tif_HABMAT_dist
    file_habdist=open("simulados_HABMAT_DIST.txt","r")
    habdist=file_habdist.readlines()
    file_habdist.close()
    for i in habdist:
        if re.search(landscape_index, i):
            landscape_grassname_habdist=i.replace("\n","")

    ## lndscp_0001_Mapa0001_tif_HABMAT_patch_clump_mata_limpa_pid
    file_habmat_pid=open("simulados_HABMAT_grassclump_PID.txt","r")
    habmat_pid=file_habmat_pid.readlines()
    file_habmat_pid.close()
    for i in habmat_pid:
        if re.search(landscape_index, i):
            landscape_grassname_habmat_pid=i.replace("\n","")

    ## lndscp_0001_Mapa0001_tif_HABMAT_patch_clump_mata_limpa_AreaHA
    file_habmat_areapix=open("simulados_HABMAT_grassclump_AREApix.txt","r")
    habmat_areapix=file_habmat_areapix.readlines()
    file_habmat_areapix.close()
    for i in habmat_areapix:
        if re.search(landscape_index, i):
            landscape_grassname_habmat_areapix=i.replace("\n","")

    ## lndscp_0001_Mapa0001_tif_HABMAT_FRAG30m_mata_clump_pid
    file_frag_pid=open("simulados_HABMAT_FRAC_PID.txt","r")
    frag_pid=file_frag_pid.readlines()
    file_frag_pid.close()
    for i in frag_pid:
        if re.search(landscape_index, i):
            landscape_grassname_frag_pid=i.replace("\n","")

    ## lndscp_0001_Mapa0001_tif_HABMAT_FRAG30m_mata_clump_AreaHA
    file_frag_AREApix=open("simulados_HABMAT_FRAC_AREApix.txt","r")
    frag_AREApix=file_frag_AREApix.readlines()
    file_frag_AREApix.close()
    for i in frag_AREApix:
        if re.search(landscape_index, i):
            landscape_grassname_frag_AREApix=i.replace("\n","")   
  
    ### STILLLL CHECK... Need I load COMPLETE maps?! yes !!!!
    #---------------------- DILA01
    ## lndscp_0001_Mapa0001_tif_HABMAT_dila_30m_orig_clump_mata_limpa_pid
    file_dila01clean_pid=open("simulados_HABMAT_grassclump_dila01_clean_PID.txt","r")
    dila01clean_pid=file_dila01clean_pid.readlines()
    file_dila01clean_pid.close()
    for i in dila01clean_pid:
        if re.search(landscape_index, i):
            landscape_grassname_dila01clean_pid=i.replace("\n","")
            
    ## lndscp_0001_Mapa0001_tif_HABMAT_dila_30m_orig_clump_mata_limpa_AreaHA
    file_dila01clean_AREApix=open("simulados_HABMAT_grassclump_dila01_clean_AREApix.txt","r")
    dila01clean_AREApix=file_dila01clean_AREApix.readlines()
    file_dila01clean_AREApix.close()
    for i in dila01clean_AREApix:
        if re.search(landscape_index, i):
            landscape_grassname_dila01clean_AREApix=i.replace("\n","")   

    #---------------------- DILA02
    ## lndscp_0001_Mapa0001_tif_HABMAT_dila_60m_orig_clump_mata_limpa_pid
    file_dila02clean_pid=open("simulados_HABMAT_grassclump_dila02_clean_PID.txt","r")
    dila02clean_pid=file_dila02clean_pid.readlines()
    file_dila02clean_pid.close()
    for i in dila02clean_pid:
        if re.search(landscape_index, i):
            landscape_grassname_dila02clean_pid=i.replace("\n","")
            
    ## lndscp_0001_Mapa0001_tif_HABMAT_dila_60m_orig_clump_mata_limpa_AreaHA
    file_dila02clean_AREApix=open("simulados_HABMAT_grassclump_dila02_clean_AREApix.txt","r")
    dila02clean_AREApix=file_dila02clean_AREApix.readlines()
    file_dila02clean_AREApix.close()
    for i in dila02clean_AREApix:
        if re.search(landscape_index, i):
            landscape_grassname_dila02clean_AREApix=i.replace("\n","")
    
    return landscape_grassname_habmat, landscape_grassname_habdist, landscape_grassname_habmat_pid, landscape_grassname_habmat_areapix, landscape_grassname_frag_pid, landscape_grassname_frag_AREApix, landscape_grassname_dila01clean_pid, landscape_grassname_dila01clean_AREApix, landscape_grassname_dila02clean_pid, landscape_grassname_dila02clean_AREApix


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
    
    # Possible variables
    variables_options = ['edge_dist', 'pid', 'patch_area', 'fid', 'frag_area', 
                         'cross1_pid', 'cross1_patch_area', 'cross2_pid', 'cross2_patch_area']
    
    # Correspondent possible mapsets and possible patterns
    
    # If random maps will be used
    if use_random_landscapes:
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
        # Assessing the name of the current mapset - this may be used within the metrics functions
        current_mapset = grass.read_command('g.mapset', flags = 'p').replace('\n','').replace('\r','')        
        
        # Possible mapsets
        mapset_names = [current_mapset] * len(variables)
        
        # Possible patterns
        # complete later! see patterns from LSMetrics
    
    # For each variable
    for i in (variables):
        
        # If the variable is one of the possible ones
        if i in variables_options:
            
            # Get index of the variable i in the list of variable options
            index = variables_options.index(i)
            # Define the list of map names as a dictionary entry
            list_names[i] = grass.list_grouped('rast', pattern = possible_patterns[index]) [mapset_names[index]]
            
            # Check if the list has at least one map; otherwise there may be a problem
            if len(list_names[i]) == 0:
                raise Exception('There are no maps with the pattern '+possible_patterns[index]+' in the mapset '+mapset_names[index]+'! Please check it.')
            
        # If the variable in another, gives a warning
        else:
            raise Exception('There is some issue with maps related to variable '+i+'! Please check it.')
        
    return list_names   
        
    


