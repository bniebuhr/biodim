import grass.script as grass
import platform

from select_landscape_grassnames import *
from export_raster_from_grass import *
from read_landscape_head_ascii_standard import read_landscape_head_ascii_standard

def pickup_one_landscape(defaultDir, inputDir, tempDir, select_form = 'random', previous_landscape = '', userbasemap = False, exportPNG = True):
    '''
    This function select one random landscape from the Spatial Data Base (if userbasemap = False)
    or from the User Defined Data Base, export ascii and png files for each of them,
    reads ascii files, and transforms it into matrices
    Input:
    - defaultDir: parent directory where all BioDIM directories are in
    - inputDir: directory of input files
    - tempDir: directory of temp files (ascii and png files are written here)
    - userbasemap: boolean variable stating if Spatial Internal Data Base (=False) or User Defined Data Base (=True) will be used
    Output:
    - ... a lot of files
    '''
    
    if userbasemap: 
        os.chdir(defaultDir)
        os.chdir(inputDir)
        landscape_grassname_habmat, landscape_grassname_habdist, landscape_grassname_habmat_pid, landscape_grassname_habmat_areapix, landscape_grassname_frag_pid, landscape_grassname_frag_AREApix, landscape_grassname_dila01clean_pid, landscape_grassname_dila01clean_AREApix, landscape_grassname_dila02clean_pid, landscape_grassname_dila02clean_AREApix=select_landscape_grassnames_userbase(select_form=select_form, previous_landscape=previous_landscape)
                
        export_raster_from_grass_userbase(landscape_grassname_habmat, landscape_grassname_habdist, landscape_grassname_habmat_pid, landscape_grassname_habmat_areapix, landscape_grassname_frag_pid, landscape_grassname_frag_AREApix, landscape_grassname_dila01clean_pid, landscape_grassname_dila01clean_AREApix, landscape_grassname_dila02clean_pid, landscape_grassname_dila02clean_AREApix, defaultDir, inputDir, tempDir, exportPNG=exportPNG)
        
        landscape_head, landscape_matrix=read_landscape_head_ascii_standard('random_landscape_habmat.asc',"int") # mudei essa linha para ler do habmat
        landscape_head, landscape_habdist=read_landscape_head_ascii_standard('random_landscape_habdist.asc',"float")
        landscape_head, landscape_habmat_pid=read_landscape_head_ascii_standard('random_landscape_habmat_pid.asc',"long")
        landscape_head, landscape_habmat_areapix=read_landscape_head_ascii_standard('random_landscape_habmat_areapix.asc',"long")        
        #landscape_head, landscape_hqmqlq_quality=read_landscape_head_ascii_standard('random_landscape_hqmqlq_quality.asc',"int")        
        #landscape_head, landscape_hqmqlq_AREAqual=read_landscape_head_ascii_standard('random_landscape_hqmqlq_AREAqual.asc',"long")
        
        #------------------------
        landscape_head, landscape_frag_pid=read_landscape_head_ascii_standard('random_landscape_frag_pid.asc',"int")        
        landscape_head, landscape_frag_AREApix=read_landscape_head_ascii_standard('random_landscape_frag_AREApix.asc',"long")
        #landscape_head, landscape_frag_AREAqual=read_landscape_head_ascii_standard('random_landscape_frag_AREAqual.asc',"long")
    
        #------------------------
        landscape_head, landscape_dila01clean_pid=read_landscape_head_ascii_standard('random_landscape_dila01clean_pid.asc',"int")        
        landscape_head, landscape_dila01clean_AREApix=read_landscape_head_ascii_standard('random_landscape_dila01clean_AREApix.asc',"long")
        #landscape_head, landscape_dila01clean_AREAqual=read_landscape_head_ascii_standard('random_landscape_dila01clean_AREAqual.asc',"long")
    
        #------------------------
        landscape_head, landscape_dila02clean_pid=read_landscape_head_ascii_standard('random_landscape_dila02clean_pid.asc',"int")        
        landscape_head, landscape_dila02clean_AREApix=read_landscape_head_ascii_standard('random_landscape_dila02clean_AREApix.asc',"long")
        #landscape_head, landscape_dila02clean_AREAqual=read_landscape_head_ascii_standard('random_landscape_dila02clean_AREAqual.asc',"long")  
        
        return landscape_head, landscape_matrix, landscape_grassname_habmat, landscape_habdist, landscape_habmat_pid, landscape_habmat_areapix, landscape_frag_pid, landscape_frag_AREApix, landscape_dila01clean_pid, landscape_dila01clean_AREApix, landscape_dila02clean_pid, landscape_dila02clean_AREApix
    else:
        os.chdir(defaultDir)
        os.chdir(inputDir)        
        landscape_grassname_habmat, landscape_grassname_hqmqlq, landscape_grassname_habdist, landscape_grassname_habmat_pid, landscape_grassname_habmat_areapix, landscape_grassname_hqmqlq_quality, landscape_grassname_hqmqlq_AREAqual, landscape_grassname_frag_pid, landscape_grassname_frag_AREApix,landscape_grassname_frag_AREAqual,landscape_grassname_dila01clean_pid,landscape_grassname_dila01clean_AREApix,landscape_grassname_dila01clean_AREAqual,landscape_grassname_dila02clean_pid,landscape_grassname_dila02clean_AREApix,landscape_grassname_dila02clean_AREAqual=select_landscape_grassnames(select_form=select_form, previous_landscape=previous_landscape)
     
        export_raster_from_grass(landscape_grassname_habmat, landscape_grassname_hqmqlq, landscape_grassname_habdist, landscape_grassname_habmat_pid, landscape_grassname_habmat_areapix, landscape_grassname_hqmqlq_quality, landscape_grassname_hqmqlq_AREAqual, landscape_grassname_frag_pid, landscape_grassname_frag_AREApix, landscape_grassname_frag_AREAqual, landscape_grassname_dila01clean_pid, landscape_grassname_dila01clean_AREApix, landscape_grassname_dila01clean_AREAqual, landscape_grassname_dila02clean_pid, landscape_grassname_dila02clean_AREApix, landscape_grassname_dila02clean_AREAqual, defaultDir, inputDir, tempDir, exportPNG=exportPNG)
    
        landscape_head, landscape_matrix=read_landscape_head_ascii_standard('random_landscape_hqmqlq.asc',"int")
        landscape_head, landscape_habdist=read_landscape_head_ascii_standard('random_landscape_habdist.asc',"float")
        landscape_head, landscape_habmat_pid=read_landscape_head_ascii_standard('random_landscape_habmat_pid.asc',"long")
        landscape_head, landscape_habmat_areapix=read_landscape_head_ascii_standard('random_landscape_habmat_areapix.asc',"long")        
        landscape_head, landscape_hqmqlq_quality=read_landscape_head_ascii_standard('random_landscape_hqmqlq_quality.asc',"int")        
        landscape_head, landscape_hqmqlq_AREAqual=read_landscape_head_ascii_standard('random_landscape_hqmqlq_AREAqual.asc',"long")
        
        #------------------------
        landscape_head, landscape_frag_pid=read_landscape_head_ascii_standard('random_landscape_frag_pid.asc',"int")        
        landscape_head, landscape_frag_AREApix=read_landscape_head_ascii_standard('random_landscape_frag_AREApix.asc',"long")
        landscape_head, landscape_frag_AREAqual=read_landscape_head_ascii_standard('random_landscape_frag_AREAqual.asc',"long")
    
        #------------------------
        landscape_head, landscape_dila01clean_pid=read_landscape_head_ascii_standard('random_landscape_dila01clean_pid.asc',"int")        
        landscape_head, landscape_dila01clean_AREApix=read_landscape_head_ascii_standard('random_landscape_dila01clean_AREApix.asc',"long")
        landscape_head, landscape_dila01clean_AREAqual=read_landscape_head_ascii_standard('random_landscape_dila01clean_AREAqual.asc',"long")
    
        #------------------------
        landscape_head, landscape_dila02clean_pid=read_landscape_head_ascii_standard('random_landscape_dila02clean_pid.asc',"int")        
        landscape_head, landscape_dila02clean_AREApix=read_landscape_head_ascii_standard('random_landscape_dila02clean_AREApix.asc',"long")
        landscape_head, landscape_dila02clean_AREAqual=read_landscape_head_ascii_standard('random_landscape_dila02clean_AREAqual.asc',"long")
        return landscape_head, landscape_matrix, landscape_grassname_habmat, landscape_habdist, landscape_habmat_pid, landscape_habmat_areapix, landscape_hqmqlq_quality, landscape_hqmqlq_AREAqual, landscape_frag_pid, landscape_frag_AREApix,landscape_frag_AREAqual, landscape_dila01clean_pid, landscape_dila01clean_AREApix,landscape_dila01clean_AREAqual, landscape_dila02clean_pid, landscape_dila02clean_AREApix,landscape_dila02clean_AREAqual

def pickup_one_landscape_sep(defaultDir, inputDir, tempDir, select_form = 'random', previous_landscape = '', sp_profile = '', userbasemap = False, usegrid = False, x_col = '', y_row = '', dims = '', exportPNG = True):
    '''
    This function select one random landscape from the Spatial Data Base (if userbasemap = False)
    or from the User Defined Data Base, export ascii and png files for each of them,
    reads ascii files, and transforms it into matrices
    Input:
    - defaultDir: parent directory where all BioDIM directories are in
    - inputDir: directory of input files
    - tempDir: directory of temp files (ascii and png files are written here)
    - userbasemap: boolean variable stating if Spatial Internal Data Base (=False) or User Defined Data Base (=True) will be used
    Output:
    - ... a lot of files
    '''
    
    if userbasemap:         
        if sp_profile == '':
            os.chdir(defaultDir)
            os.chdir(inputDir)
            landscape_grassname_habmat, landscape_grassname_habdist, landscape_grassname_habmat_pid, landscape_grassname_habmat_areapix, landscape_grassname_frag_pid, landscape_grassname_frag_AREApix, landscape_grassname_dila01clean_pid, landscape_grassname_dila01clean_AREApix, landscape_grassname_dila02clean_pid, landscape_grassname_dila02clean_AREApix=select_landscape_grassnames_userbase(select_form=select_form, previous_landscape=previous_landscape)
        
            export_raster_from_grass_userbase(landscape_grassname_habmat, landscape_grassname_habdist, landscape_grassname_habmat_pid, landscape_grassname_habmat_areapix, landscape_grassname_frag_pid, landscape_grassname_frag_AREApix, landscape_grassname_dila01clean_pid, landscape_grassname_dila01clean_AREApix, landscape_grassname_dila02clean_pid, landscape_grassname_dila02clean_AREApix, defaultDir, inputDir, tempDir, exportPNG=exportPNG, usegrid=usegrid, x_col = x_col, y_row = y_row, dims=dims)
            
            landscape_head, landscape_matrix=read_landscape_head_ascii_standard('random_landscape_habmat.asc',"int") # mudei essa linha para ler do habmat
            landscape_head, landscape_habdist=read_landscape_head_ascii_standard('random_landscape_habdist.asc',"float")
            return landscape_head, landscape_matrix, landscape_grassname_habmat, landscape_habdist
        elif sp_profile == 'Habitat dependent':
            os.chdir(defaultDir)
            os.chdir(tempDir)            
            landscape_head, landscape_habmat_pid=read_landscape_head_ascii_standard('random_landscape_habmat_pid.asc',"long")
            landscape_head, landscape_habmat_areapix=read_landscape_head_ascii_standard('random_landscape_habmat_areapix.asc',"long")
            #landscape_head, landscape_hqmqlq_quality=read_landscape_head_ascii_standard('random_landscape_hqmqlq_quality.asc',"int")        
            #landscape_head, landscape_hqmqlq_AREAqual=read_landscape_head_ascii_standard('random_landscape_hqmqlq_AREAqual.asc',"long")
            return landscape_habmat_pid, landscape_habmat_areapix
        #------------------------
        elif sp_profile == 'Frag. dependent' or sp_profile == 'Core dependent':
            os.chdir(defaultDir)
            os.chdir(tempDir)            
            landscape_head, landscape_frag_pid=read_landscape_head_ascii_standard('random_landscape_frag_pid.asc',"int")        
            landscape_head, landscape_frag_AREApix=read_landscape_head_ascii_standard('random_landscape_frag_AREApix.asc',"long")
            #landscape_head, landscape_frag_AREAqual=read_landscape_head_ascii_standard('random_landscape_frag_AREAqual.asc',"long")
            return landscape_frag_pid, landscape_frag_AREApix
        #------------------------
        elif sp_profile == 'Moderately generalist':
            os.chdir(defaultDir)
            os.chdir(tempDir)            
            landscape_head, landscape_dila01clean_pid=read_landscape_head_ascii_standard('random_landscape_dila01clean_pid.asc',"int")        
            landscape_head, landscape_dila01clean_AREApix=read_landscape_head_ascii_standard('random_landscape_dila01clean_AREApix.asc',"long")
            #landscape_head, landscape_dila01clean_AREAqual=read_landscape_head_ascii_standard('random_landscape_dila01clean_AREAqual.asc',"long")
            return landscape_dila01clean_pid, landscape_dila01clean_AREApix
        #------------------------
        elif sp_profile == 'Highly generalist':
            os.chdir(defaultDir)
            os.chdir(tempDir)            
            landscape_head, landscape_dila02clean_pid=read_landscape_head_ascii_standard('random_landscape_dila02clean_pid.asc',"int")        
            landscape_head, landscape_dila02clean_AREApix=read_landscape_head_ascii_standard('random_landscape_dila02clean_AREApix.asc',"long")
            #landscape_head, landscape_dila02clean_AREAqual=read_landscape_head_ascii_standard('random_landscape_dila02clean_AREAqual.asc',"long")  
            return landscape_dila02clean_pid, landscape_dila02clean_AREApix
    
    else:    
        if sp_profile == '':
            os.chdir(defaultDir)
            os.chdir(inputDir)        
            landscape_grassname_habmat, landscape_grassname_hqmqlq, landscape_grassname_habdist, landscape_grassname_habmat_pid, landscape_grassname_habmat_areapix, landscape_grassname_hqmqlq_quality, landscape_grassname_hqmqlq_AREAqual, landscape_grassname_frag_pid, landscape_grassname_frag_AREApix,landscape_grassname_frag_AREAqual,landscape_grassname_dila01clean_pid,landscape_grassname_dila01clean_AREApix,landscape_grassname_dila01clean_AREAqual,landscape_grassname_dila02clean_pid,landscape_grassname_dila02clean_AREApix,landscape_grassname_dila02clean_AREAqual=select_landscape_grassnames(select_form=select_form, previous_landscape=previous_landscape)
        
            export_raster_from_grass(landscape_grassname_habmat, landscape_grassname_hqmqlq, landscape_grassname_habdist, landscape_grassname_habmat_pid, landscape_grassname_habmat_areapix, landscape_grassname_hqmqlq_quality, landscape_grassname_hqmqlq_AREAqual, landscape_grassname_frag_pid, landscape_grassname_frag_AREApix, landscape_grassname_frag_AREAqual, landscape_grassname_dila01clean_pid, landscape_grassname_dila01clean_AREApix, landscape_grassname_dila01clean_AREAqual, landscape_grassname_dila02clean_pid, landscape_grassname_dila02clean_AREApix, landscape_grassname_dila02clean_AREAqual, defaultDir, inputDir, tempDir, exportPNG=exportPNG)

            landscape_head, landscape_matrix=read_landscape_head_ascii_standard('random_landscape_hqmqlq.asc',"int")
            landscape_head, landscape_habdist=read_landscape_head_ascii_standard('random_landscape_habdist.asc',"float")
            landscape_head, landscape_hqmqlq_quality=read_landscape_head_ascii_standard('random_landscape_hqmqlq_quality.asc',"int")                    
            return landscape_head, landscape_matrix, landscape_grassname_habmat, landscape_habdist, landscape_hqmqlq_quality
        elif sp_profile == 'Habitat dependent':
            os.chdir(defaultDir)
            os.chdir(tempDir)            
            landscape_head, landscape_habmat_pid=read_landscape_head_ascii_standard('random_landscape_habmat_pid.asc',"long")
            landscape_head, landscape_habmat_areapix=read_landscape_head_ascii_standard('random_landscape_habmat_areapix.asc',"long")        
            landscape_head, landscape_hqmqlq_AREAqual=read_landscape_head_ascii_standard('random_landscape_hqmqlq_AREAqual.asc',"long")
            return landscape_habmat_pid, landscape_habmat_areapix, landscape_hqmqlq_AREAqual
        #------------------------
        elif sp_profile == 'Frag. dependent' or sp_profile == 'Core dependent':
            os.chdir(defaultDir)
            os.chdir(tempDir)            
            landscape_head, landscape_frag_pid=read_landscape_head_ascii_standard('random_landscape_frag_pid.asc',"int")        
            landscape_head, landscape_frag_AREApix=read_landscape_head_ascii_standard('random_landscape_frag_AREApix.asc',"long")
            landscape_head, landscape_frag_AREAqual=read_landscape_head_ascii_standard('random_landscape_frag_AREAqual.asc',"long")
            return landscape_frag_pid, landscape_frag_AREApix,landscape_frag_AREAqual
        #------------------------
        elif sp_profile == 'Moderately generalist':
            os.chdir(defaultDir)
            os.chdir(tempDir)            
            landscape_head, landscape_dila01clean_pid=read_landscape_head_ascii_standard('random_landscape_dila01clean_pid.asc',"int")        
            landscape_head, landscape_dila01clean_AREApix=read_landscape_head_ascii_standard('random_landscape_dila01clean_AREApix.asc',"long")
            landscape_head, landscape_dila01clean_AREAqual=read_landscape_head_ascii_standard('random_landscape_dila01clean_AREAqual.asc',"long")
            return landscape_dila01clean_pid, landscape_dila01clean_AREApix,landscape_dila01clean_AREAqual
        #------------------------
        elif sp_profile == 'Highly generalist':
            os.chdir(defaultDir)
            os.chdir(tempDir)            
            landscape_head, landscape_dila02clean_pid=read_landscape_head_ascii_standard('random_landscape_dila02clean_pid.asc',"int")        
            landscape_head, landscape_dila02clean_AREApix=read_landscape_head_ascii_standard('random_landscape_dila02clean_AREApix.asc',"long")
            landscape_head, landscape_dila02clean_AREAqual=read_landscape_head_ascii_standard('random_landscape_dila02clean_AREAqual.asc',"long")
            return landscape_dila02clean_pid, landscape_dila02clean_AREApix,landscape_dila02clean_AREAqual

def pickup_one_cell(cell_index_list, cell_id_string, cell_x_col, cell_y_row, select_form = 'random', previous_index = ''):
    
    if select_form == 'random':
        if previous_index == '':
            cell_index=cell_index_list[0]
        else:
            cell_index=random.sample(cell_index_list, 1)[0]
    elif select_form == 'order':              
        if previous_index == '' or previous_index == cell_index_list[(len(cell_index_list)-1)]:
            cell_index=cell_index_list[0]
        else:
            cell_index = previous_index+1
    elif select_form == 'type':
        cell_index=previous_index
        
    return cell_index, cell_id_string[cell_index], cell_x_col[cell_index], cell_y_row[cell_index]

def get_landscape_centers(mapa, cols):
    
    cells_aux = grass.read_command('v.db.select', map=mapa, columns=cols, separator='comma')
    if platform.system() == 'Windows':
        cells_aux2 = cells_aux.split('\r\n')
    elif platform.system() == 'Linux':
        cells_aux2 = cells_aux.split('\n') # maybe the problem is because we are running grass 7.0.4 on linux - check that later
    else:
        # colocar Mac OS depois
        raise Exception("What platform is yours?? It's not Windows or Linux...")
    cells_aux2 = cells_aux2[1:len(cells_aux2)-2] # first and last items are not cells

    #cat = []
    ID = []
    x_col = []
    y_row = []
    foco = []
    for j in cells_aux2:
        i = j.split(',')
        #if i[0] == '1': print i
        #cat.append(int(i[0]))
        ID.append(i[0])
        x_col.append(float(i[1]))
        y_row.append(float(i[2]))
        foco.append(int(i[3]))
        
    indices = [i for i, v in enumerate(foco) if v == 1]
    
    index = range(len(indices))
    #cat = [cat[i] for i in indices]
    ID = [ID[i] for i in indices]
    x_col = [x_col[i] for i in indices]
    y_row = [y_row[i] for i in indices]
    
    #return index, cat, ID, x_col, y_row
    return index, ID, x_col, y_row
