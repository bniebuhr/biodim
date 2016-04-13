import random
import re
import os

def select_landscape_grassnames():
    '''This part read HABMAT file list and return the grassname
       for HABMAT, as well as the index for landscape matrix.
       After also return other grassnames to use used on simulations
    '''
    #.... grab HABMAT grassname and landscape index
       
    file_habmat=open("simulados_HABMAT.txt","r")
    habmat=file_habmat.readlines()
    file_habmat.close()
    landscape_grassname_habmat=random.sample(habmat, 1)[0].replace("\n","")
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


def select_landscape_grassnames_userbase():
    '''This part read HABMAT file list and return the grassname
       for HABMAT, as well as the index for landscape matrix.
       After also return other grassnames to use used on simulations
    '''
    #.... grab HABMAT grassname and landscape index
    ## lndscp_0001_Mapa0001_tif_HABMAT   
    file_habmat=open("simulados_HABMAT.txt","r")
    habmat=file_habmat.readlines()
    file_habmat.close()
    landscape_grassname_habmat=random.sample(habmat, 1)[0].replace("\n","")
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
