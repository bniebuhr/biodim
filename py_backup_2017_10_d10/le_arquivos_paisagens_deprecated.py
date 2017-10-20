import random, re
#---------------------------------------------------
def select_landscape_grassnames():
    '''This part read HABMAT file list and return the grassname
       for HABMAT, as well as the index for landscape matrix.
       After also return other grassnames to use used on simulations
    '''
    #.... grab HABMAT grassname and landscape index
    file_habmat=open("_HQ_simulados.txt","r")
    habmat=file_habmat.readlines()
    file_habmat.close()
    landscape_grassname_habmat=random.sample(habmat, 1)[0].replace(".txt\n","")
    landscape_index=landscape_grassname_habmat[14:20]

    #.... return grassname for HIQMAT (high quality - matrix)
    file_hqmat=open("_MQ_simulados.txt","r")
    hqmat=file_hqmat.readlines()
    file_hqmat.close()
    
    for i in hqmat:
        if re.search(landscape_index, i):
            landscape_grassname_hiqmat=i.replace(".txt\n","")


    #.... return grassname for TRICLA (triple classes - HQMQ&MAT)
    ##Ex.HQ_simulation_010000_p035_h036_HQ022_MQ013_LQ064
    file_trimat=open("_simulados04_3class.txt","r")
    trimat=file_trimat.readlines()
    file_trimat.close()
    
    for i in trimat:        
        if re.search(landscape_index, i):
            i=i.replace(".txt","")
            i=i.replace("= ","")
            i=i.replace(" ","_")
            i=i.replace("\n","")
            landscape_grassname_tricla=i

    #.... return grassname for HABDIST (Distance from EDGE of habitat)
    #.... and on this case, distance are in PIXELS, where positive
    #.... values represent distance on MATRIX direction, and
    #.... negative values are on CORE direction
    ##Ex.HQ_simulation_010000_p035_h036_dist_HABMAT
    file_dsthab=open("_simulados03_dist_HABMAT.txt","r")
    dsthab=file_dsthab.readlines()
    file_dsthab.close()
    
    for i in dsthab:
        if re.search(landscape_index, i):
            landscape_grassname_dsthab=i.replace(".txt\n","")
            landscape_grassname_dsthab+="_dist_HABMAT"
   
    return landscape_grassname_habmat, landscape_grassname_hiqmat, landscape_grassname_tricla, landscape_grassname_dsthab
    
if __name__ == "__main__":
    habmat=select_landscape_grassnames()
    print habmat
    