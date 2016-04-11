from select_landscape_grassnames import *
from export_raster_from_grass import *
from read_landscape_head_ascii_standard import read_landscape_head_ascii_standard

def pickup_one_landscape(defaultDir, inputDir, tempDir, userbasemap = False, exportPNG = True):
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
        landscape_grassname_habmat, landscape_grassname_habdist, landscape_grassname_habmat_pid, landscape_grassname_habmat_areapix, landscape_grassname_frag_pid, landscape_grassname_frag_AREApix, landscape_grassname_dila01clean_pid, landscape_grassname_dila01clean_AREApix, landscape_grassname_dila02clean_pid, landscape_grassname_dila02clean_AREApix=select_landscape_grassnames_userbase()
                
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
        landscape_grassname_habmat, landscape_grassname_hqmqlq, landscape_grassname_habdist, landscape_grassname_habmat_pid, landscape_grassname_habmat_areapix, landscape_grassname_hqmqlq_quality, landscape_grassname_hqmqlq_AREAqual, landscape_grassname_frag_pid, landscape_grassname_frag_AREApix,landscape_grassname_frag_AREAqual,landscape_grassname_dila01clean_pid,landscape_grassname_dila01clean_AREApix,landscape_grassname_dila01clean_AREAqual,landscape_grassname_dila02clean_pid,landscape_grassname_dila02clean_AREApix,landscape_grassname_dila02clean_AREAqual=select_landscape_grassnames()
     
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
