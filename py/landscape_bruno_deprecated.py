#!/c/Python25 python
#import sys, os, numpy #sys, os, PIL, numpy, Image, ImageEnhance
import grass.script as grass
from PIL import Image
import wx
import random
import re
import time
import math
#from rpy2 import robjects
from datetime import tzinfo, timedelta, datetime

ID_ABOUT=101
ID_IBMCFG=102
ID_EXIT=110


#---------------------------------------------------
import distance_between_indiv
#---------------------------------------------------
import gene_exchance
#---------------------------------------------------
###############CARE CARE CARE CARE
###############CARE CARE CARE CARE
###############CARE CARE CARE CARE
import gene_exchanceANTIGO
#---------------------------------------------------
import LOCI_start
#---------------------------------------------------
def estimate_movement_cost(actualcost,distfromedgePix, aux_xy):
    protecdness=get_safetyness_mortality(tab_in=Form1.tab_safetyness, distPix=distfromedgePix)
    
    aux=[aux_xy]
    aux, changed_quadrante=check_landscaperange(aux)
    YY=aux[0][0]
    XX=aux[0][1]        
    row=int(YY)
    col=int(XX)
    habqualyOnPosition=Form1.landscape_hqmqlq_quality[row][col]

    if protecdness<0.05:
        protecdness=0.05
    if protecdness>1:
        protecdness=1.0
    if habqualyOnPosition<0.05:
        habqualyOnPosition=0.05
    if habqualyOnPosition>1:
        habqualyOnPosition=1.0
    
    cost=actualcost+1.0/(protecdness*habqualyOnPosition)
    
    return cost

#---------------------------------------------------
def get_safetyness_mortality(tab_in, distPix=0):
    distMeters=float(distPix)*float(Form1.spatialresolution)
    if distMeters>0:
        distMeters=float(distPix+1)*float(Form1.spatialresolution)
    for line in range(len(tab_in)):
        line_dist=tab_in[line][0]
        if float(distMeters) < float(line_dist):
            if line==0:
                if Form1.species_profile=="Core dependent":
                    return tab_in[line][1]
                elif  Form1.species_profile=="Frag. dependent":
                    return tab_in[line][2]
                elif  Form1.species_profile=="Habitat dependent":
                    return tab_in[line][3]
                elif  Form1.species_profile=="Moderately generalist":
                    return tab_in[line][4]
                elif  Form1.species_profile=="Highly generalist":
                    return tab_in[line][5]
                else:
                    return 0
                    
            else:
                if Form1.species_profile=="Core dependent":
                    return tab_in[line-1][1]
                elif  Form1.species_profile=="Frag. dependent":
                    return tab_in[line-1][2]
                elif  Form1.species_profile=="Habitat dependent":
                    return tab_in[line-1][3]
                elif  Form1.species_profile=="Moderately generalist":
                    return tab_in[line-1][4]
                elif  Form1.species_profile=="Highly generalist":
                    return tab_in[line-1][5]
    return 0
#---------------------------------------------------
import read_table
#---------------------------------------------------
class TZ(tzinfo):
    import utcoffset
#---------------------------------------------------
class MyDate(object):
    import __init__
    import __repr__
#---------------------------------------------------
import kill_individual_new
#---------------------------------------------------
def organize_output(moment, grassname_habmat, isdispersing, isfemale, islive, totaldistance, effectivedistance, experiment_info, actualrun, actual_step, actual_movementcost, timestep_waslive,number_of_meetings,LOCI_start,LOCI_end):

    if actualrun<9:
        myzeros="000"
    elif actualrun<99:
        myzeros="00"
    elif actualrun<999:        
        myzeros="0"
    else:
        myzeros=""

#    for indiv in range(len(timestep_waslive)):
#        if timestep_waslive[indiv]==0:
#            timestep_waslive[indiv]=actual_step+1

    if moment=="ongoingstep":
        if Form1.output_store_ongoingsteps_indiv==1:
            output_filename_indiv=Form1.output_prefix+"_indiv_step"+".txt"
            file_output_indiv=open(output_filename_indiv,"a")
            if actual_step==0 and actualrun==0:
                file_output_indiv.write('experiment_info;actualrun;nruns;grassname_habmat;PLAND;CONFIG;HABQUAL;species_profile;include_quality;start_popsize;actual_step;timesteps;indiv;homerangesize;movdistpix;dispfactor;isdispersing;isfemale;islive;totaldistance;effectivedistance;actual_movementcost;timestep_waslivem;number_of_meetings;LOCI_start;LOCI_end\n')
            for indiv in range(len(totaldistance)):
                file_output_indiv.write('%s;' % experiment_info)
                file_output_indiv.write('%s;' % str(actualrun+1))
                file_output_indiv.write('%s;' % Form1.numberruns)
                file_output_indiv.write('%s;' % grassname_habmat)
                file_output_indiv.write('%s;' % Form1.landscape_grassname_habmat[19:22])
                file_output_indiv.write('%s;' % Form1.landscape_grassname_habmat[24:27])
                
                HABQUAL=0
                for row in range(len(Form1.landscape_hqmqlq_quality)):
                    for col in range(len(Form1.landscape_hqmqlq_quality[0])):
                        HABQUAL+=Form1.landscape_hqmqlq_quality[row][col]
                HABQUAL=float(HABQUAL)/100.0
                HABQUAL=HABQUAL/(len(Form1.landscape_matrix)*len(Form1.landscape_matrix))
                HABQUAL=round(HABQUAL*100,0)
               
                file_output_indiv.write('%s;' % str(HABQUAL))
                file_output_indiv.write('%s;' % Form1.species_profile)
                file_output_indiv.write('%s;' % Form1.include_habitatquality)
                file_output_indiv.write('%s;' % str(Form1.start_popsize))
                file_output_indiv.write('%s;' % str(actual_step+1))
                file_output_indiv.write('%s;' % str(Form1.timesteps))
                file_output_indiv.write('%s;' % str(indiv+1))
                file_output_indiv.write('%s;' % str(Form1.homerangesize))
                file_output_indiv.write('%s;' % str(Form1.movement_dist_sigma_pixel))
                file_output_indiv.write('%s;' % str(Form1.when_dispersing_distance_factor))
                file_output_indiv.write('%s;' % str(isdispersing[indiv]))
                file_output_indiv.write('%s;' % str(isfemale[indiv]))
                file_output_indiv.write('%s;' % str(islive[indiv]))                
                file_output_indiv.write('%s;' % str(totaldistance[indiv]))
                file_output_indiv.write('%s;' % str(effectivedistance[indiv]))
                file_output_indiv.write('%s;' % str(actual_movementcost[indiv]))
                file_output_indiv.write('%s;' % str(timestep_waslive[indiv]))
                file_output_indiv.write('%s;' % str(number_of_meetings[indiv]))
                file_output_indiv.write('%s;' % str(LOCI_start[indiv]))
                file_output_indiv.write('%s'  % str(LOCI_end[indiv]))
                file_output_indiv.write('\n')
            file_output_indiv.close()
    
        if Form1.output_store_ongoingsteps_landscape==1:
            output_filename_landscape=Form1.output_prefix+"_landscape_step"+".txt"
            file_output_landscape=open(output_filename_landscape,"a")
            if actual_step==0 and actualrun==0:
                file_output_landscape.write('experiment_info;actualrun;nruns;grassname_habmat;PLAND;CONFIG;HABQUAL;species_profile;include_quality;start_popsize;actual_step;timesteps;homerangesize;movdistpix;dispfactor;isdispersing;isfemale;islive;totaldistance;effectivedistance;actual_movementcost;timestep_waslive;number_of_meetings\n')
            file_output_landscape.write('%s;' % experiment_info)
            file_output_landscape.write('%s;' % str(actualrun+1))
            file_output_landscape.write('%s;' % Form1.numberruns)
            file_output_landscape.write('%s;' % Form1.landscape_grassname_habmat)
            file_output_landscape.write('%s;' % Form1.landscape_grassname_habmat[19:22])
            file_output_landscape.write('%s;' % Form1.landscape_grassname_habmat[24:27])
            
            HABQUAL=0
            for row in range(len(Form1.landscape_hqmqlq_quality)):
                for col in range(len(Form1.landscape_hqmqlq_quality[0])):
                    HABQUAL+=Form1.landscape_hqmqlq_quality[row][col]
            HABQUAL=float(HABQUAL)/100.0
            HABQUAL=HABQUAL/(len(Form1.landscape_matrix)*len(Form1.landscape_matrix))
            HABQUAL=round(HABQUAL*100,0)
           
            file_output_landscape.write('%s;' % str(HABQUAL))
            file_output_landscape.write('%s;' % Form1.species_profile)
            file_output_landscape.write('%s;' % Form1.include_habitatquality)
            file_output_landscape.write('%s;' % str(Form1.start_popsize))
            file_output_landscape.write('%s;' % str(actual_step+1))  
            file_output_landscape.write('%s;' % str(Form1.timesteps))
            file_output_landscape.write('%s;' % str(Form1.homerangesize))
            file_output_landscape.write('%s;' % str(Form1.movement_dist_sigma_pixel))
            file_output_landscape.write('%s;' % str(Form1.when_dispersing_distance_factor))
            file_output_landscape.write('%s;' % str(sum(isdispersing)))
            file_output_landscape.write('%s;' % str(sum(isfemale)))
            file_output_landscape.write('%s;' % str(sum(islive)))
            file_output_landscape.write('%s;' % str(  round(float(sum(totaldistance)),2)  ))
            file_output_landscape.write('%s;' % str(  round(float(sum(effectivedistance)),2)  ))
            file_output_landscape.write('%s;' % str(  max(actual_movementcost)  ))
            file_output_landscape.write('%s;' % str(sum(timestep_waslive)))
            file_output_landscape.write('%s'  % str(sum(number_of_meetings)))
            file_output_landscape.write('\n')
            file_output_landscape.close()

        
        
        
    if moment=="summary_of_a_run":
        if Form1.output_store_summary_indiv==1:
            output_filename_indiv=Form1.output_prefix+"_indiv.txt"
            file_output_indiv=open(output_filename_indiv,"a")
            for indiv in range(len(totaldistance)):
                if indiv==0:
                    file_output_indiv.write('experiment_info;actualrun;nruns;grassname_habmat;PLAND;CONFIG;HABQUAL;species_profile;include_quality;start_popsize;timesteps;indiv;homerangesize;movdistpix;dispfactor;isdispersing;isfemale;islive;totaldistance;effectivedistance;actual_movementcost;timestep_waslive;number_of_meetings;LOCI_start;LOCI_end\n')
                file_output_indiv.write('%s;' % experiment_info)
                file_output_indiv.write('%s;' % str(actualrun+1))
                file_output_indiv.write('%s;' % Form1.numberruns)
                file_output_indiv.write('%s;' % grassname_habmat)
                file_output_indiv.write('%s;' % Form1.landscape_grassname_habmat[19:22])
                file_output_indiv.write('%s;' % Form1.landscape_grassname_habmat[24:27])

                HABQUAL=0
                for row in range(len(Form1.landscape_hqmqlq_quality)):
                    for col in range(len(Form1.landscape_hqmqlq_quality[0])):
                        HABQUAL+=Form1.landscape_hqmqlq_quality[row][col]
                HABQUAL=float(HABQUAL)/100.0
                HABQUAL=HABQUAL/(len(Form1.landscape_matrix)*len(Form1.landscape_matrix))
                HABQUAL=round(HABQUAL*100,0)
            
                file_output_indiv.write('%s;' % str(HABQUAL))                
                file_output_indiv.write('%s;' % Form1.species_profile)
                file_output_indiv.write('%s;' % Form1.include_habitatquality)
                file_output_indiv.write('%s;' % str(Form1.start_popsize))
                file_output_indiv.write('%s;' % str(Form1.timesteps))
                file_output_indiv.write('%s;' % str(indiv+1))
                file_output_indiv.write('%s;' % str(Form1.homerangesize))
                file_output_indiv.write('%s;' % str(Form1.movement_dist_sigma_pixel))
                file_output_indiv.write('%s;' % str(Form1.when_dispersing_distance_factor))
                file_output_indiv.write('%s;' % str(isdispersing[indiv]))
                file_output_indiv.write('%s;' % str(isfemale[indiv]))
                file_output_indiv.write('%s;' % str(islive[indiv]))
                file_output_indiv.write('%s;' % str(totaldistance[indiv]))
                file_output_indiv.write('%s;' % str(effectivedistance[indiv]))
                file_output_indiv.write('%s;' % str(actual_movementcost[indiv]))
                file_output_indiv.write('%s;' % str(timestep_waslive[indiv]))
                file_output_indiv.write('%s;' % str(number_of_meetings[indiv]))
                file_output_indiv.write('%s;' % str(LOCI_start[indiv]))
                file_output_indiv.write('%s'  % str(LOCI_end[indiv]))
                file_output_indiv.write('\n')
            file_output_indiv.close()
    
        if Form1.output_store_summary_landscape==1:
            output_filename_landscape=Form1.output_prefix+"_landscape.txt"
            file_output_landscape=open(output_filename_landscape,"a")
            if actualrun==0:
                file_output_landscape.write('experiment_info;actualrun;nruns;grassname_habmat;PLAND;CONFIG;HABQUAL;species_profile;include_quality;start_popsize;timesteps;homerangesize;movdistpix;dispfactor;isdispersing;isfemale;islive;totaldistance;effectivedistance;actual_movementcost;timestep_waslive;number_of_meetings\n')
            file_output_landscape.write('%s;' % experiment_info)
            file_output_landscape.write('%s;' % str(actualrun+1))
            file_output_landscape.write('%s;' % Form1.numberruns)
            file_output_landscape.write('%s;' % Form1.landscape_grassname_habmat)
            file_output_landscape.write('%s;' % Form1.landscape_grassname_habmat[19:22])
            file_output_landscape.write('%s;' % Form1.landscape_grassname_habmat[24:27])
            
            HABQUAL=0
            for row in range(len(Form1.landscape_hqmqlq_quality)):
                for col in range(len(Form1.landscape_hqmqlq_quality[0])):
                    HABQUAL+=Form1.landscape_hqmqlq_quality[row][col]
            HABQUAL=float(HABQUAL)/100.0
            HABQUAL=HABQUAL/(len(Form1.landscape_matrix)*len(Form1.landscape_matrix))
            HABQUAL=round(HABQUAL*100,0)
            
            file_output_landscape.write('%s;' % str(HABQUAL))
            file_output_landscape.write('%s;' % Form1.species_profile)
            file_output_landscape.write('%s;' % Form1.include_habitatquality)
            file_output_landscape.write('%s;' % str(Form1.start_popsize))
            file_output_landscape.write('%s;' % str(Form1.timesteps))
            file_output_landscape.write('%s;' % str(Form1.homerangesize))
            file_output_landscape.write('%s;' % str(Form1.movement_dist_sigma_pixel))
            file_output_landscape.write('%s;' % str(Form1.when_dispersing_distance_factor))            
            file_output_landscape.write('%s;' % str(sum(isdispersing)))
            file_output_landscape.write('%s;' % str(sum(isfemale)))
            file_output_landscape.write('%s;' % str(sum(islive)))
            file_output_landscape.write('%s;' % str(  round(float(sum(totaldistance)),2)  ))
            file_output_landscape.write('%s;' % str(  round(float(sum(effectivedistance)),2)  ))
            file_output_landscape.write('%s;' % str(max(actual_movementcost)))
            file_output_landscape.write('%s;' % str(sum(timestep_waslive)))
            file_output_landscape.write('%s'  % str(sum(number_of_meetings)))
            file_output_landscape.write('\n')
            file_output_landscape.close()
    

#---------------------------------------------------
import estimate_effectivedistance
#---------------------------------------------------
import check_overpopulation_onpatch
#---------------------------------------------------
import reset_isdispersing
#---------------------------------------------------
import identify_habareapix
#---------------------------------------------------
import identify_patchid
#---------------------------------------------------
def estimate_start_popsize(landscape_grassname_habmat):
    tmp_pland=landscape_grassname_habmat[19:22]
    PixelAreaHA=Form1.spatialresolution*Form1.spatialresolution
    LandscapePixels=len(Form1.landscape_matrix)*len(Form1.landscape_matrix)
    tmp_starting_popsize=int(int(tmp_pland)*LandscapePixels*PixelAreaHA/100/10000/Form1.homerangesize)+1
    return tmp_starting_popsize 
#---------------------------------------------------
import estimate_distedgePix
#-------------------------------------------------ateaqui
#-------------------------------------------------ateaqui
#---------------------------------------------------
def pickup_one_landscape():
    '''This part select one random landscape when
       from the Spatial Data Base
    '''
    landscape_grassname_habmat, landscape_grassname_hqmqlq, landscape_grassname_habdist, landscape_grassname_habmat_pid, landscape_grassname_habmat_areapix, landscape_grassname_hqmqlq_quality, landscape_grassname_hqmqlq_AREAqual, landscape_grassname_frag_pid, landscape_grassname_frag_AREApix,landscape_grassname_frag_AREAqual,landscape_grassname_dila01clean_pid,landscape_grassname_dila01clean_AREApix,landscape_grassname_dila01clean_AREAqual,landscape_grassname_dila02clean_pid,landscape_grassname_dila02clean_AREApix,landscape_grassname_dila02clean_AREAqual=select_landscape_grassnames()
    
    export_raster_from_grass(landscape_grassname_habmat, landscape_grassname_hqmqlq, landscape_grassname_habdist,landscape_grassname_habmat_pid,landscape_grassname_habmat_areapix,landscape_grassname_hqmqlq_quality,landscape_grassname_hqmqlq_AREAqual,landscape_grassname_frag_pid,landscape_grassname_frag_AREApix,landscape_grassname_frag_AREAqual,landscape_grassname_dila01clean_pid,landscape_grassname_dila01clean_AREApix,landscape_grassname_dila01clean_AREAqual,landscape_grassname_dila02clean_pid,landscape_grassname_dila02clean_AREApix,landscape_grassname_dila02clean_AREAqual)
    
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
    
#---------------------------------------------------
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
    landscape_grassname_frag_AREAqual=landscape_grassname_frag_AREApix.replace("AREApix","AREAqual")

    
    
    ### STILLLL CHECK... Need I load COMPLETE maps?!
    ### STILLLL CHECK... Need I load COMPLETE maps?!
    ### STILLLL CHECK... Need I load COMPLETE maps?!
    ### STILLLL CHECK... Need I load COMPLETE maps?!
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
        if re.search(landscape_index, i):
            landscape_grassname_dila01clean_AREApix=i.replace("\n","")

    ##simulation_000001_p029_h059_HABMAT_DILA01_AREAqual
         ### USING THE SAME INPUT FILE AS AREApix!!!!
    landscape_grassname_dila01clean_AREAqual=landscape_grassname_dila01clean_AREApix.replace("AREApix","AREAqual")
    

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
        if re.search(landscape_index, i):
            landscape_grassname_dila02clean_AREApix=i.replace("\n","")

    ##simulation_000001_p029_h059_HABMAT_DILA02_AREAqual
         ### USING THE SAME INPUT FILE AS AREApix!!!!
    landscape_grassname_dila02clean_AREAqual=landscape_grassname_dila02clean_AREApix.replace("AREApix","AREAqual")
    
    return landscape_grassname_habmat, landscape_grassname_hqmqlq, landscape_grassname_habdist, landscape_grassname_habmat_pid, landscape_grassname_habmat_areapix, landscape_grassname_hqmqlq_quality, landscape_grassname_hqmqlq_AREAqual, landscape_grassname_frag_pid, landscape_grassname_frag_AREApix, landscape_grassname_frag_AREAqual, landscape_grassname_dila01clean_pid, landscape_grassname_dila01clean_AREApix, landscape_grassname_dila01clean_AREAqual, landscape_grassname_dila02clean_pid, landscape_grassname_dila02clean_AREApix, landscape_grassname_dila02clean_AREAqual

#----------------------------------------------------------------------
def export_raster_from_grass(landscape_grassname_habmat, landscape_grassname_hqmqlq, landscape_grassname_habdist, landscape_grassname_habmat_pid, landscape_grassname_habmat_areapix, landscape_grassname_hqmqlq_quality, landscape_grassname_hqmqlq_AREAqual, landscape_grassname_frag_pid, landscape_grassname_frag_AREApix,landscape_grassname_frag_AREAqual, landscape_grassname_dila01clean_pid, landscape_grassname_dila01clean_AREApix,landscape_grassname_dila01clean_AREAqual, landscape_grassname_dila02clean_pid, landscape_grassname_dila02clean_AREApix,landscape_grassname_dila02clean_AREAqual):
    '''This function read a set of filenames and export it from grass Mapsets 
    For this simulations, filename will be a list of _habmat, 
    _dist, _funcArea (several), _effectiveFuncArea
    '''

    ''' 
    An update was done in jan 2014 to fit with the new versions of GRASS 6.4.3
    
    '''
    
    #mycommands=[]

    grass.run_command("r.colors", map=landscape_grassname_habmat+'@MS_HABMAT', rules='_habmat_color.txt')
    grass.run_command('r.out.ascii', input=landscape_grassname_habmat+'@MS_HABMAT', output='random_landscape_habmat.asc')
    grass.run_command('r.out.png', input=landscape_grassname_habmat+'@MS_HABMAT', output='random_landscape_habmat.png')
    
    grass.run_command('r.colors.stddev', input=landscape_grassname_habdist+'@MS_HABMAT_DIST')
    grass.run_command('r.out.ascii', input=landscape_grassname_habdist+'@MS_HABMAT_DIST', output='random_landscape_habdist.asc')
    grass.run_command('r.out.png', input=landscape_grassname_habdist+'@MS_HABMAT_DIST', output='random_landscape_habdist.png')
    
    grass.run_command('r.out.ascii',input=landscape_grassname_hqmqlq+'@MS_HQMQLQ', output='random_landscape_hqmqlq.asc')
    grass.run_command('r.out.png', input=landscape_grassname_hqmqlq+'@MS_HQMQLQ', output='random_landscape_hqmqlq.png')
    
    ##---------------------------------
    grass.run_command('r.out.ascii', input=landscape_grassname_habmat_pid+'@MS_HABMAT_PID',  output='random_landscape_habmat_pid.asc', null=0)
    grass.run_command('r.out.png', input=landscape_grassname_habmat_pid+'@MS_HABMAT_PID', output='random_landscape_habmat_pid.png')

    grass.run_command('r.out.ascii', input=landscape_grassname_habmat_areapix+'@MS_HABMAT_AREA', output='random_landscape_habmat_areapix.asc', null=0)
    grass.run_command('r.out.png', input=landscape_grassname_habmat_areapix+'@MS_HABMAT_AREA', output='random_landscape_habmat_areapix.png')

    grass.run_command('r.out.ascii', input=landscape_grassname_hqmqlq_quality+'@MS_HQMQLQ_AREAqual', output='random_landscape_hqmqlq_quality.asc', null=0)
    grass.run_command('r.out.png', input=landscape_grassname_hqmqlq_quality+'@MS_HQMQLQ_AREAqual', output='random_landscape_hqmqlq_quality.png')
    
    grass.run_command('r.out.ascii', input=landscape_grassname_hqmqlq_AREAqual+'@MS_HQMQLQ_AREAqual', output='random_landscape_hqmqlq_AREAqual.asc', null=0)
    grass.run_command('r.out.png', input=landscape_grassname_hqmqlq_AREAqual+'@MS_HQMQLQ_AREAqual', output='random_landscape_hqmqlq_AREAqual.png')

    ##---------------------------------
    grass.run_command('r.out.ascii', input=landscape_grassname_frag_pid+'@MS_HABMAT_FRAG_PID', output='random_landscape_frag_pid.asc', null=0)
    grass.run_command('r.out.png', input=landscape_grassname_frag_pid+'@MS_HABMAT_FRAG_PID', output='random_landscape_frag_pid.png')

    grass.run_command('r.out.ascii', input=landscape_grassname_frag_AREApix+'@MS_HABMAT_FRAG_AREA' , output='random_landscape_frag_AREApix.asc', null=0)
    grass.run_command('r.out.png', input=landscape_grassname_frag_AREApix+'@MS_HABMAT_FRAG_AREA', output='random_landscape_frag_AREApix.png')

    grass.run_command('r.out.ascii', input=landscape_grassname_frag_AREAqual+'@MS_HABMAT_FRAG_AREAqual', output='random_landscape_frag_AREAqual.asc', null=0)
    grass.run_command('r.out.png', input=landscape_grassname_frag_AREAqual+'@MS_HABMAT_FRAG_AREAqual', output='random_landscape_frag_AREAqual.png')    

    #----------- DILA01
    ##---------------------------------
    grass.run_command('r.out.ascii', input=landscape_grassname_dila01clean_pid+'@MS_HABMAT_DILA01_PID',output='random_landscape_dila01clean_pid.asc', null=0)
    grass.run_command('r.out.png', input=landscape_grassname_dila01clean_pid+'@MS_HABMAT_DILA01_PID', output='random_landscape_dila01clean_pid.png')

    grass.run_command('r.out.ascii', input=landscape_grassname_dila01clean_AREApix+'@MS_HABMAT_DILA01_AREA', output='random_landscape_dila01clean_AREApix.asc', null=0)
    grass.run_command('r.out.png', input=landscape_grassname_dila01clean_AREApix+'@MS_HABMAT_DILA01_AREA', output='random_landscape_dila01clean_AREApix.png')

    grass.run_command('r.out.ascii', input=landscape_grassname_dila01clean_AREAqual.replace("HABMAT_grassclump_dila01_clean_AREAqual","HABMAT_DILA01_AREAqual")
+'@MS_HABMAT_DILA01_AREAqual', output='random_landscape_dila01clean_AREAqual.asc', null=0)
    grass.run_command('r.out.png', input=landscape_grassname_dila01clean_AREAqual.replace("HABMAT_grassclump_dila01_clean_AREAqual","HABMAT_DILA01_AREAqual")
+'@MS_HABMAT_DILA01_AREAqual', output='random_landscape_dila01clean_AREAqual.png')

    #----------- DILA02
    ##---------------------------------
    grass.run_command('r.out.ascii', input=landscape_grassname_dila02clean_pid+'@MS_HABMAT_DILA02_PID', output='random_landscape_dila02clean_pid.asc', null=0)
    grass.run_command('r.out.png', input=landscape_grassname_dila02clean_pid+'@MS_HABMAT_DILA02_PID', output='random_landscape_dila02clean_pid.png')

    grass.run_command('r.out.ascii', input=landscape_grassname_dila02clean_AREApix.replace("HQ_","")+'@MS_HABMAT_DILA02_AREA', output='random_landscape_dila02clean_AREApix.asc', null=0)
    grass.run_command('r.out.png', input=landscape_grassname_dila02clean_AREApix.replace("HQ_","")+'@MS_HABMAT_DILA02_AREA', output='random_landscape_dila02clean_AREApix.png')

    grass.run_command('r.out.ascii', input=landscape_grassname_dila02clean_AREAqual.replace("HABMAT_grassclump_dila02_clean_AREAqual","HABMAT_DILA02_AREAqual").replace("HQ_","")
+'@MS_HABMAT_DILA02_AREAqual', output='random_landscape_dila02clean_AREAqual.asc', null=0)
    grass.run_command('r.out.png', input=landscape_grassname_dila02clean_AREAqual.replace("HABMAT_grassclump_dila02_clean_AREAqual","HABMAT_DILA02_AREAqual").replace("HQ_","")
+'@MS_HABMAT_DILA02_AREAqual', output='random_landscape_dila02clean_AREAqual.png')
    
    
    #for i in mycommands:
     #   grass.run_command(i)


#----------------------------------------------------------------------
def color_pallete():
    pal = [(0,0,0) for i in range(256)]  # all black
    
    random.seed(1)
    for i in range(1,255):
        color_R=random.sample(range(1,255),1)
        color_G=random.sample(range(1,255),1)
        color_B=random.sample(range(1,255),1)
        #pal[i]=((255-i),int(i/2),i)
        pal[i]=(color_R[0],color_G[0],color_B[0])
    
    pal=random.sample(pal, 255)

#    if Form1.background_filename[0]=="random_landscape_habmat.png":
#        pal[1] = (68,194,0)     # HABITAT
#        pal[2] = (255,190,190)  # MATRIZ
#    if Form1.background_filename[0]=="random_landscape_hqmqlq.png":
    if 1==1:
        pal[1] = (68,194,0)     # HABITAT
        pal[2] = (255,235,190)  # MQ/MATRIZ
        pal[3] = (255,190,190)  # MATRIZ

    pal = sum(pal, ())  # flatten it
    random.seed()
    return pal
        
#----------------------------------------------------------------------
def color_palleteantiga():
    pal = [(0,0,0) for i in range(256)]  # all black
    
    random.seed(1)
    for i in range(1,255):
        pal[i]=((255-i),int(i/2),i)
    
    pal=random.sample(pal, 255)

#    if Form1.background_filename[0]=="random_landscape_habmat.png":
#        pal[1] = (68,194,0)     # HABITAT
#        pal[2] = (255,190,190)  # MATRIZ
#    if Form1.background_filename[0]=="random_landscape_hqmqlq.png":
    if 1==1:
        pal[1] = (68,194,0)     # HABITAT
        pal[2] = (255,235,190)  # MQ/MATRIZ
        pal[3] = (255,190,190)  # MATRIZ

    pal = sum(pal, ())  # flatten it
    random.seed()
    return pal

#----------------------------------------------------------------------
def disperse_random_walk(landscape_matrix, indiv_xy, movement_dist_sigma_pixel, indiv_totaldistance):
    '''on landscape_matrix 1=HQ / 2=MQ / 3=LQ'''
    modified_indiv_xy=[]
    for i in range(len(indiv_xy)):
        modified_indiv_xy.append(indiv_xy[i])
   
    for xp in range(len(modified_indiv_xy)):
        modified_indiv_xy[xp][0]+=random.normalvariate(mu=0,sigma=movement_dist_sigma_pixel)   # random xpos
        modified_indiv_xy[xp][1]+=random.normalvariate(mu=0,sigma=movement_dist_sigma_pixel)   # random ypos

    modified_indiv_xy,changed_quadrant=check_landscaperange(modified_indiv_xy)
    
    return modified_indiv_xy, indiv_totaldistance,changed_quadrant


#----------------------------------------------------------------------
def get_listofposition(modified_indiv_xy_startpos):
    n_positions=20
    listofpositions=[]
    for pos in range(n_positions):
        deltaX=random.uniform(-Form1.movement_dist_sigma_pixel,Form1.movement_dist_sigma_pixel)
        deltaY=random.uniform(-Form1.movement_dist_sigma_pixel,Form1.movement_dist_sigma_pixel)
        listofpositions.append([modified_indiv_xy_startpos[0]+deltaX,modified_indiv_xy_startpos[1]+deltaY])

    listofpositions,changed_quadrante_psicologic=check_landscaperange(listofpositions)
    return listofpositions

#----------------------------------------------------------------------
def check_landscaperange(list_of_xy):
    list_of_xy_modified=[]
    for i in range(len(list_of_xy)):
        list_of_xy_modified.append(list_of_xy[i])
    
    changed_quadrant=[]
    for indiv in range(len(list_of_xy)):
        #let row be ok
        ns=0
        ew=0
        
        if list_of_xy_modified[indiv][0]<0:
            list_of_xy_modified[indiv][0]=list_of_xy_modified[indiv][0]+len(Form1.landscape_matrix)
            ns=+1 #gone to North
        if list_of_xy_modified[indiv][0]>len(Form1.landscape_matrix):
            list_of_xy_modified[indiv][0]=list_of_xy_modified[indiv][0]-len(Form1.landscape_matrix)
            ns=-1 #gone to South
        #let col be ok    
        if list_of_xy_modified[indiv][1]<0:
            list_of_xy_modified[indiv][1]=list_of_xy_modified[indiv][1]+len(Form1.landscape_matrix)
            ew=-1 #gone to West
        if list_of_xy_modified[indiv][1]>len(Form1.landscape_matrix):
            list_of_xy_modified[indiv][1]=list_of_xy_modified[indiv][1]-len(Form1.landscape_matrix)
            ew=+1 #gone to Eest
        changed_quadrant.append([ns,ew])
    return list_of_xy_modified, changed_quadrant


#----------------------------------------------------------------------
def OnHabitat(listposition):
    aux=[]
    distfromedgePix=[]
    for i in range(len(listposition)):
        aux.append([listposition[i][0],listposition[i][1]])
        
    OnHabitatList=[] #X, Y
    OnHabitatEdgedistPixList=[] #DIST from edge
    
    for position in range(len(aux)):
        aux, changed_quadrante=check_landscaperange(aux)
        YY=aux[position][0]
        XX=aux[position][1]        
        row=int(YY)
        col=int(XX)
        distfromedgePix.append(Form1.landscape_habdist[row][col])


        ##'Random walk','Core dependent','Frag. dependent', 'Habitat dependent', 'Moderately generalist'
        
        if distfromedgePix[position]*Form1.spatialresolution<=0 and Form1.species_profile=="Habitat dependent":
            # <=0 above means the the full patch is considered.. 
            # corridor (<60m) IS INCLUDED as "habitat patch"
            OnHabitatList.append([YY,XX])
            OnHabitatEdgedistPixList.append(Form1.landscape_habdist[row][col])
            
        if distfromedgePix[position]*Form1.spatialresolution<(-30) and Form1.species_profile=="Frag. dependent":
        
            # < (-30) means 30 meters from edge
            # so only the fragment is considered.. corridor (<60m)
            # is NOT INCLUDED as "habitat patch"
            OnHabitatList.append([YY,XX])
            OnHabitatEdgedistPixList.append(Form1.landscape_habdist[row][col])

        if distfromedgePix[position]*Form1.spatialresolution<(-30) and Form1.species_profile=="Core dependent":
            ### I COPYED THIS PART FROM ABOVE ON FEV2010 - CHECK CHECK CHECK m
            #####  check -30 !!!!
            # < (-30) means 30 meters from edge
            # so only the fragment is considered.. corridor (<60m)
            # is NOT INCLUDED as "habitat patch"
            OnHabitatList.append([YY,XX])
            OnHabitatEdgedistPixList.append(Form1.landscape_habdist[row][col])
            
        if distfromedgePix[position]*Form1.spatialresolution<=(+30) and Form1.species_profile=="Moderately generalist":
            # <=+30 above means the the full patch is considered.. 
            # corridor (<60m) IS INCLUDED as "habitat patch"
            # Positions <30 of ANY HABITAT PATCH is considered within habitat patch"
            
            OnHabitatList.append([YY,XX])
            OnHabitatEdgedistPixList.append(Form1.landscape_habdist[row][col])
            
        if distfromedgePix[position]*Form1.spatialresolution<=(+60) and Form1.species_profile=="Highly generalist":
            # <=+60 above means the the full patch is considered.. 
            # corridor (<60m) IS INCLUDED as "habitat patch"
            # Positions <60 of ANY HABITAT PATCH is considered within habitat patch"
            
            OnHabitatList.append([YY,XX])
            OnHabitatEdgedistPixList.append(Form1.landscape_habdist[row][col])

    return OnHabitatList, OnHabitatEdgedistPixList

#----------------------------------------------------------------------
#----------------------------------------------------------------------
def disperse_habitat_dependent(indiv_xy, indiv_isdispersing,indiv_totaldistance,indiv_dispdirectionX,indiv_dispdirectionY):
    modified_indiv_xy=[]
    for i in range(len(indiv_xy)):
        modified_indiv_xy.append([indiv_xy[i][0],indiv_xy[i][1]])
   
    for indiv in range(len(modified_indiv_xy)):
        x1=modified_indiv_xy[indiv][0]
        y1=modified_indiv_xy[indiv][1]
        if indiv_isdispersing[indiv]==0:
            modified_indiv_xy_listposition=get_listofposition(modified_indiv_xy_startpos=modified_indiv_xy[indiv])
            modified_indiv_xy_listposition, distfromedgePix=OnHabitat(modified_indiv_xy_listposition)
            
            if len(modified_indiv_xy_listposition)>0:
                PROB_go_core_region=0

                if Form1.species_profile=="Highly generalist":
                    PROB_go_core_region=0.05                
                if Form1.species_profile=="Moderately generalist":
                    PROB_go_core_region=0.05
                if Form1.species_profile=="Habitat dependent":
                    PROB_go_core_region=0.1
                if Form1.species_profile=="Frag. dependent":
                    PROB_go_core_region=0.3 
                if Form1.species_profile=="Core dependent":
                    PROB_go_core_region=0.7
                    
                if distfromedgePix[0]*Form1.spatialresolution< (-90):
                    #when position in relation to edge is > (-) 80 m 
                    #then the individual can move freely
                    #Based on Hansbauer et al 2008 - for C.caudata species
                    PROB_go_core_region=0.05
                    
                if random.uniform(0,1)<PROB_go_core_region: #FORCE go to core of habitats
                    max_distfromedgePix=min(distfromedgePix)
                    #### MAX DIST FROM EDGE is equal to min(distfromedgePix)
                    
                    for OnHabitatPosition in range(len(modified_indiv_xy_listposition)):
                        if distfromedgePix[OnHabitatPosition]==max_distfromedgePix:
                            modified_indiv_xy[indiv][0]=modified_indiv_xy_listposition[OnHabitatPosition][0]
                            modified_indiv_xy[indiv][1]=modified_indiv_xy_listposition[OnHabitatPosition][1]
                else: #pickup a random distance THAT is OnHabitatList
                    modified_indiv_xy[indiv][0]=modified_indiv_xy_listposition[0][0]
                    modified_indiv_xy[indiv][1]=modified_indiv_xy_listposition[0][1]
        if indiv_isdispersing[indiv]==1:
            disdir_aux_XMIN=indiv_dispdirectionX[indiv][0]
            disdir_aux_XMAX=indiv_dispdirectionX[indiv][1]
            disdir_aux_YMIN=indiv_dispdirectionY[indiv][0]
            disdir_aux_YMAX=indiv_dispdirectionY[indiv][1]
            if random.uniform(0,1)<0.2:  #50% of a movements of the dispersing individual will follow a main direction
                modified_indiv_xy[indiv][0]+=random.uniform(disdir_aux_XMIN,disdir_aux_XMAX)*Form1.movement_dist_sigma_pixel*Form1.when_dispersing_distance_factor   # random xpos BUT with preferencial direction
                modified_indiv_xy[indiv][1]+=random.uniform(disdir_aux_YMIN,disdir_aux_YMAX)*Form1.movement_dist_sigma_pixel*Form1.when_dispersing_distance_factor   # random xpos BUT with preferencial direction
            else:
                modified_indiv_xy[indiv][0]+=random.normalvariate(mu=0,sigma=Form1.movement_dist_sigma_pixel)*Form1.when_dispersing_distance_factor   # random xpos
                modified_indiv_xy[indiv][1]+=random.normalvariate(mu=0,sigma=Form1.movement_dist_sigma_pixel)*Form1.when_dispersing_distance_factor   # random ypos
            
        
        x2y2=[[modified_indiv_xy[indiv][0],modified_indiv_xy[indiv][1]]]
        x2y2,changed_quadrant_psico=check_landscaperange(x2y2)
        x2=x2y2[0][0]
        y2=x2y2[0][1]
        if changed_quadrant_psico[0][0]==1:
            x2=x2-511
        if changed_quadrant_psico[0][0]==-1:
            x2=x2+511
        if changed_quadrant_psico[0][1]==1:
            y2=y2-511
        if changed_quadrant_psico[0][1]==-1:
            y2=y2+511            
        #y2=modified_indiv_xy[indiv][1]
        dist=math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
        if abs(dist)>500 or dist<0: #CHECK - I need to check when the distance is computed wrongly
            #print "error on Total Distance estimation\n"
            dist=0
        indiv_totaldistance[indiv]+=dist
        
    modified_indiv_xy, changed_quadrant=check_landscaperange(modified_indiv_xy)
    return modified_indiv_xy, indiv_totaldistance, changed_quadrant

#---------------------------------------
def plot_walk(landscape_matrix, indiv_xy, aux_isdispersing, aux_islive, nruns, aux_isdispersingRESET, timestep):
    '''....'''

    #random.seed(123) #to force every individual have the same color
                     #on each movement
                     
    landscape_matrix_temp=[]
    for row in range(len(landscape_matrix)):
        landscape_matrix_temp.append(landscape_matrix[row])

    for num_of_indiv in range(len(indiv_xy)):
        if aux_islive[num_of_indiv]==0:
            numbpix=Form1.indivpixels_isNOTlive
        elif aux_isdispersing[num_of_indiv]==1:
            numbpix=Form1.indivpixels_isdispersing
        else:
            numbpix=Form1.indivpixels_whenmoving
            
        for pixelsX in range(-(int(numbpix/2)),(int(numbpix/2)+1)):
            for pixelsY in range(-(int(numbpix/2)),(int(numbpix/2)+1)):
                xp=int(indiv_xy[num_of_indiv][0]+pixelsX)
                yp=int(indiv_xy[num_of_indiv][1]+pixelsY)
                if xp>(len(landscape_matrix)-1):
                    xp=(len(landscape_matrix)-1)
                if xp<0:
                    xp=0
                if yp>(len(landscape_matrix)-1):
                    yp=(len(landscape_matrix)-1)
                if yp<0:
                    yp=0
                num_of_indiv_color=num_of_indiv
                while num_of_indiv_color>255:
                    num_of_indiv_color=num_of_indiv_color-230
                    
                landscape_matrix_temp[xp][yp]=10+num_of_indiv_color
                                             #this 10 is just to shift starting color
                #landscape_matrix_temp[xp][yp]=random.sample(range(10,255),1 )
    
    im = Image.new('P', (len(landscape_matrix),len(landscape_matrix)))  # 'P' for palettized
    data = sum(landscape_matrix_temp, [])  # flatten data
    im.putdata(data)

    pal = color_pallete()

    im.putpalette(pal)

    im.save(Form1.background_filename[0])
    
    if nruns<9:
        myzeros="000"
    elif nruns<99:
        myzeros="00"
    elif nruns<999:        
        myzeros="0"
    else:
        myzeros=""
        
    saverun=Form1.output_prefix+"_run_"+myzeros+str(nruns+1)+".png"
    im.save(saverun)

    if timestep<9:
        myzerosTS="000"
    elif timestep<99:
        myzerosTS="00"
    elif timestep<999:        
        myzerosTS="0"
    else:
        myzerosTS=""
    saverunTS="moves/"+Form1.output_prefix+"_run_"+myzeros+str(nruns+1)+"_TS_"+myzerosTS+str(timestep+1)+".png"
    im2=im.copy()
    im2.save(saverunTS)
    
    
    
    random.seed()  #to release the random.seed()

#----------------------------------------------------------------------
def getForest(landscape_matrix):
    forest = []
    for row in range(len(landscape_matrix)):
        for col in range(len(landscape_matrix[0])):
            feature = landscape_matrix[row][col]
            if feature == 1: #HQ
                forest.append([row,col])
            if feature == 2: #MQ
                forest.append([row,col])                
    return forest

#----------------------------------------------------------------------
def populate(forest, nPop):
    return random.sample(forest, nPop)

#----------------------------------------------------------------------
def choose_dispersaldirection():
    direction_MIN=random.uniform(-1,0.75)
    direction_MAX=direction_MIN+0.5
    return [direction_MIN,direction_MAX]

#----------------------------------------------------------------------
class Form1(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        
        Form1.include_habitatquality="HabitatQuality_NO"
        Form1.plotmovements=0
        Form1.include_probdeath=0
        
        Form1.tab_safetyness=read_table.read_table("_models_safetyness.txt")
        Form1.tab_mortality =read_table.read_table("_models_mortality.txt")
        
        Form1.output_store_ongoingsteps_indiv=0
        Form1.output_store_ongoingsteps_landscape=0
        Form1.output_store_summary_indiv=1
        Form1.output_store_summary_landscape=1
        
        self.speciesList = ['Random walk','Core dependent','Frag. dependent', 'Habitat dependent', 'Moderately generalist', 'Highly generalist']

        Form1.species_profile=self.speciesList[3]
        
        Form1.start_popsize=5
        Form1.numberruns=100
        Form1.timesteps=200
        Form1.background_filename=["random_landscape_hqmqlq.png","random_landscape_habmat.png","random_landscape_habdist.png","random_landscape_habmat_pid.png","random_landscape_habmat_areapix.png","random_landscape_hqmqlq_quality.png","random_landscape_hqmqlq_AREAqual.png","random_landscape_frag_pid.png","random_landscape_frag_AREApix.png","random_landscape_frag_AREAqual.png"]
        Form1.background_filename_start=Form1.background_filename

        #LOCI Informations -----------------------------
        Form1.LOCI_structure=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0],[0,0],[0,0,0,0,0,0]]
        #####..........LOCI_structure=list of locus with its alleles 
        Form1.proximity_between_indiv_meters_threshold=100
        Form1.LOCI_gene_exchange_rate=0.1

        #HOME RANGE Informations -----------------------------
        Form1.homerangesize=10
        Form1.changehomerangesize=0 #0=not change; 1=uniform distr; 2=normaldist
        ####--- if changehomerangesize=1
        ####............ P1=min; P2=max
        ####--- if changehomerangesize=2
        ####............ P1=mean; P2=sd
        Form1.changehomerangesize_P1=20
        Form1.changehomerangesize_P2=10
        #(END) HOME RANGE Informations -----------------------------
        
        Form1.indivpixels_whenmoving=1
        Form1.indivpixels_isdispersing=1
        Form1.indivpixels_isNOTlive=1
       
        Form1.movement_dist_sigma_pixel=2.0
        Form1.when_dispersing_distance_factor=3.0
        
        Form1.indiv_agemean = 100
        Form1.indiv_agestd  = 20
        Form1.indiv_female_rate = 0.5
        
        Form1.spatialresolution=30 #resolution in meters
        Form1.output_prefix="_explandgen01_mca_t02"
        
        
        self.quote = wx.StaticText(self, id=-1, label="BioDIM v1.1 - landscape genetic embedded",pos=wx.Point(20, 30))
        
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.quote.SetForegroundColour("blue")
        self.quote.SetFont(font)

        Form1.landscape_head, Form1.landscape_matrix, Form1.landscape_grassname_habmat, Form1.landscape_habdist,Form1.landscape_habmat_pid,Form1.landscape_habmat_areapix,Form1.landscape_hqmqlq_quality,Form1.landscape_hqmqlq_AREAqual,Form1.landscape_frag_pid,Form1.landscape_frag_AREApix,Form1.landscape_frag_AREAqual,Form1.landscape_dila01clean_pid,Form1.landscape_dila01clean_AREApix,Form1.landscape_dila01clean_AREAqual,Form1.landscape_dila02clean_pid,Form1.landscape_dila02clean_AREApix,Form1.landscape_dila02clean_AREAqual=pickup_one_landscape()
        
                
        Form1.start_popsize=estimate_start_popsize(Form1.landscape_grassname_habmat)
        
        # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
        self.logger = wx.TextCtrl(self,5, "",wx.Point(20,380), wx.Size(320,100),wx.TE_MULTILINE | wx.TE_READONLY)
        # A button
        self.button =wx.Button(self, 10, "START SIMULATION", wx.Point(10, 500))
        wx.EVT_BUTTON(self, 10, self.OnClick)
        
        self.button =wx.Button(self, 9, "change Background", wx.Point(140, 500))
        wx.EVT_BUTTON(self, 9, self.OnClick)

        self.button =wx.Button(self, 11, "change Landscape", wx.Point(140, 530))
        wx.EVT_BUTTON(self, 11, self.OnClick)

        self.button =wx.Button(self, 8, "EXIT", wx.Point(260, 500))
        wx.EVT_BUTTON(self, 8, self.OnExit)

        ##------------ plot landscape image on wx.Panel
        im = Image.new('P', (len(Form1.landscape_matrix),len(Form1.landscape_matrix)))  # 'P' for palettized
        data = sum(Form1.landscape_matrix, [])  # flatten data
        im.putdata(data)
        pal = color_pallete()
        im.putpalette(pal)
        im.save(Form1.background_filename[0])
            
        imageFile=Form1.background_filename[0]
        im1 = Image.open(imageFile)
        jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(self, -1, jpg1, (350,30), (jpg1.GetWidth(), jpg1.GetHeight()), style=wx.SIMPLE_BORDER)
        
        ##------------ LElab_logo
        imageFile = 'LeLab05.gif'
        im1 = Image.open(imageFile)
        jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(self, -1, jpg1, (180,205), (jpg1.GetWidth(), jpg1.GetHeight()), style=wx.SUNKEN_BORDER)
        
        
        # the edit control - one line version.
        self.lblname = wx.StaticText(self, -1, "Output file name :",wx.Point(20,60))
        self.editname = wx.TextCtrl(self, 20, Form1.output_prefix, wx.Point(150, 60), wx.Size(140,-1))
        wx.EVT_TEXT(self, 20, self.EvtText)
        wx.EVT_CHAR(self.editname, self.EvtChar)
        

        Form1.lblstart_popsize = wx.StaticText(self, -1, "Pop Size :",wx.Point(20,120))
        Form1.edtstart_popsize = wx.TextCtrl(self, 30, str(Form1.start_popsize), wx.Point(82, 120), wx.Size(35,-1))
        wx.EVT_TEXT(self, 30, self.EvtText)
        wx.EVT_CHAR(Form1.edtstart_popsize, self.EvtChar)
        
        
        Form1.lblmovement_dist_sigma_pixel = wx.StaticText(self, -1, "Mov.Dist.Pix:",wx.Point(125,120))
        Form1.edtmovement_dist_sigma_pixel = wx.TextCtrl(self, 80, str(Form1.movement_dist_sigma_pixel), wx.Point(195, 120), wx.Size(30,-1))
        wx.EVT_TEXT(self, 80, self.EvtText)
        wx.EVT_CHAR(Form1.edtmovement_dist_sigma_pixel, self.EvtChar)
        
        Form1.lblwhen_dispersing_distance_factor = wx.StaticText(self, -1, "Dispers.Fact:",wx.Point(125,150))
        Form1.edtwhen_dispersing_distance_factor = wx.TextCtrl(self, 81, str(Form1.when_dispersing_distance_factor), wx.Point(195, 150), wx.Size(30,-1))
        wx.EVT_TEXT(self, 81, self.EvtText)
        wx.EVT_CHAR(Form1.edtwhen_dispersing_distance_factor, self.EvtChar)
        
        Form1.lblnumberruns = wx.StaticText(self, -1, "N. of Runs :",wx.Point(235,120))
        Form1.edtnumberruns = wx.TextCtrl(self, 50, str(Form1.numberruns), wx.Point(305, 120), wx.Size(35,-1))
        wx.EVT_TEXT(self, 50, self.EvtText)
        wx.EVT_CHAR(Form1.edtnumberruns, self.EvtChar)
        
        Form1.lbltimesteps = wx.StaticText(self, -1, "Time Steps :",wx.Point(20,150))
        Form1.edttimesteps = wx.TextCtrl(self, 40, str(Form1.timesteps), wx.Point(82, 150), wx.Size(35,-1))
        wx.EVT_TEXT(self, 40, self.EvtText)
        wx.EVT_CHAR(Form1.edttimesteps, self.EvtChar)

        Form1.lblhomerangesize = wx.StaticText(self, -1, "HRange(ha) :",wx.Point(235,150))
        Form1.edthomerangesize = wx.TextCtrl(self, 60, str(Form1.homerangesize), wx.Point(305, 150), wx.Size(35,-1))
        wx.EVT_TEXT(self, 60, self.EvtText)
        wx.EVT_CHAR(Form1.edthomerangesize, self.EvtChar)

        Form1.lblindivpixels = wx.StaticText(self, -1, "Indiv.Size (pix):",wx.Point(225,90))
        Form1.edtindivpixels = wx.TextCtrl(self, 70, str(Form1.indivpixels_whenmoving), wx.Point(305, 90), wx.Size(35,-1))
        wx.EVT_TEXT(self, 70, self.EvtText)
        wx.EVT_CHAR(Form1.edtindivpixels, self.EvtChar)
        
        
        # the combobox Control

        self.lblspeciesList = wx.StaticText(self,-1,"Species Profile:",wx.Point(20, 90))
        self.editspeciesList=wx.ComboBox(self, 93, Form1.species_profile, wx.Point(100, 90), wx.Size(120, -1),
        self.speciesList, wx.CB_DROPDOWN)
        wx.EVT_COMBOBOX(self, 93, self.EvtComboBox)
        wx.EVT_TEXT(self, 93, self.EvtText)
        
        # Checkbox
        self.insure = wx.CheckBox(self, 91, "Habitat quality on model",wx.Point(20,180))
        wx.EVT_CHECKBOX(self, 91,   self.EvtCheckBox)

        self.insure = wx.CheckBox(self, 94, "Plot movements",wx.Point(160,180))
        wx.EVT_CHECKBOX(self, 94,   self.EvtCheckBox)

        self.insure = wx.CheckBox(self, 95, "Prob.Death",wx.Point(260,180))
        wx.EVT_CHECKBOX(self, 95,   self.EvtCheckBox)        
        
        # Radio Boxes
        self.dispersiveList = ['1', '2', '3', '4', '5', '6',
                      '7', '8', '9', '10']
        rb = wx.RadioBox(self, 92, "Choose dispersive level", wx.Point(20, 210), wx.DefaultSize,
                        self.dispersiveList, 2, wx.RA_SPECIFY_COLS)
        wx.EVT_RADIOBOX(self, 92, self.EvtRadioBox)


    def EvtRadioBox(self, event):
        self.logger.AppendText('Dispersive behaviour: %d\n' % (event.GetInt()+1))
        
    def EvtComboBox(self, event):
        if event.GetId()==93:   #93==Species Profile Combo box
            Form1.species_profile=event.GetString()
            self.logger.AppendText('Species Profile: %s\n' % event.GetString())
        else:
            self.logger.AppendText('EvtComboBox: NEED TO BE SPECIFYED' )
        
        
        
    def OnClick(self,event):
        self.logger.AppendText(" Click on object with Id %d\n" %event.GetId())
        
        if event.GetId()==9:   #9==CHANGE BACKGROUND
            background_filename_list_aux=[]
            for i in range(len(Form1.background_filename)-1):
                background_filename_list_aux.append(Form1.background_filename[i+1])
            background_filename_list_aux.append(Form1.background_filename[0])
            Form1.background_filename=background_filename_list_aux
            
            self.logger.AppendText(" New background ==> %s\n" % Form1.background_filename[0] )
            
            imageFile=Form1.background_filename[0]
            im1 = Image.open(imageFile)
            jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            wx.StaticBitmap(self, -1, jpg1, (350,30), (jpg1.GetWidth(), jpg1.GetHeight()), style=wx.SIMPLE_BORDER)
            self.Refresh()

        if event.GetId()==11:   #11==CHANGE LANDSCAPE
            self.logger.AppendText(" Picking up new landscape ... please wait\n")
            
            Form1.landscape_head, Form1.landscape_matrix,Form1.landscape_grassname_habmat,Form1.landscape_habdist,Form1.landscape_habmat_pid,Form1.landscape_habmat_areapix,Form1.landscape_hqmqlq_quality,Form1.landscape_hqmqlq_AREAqual,Form1.landscape_frag_pid,Form1.landscape_frag_AREApix,Form1.landscape_frag_AREAqual,Form1.landscape_dila01clean_pid,Form1.landscape_dila01clean_AREApix,Form1.landscape_dile01clean_AREAqual,Form1.landscape_dila02clean_pid,Form1.landscape_dila02clean_AREApix,Form1.landscape_dile02clean_AREAqual=pickup_one_landscape()
            
            imageFile=Form1.background_filename[0]
        
            im = Image.new('P', (len(Form1.landscape_matrix),len(Form1.landscape_matrix)))  # 'P' for palettized
            data = sum(Form1.landscape_matrix, [])  # flatten data
            im.putdata(data)
            pal = color_pallete()
            im.putpalette(pal)
            im.save(Form1.background_filename[0])
                
            imageFile=Form1.background_filename[0]
            if Form1.plotmovements==1:
                im1 = Image.open(imageFile)
                jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                wx.StaticBitmap(self, -1, jpg1, (350,30), (jpg1.GetWidth(), jpg1.GetHeight()), style=wx.SIMPLE_BORDER)
            
            Form1.background_filename=Form1.background_filename_start
            
            self.logger.AppendText(" New landscape: %s\n" % Form1.landscape_grassname_habmat )
            self.Refresh()

            
        if event.GetId()==10:   #10==START
            Form1.experiment_info=datetime.now()
            for nruns in range(Form1.numberruns):
                if nruns>=0:
                    self.logger.AppendText("  ...........\n   Simulation started...\n")
                    self.logger.AppendText("  ...Landscape: %s\n"    % Form1.landscape_grassname_habmat)
                    self.logger.AppendText("  ...PopSize  : %d\n"    % Form1.start_popsize)
                    self.logger.AppendText("  ...NumSteps : %d\n"    % Form1.timesteps)
                    self.logger.AppendText("  ...MovDstPix: %0.1f\n" % Form1.movement_dist_sigma_pixel)
                    self.logger.AppendText("  ...OnDispFact: %0.1f\n" % Form1.when_dispersing_distance_factor)
                    self.logger.AppendText("  ...HoRa.size: %d\n"    % Form1.homerangesize)
                    self.logger.AppendText("  ...SpProfile: %s\n"    % Form1.species_profile)
                #END if nruns==0:
                
                self.logger.AppendText(".................................................\n")
                self.logger.AppendText("[RUN %s] :::" % str(nruns+1))
                time_starting = time.clock()
    
                forest=getForest(Form1.landscape_matrix)
                indiv_xy = populate(forest, Form1.start_popsize)
    
                indiv_xy_initpos=[]
                indiv_xy_quadrant=[]
                indiv_totaldistance=[]
                indiv_age = []
                indiv_isfemale = []
                
                indiv_islive = []
                indiv_islive_timestep_waslive = []
                indiv_isdispersing = []
                indiv_isdispersingRESET = []
                indiv_distedgePix = []
                indiv_whichpatchid = []
                indiv_habareapix = []
                indiv_dispdirectionX = []
                indiv_dispdirectionY = []
                indiv_movementcost = []
                indiv_LOCI = []
                indiv_LOCI_START = []
                indiv_number_of_meetings= []
                
    
                for num_of_indiv in range(len(indiv_xy)):
                    indiv_xy_initpos.append([indiv_xy[num_of_indiv][0],indiv_xy[num_of_indiv][1]])
                    indiv_age.append(abs(int(random.normalvariate(mu=Form1.indiv_agemean,sigma=Form1.indiv_agestd)))+1)
                    if (random.uniform(0,1)<Form1.indiv_female_rate):
                        indiv_isfemale.append(1)
                    else:
                        indiv_isfemale.append(0)
                        
                    indiv_islive.append(1)
                    indiv_islive_timestep_waslive.append(0)
                    indiv_totaldistance.append(0)
                    indiv_xy_quadrant.append([0,0])
                    
                    indiv_xy_position=indiv_xy[num_of_indiv]
                    
                    indiv_isdispersing.append(0)
                    indiv_isdispersingRESET.append(0)
                    
                    indiv_movementcost.append(0)
                    
                    indiv_distedgePix.append(estimate_distedgePix.estimate_distedgePix(indiv_xy_position,landscape_habdist=Form1.landscape_habdist))
                    indiv_dispdirectionX.append(choose_dispersaldirection())
                    indiv_dispdirectionY.append(choose_dispersaldirection())
                    
                    aux_LOCI=LOCI_start.LOCI_start(aux_loci_struc=Form1.LOCI_structure)
                    indiv_LOCI.append(aux_LOCI)
                    indiv_LOCI_START.append(aux_LOCI)
                    indiv_number_of_meetings.append(0)
                    
                    if Form1.species_profile=="Habitat dependent":
                        indiv_whichpatchid.append(identify_patchid.identify_patchid(indiv_xy_position, patchid_map=Form1.landscape_habmat_pid))
                        if Form1.include_habitatquality=="HabitatQuality_YES":
                            indiv_habareapix.append(identify_habareapix.identify_habareapix(indiv_xy_position, habareapix_map=Form1.landscape_hqmqlq_AREAqual))
                            Form1.using = "landscape_hqmqlq_AREAqual"
                        else:
                            indiv_habareapix.append(identify_habareapix.identify_habareapix(indiv_xy_position, habareapix_map=Form1.landscape_habmat_areapix))
                            Form1.using = "landscape_habmat_areapix"
                            
                    elif Form1.species_profile=="Frag. dependent" or Form1.species_profile=="Core dependent":
                        ###CHECK = I need to change here, because I still not processed
                        ###    AREAqual for FRAGs
                        ############ NOW ARE OK - BUT IS GOOD TO CHECK IT OUT
                        indiv_whichpatchid.append(identify_patchid.identify_patchid(indiv_xy_position, patchid_map=Form1.landscape_frag_pid))
                        if Form1.include_habitatquality=="HabitatQuality_YES":
                            indiv_habareapix.append(identify_habareapix.identify_habareapix(indiv_xy_position, habareapix_map=Form1.landscape_frag_AREAqual))
                            Form1.using = "landscape_frag_AREAqual"
                        else:
                            indiv_habareapix.append(identify_habareapix.identify_habareapix(indiv_xy_position, habareapix_map=Form1.landscape_frag_AREApix))
                            Form1.using = "landscape_frag_areapix"
                    
                    elif Form1.species_profile=="Moderately generalist":
                        indiv_whichpatchid.append(identify_patchid.identify_patchid(indiv_xy_position, patchid_map=Form1.landscape_dila01clean_pid))
                        if Form1.include_habitatquality=="HabitatQuality_YES":
                            indiv_habareapix.append(identify_habareapix.identify_habareapix(indiv_xy_position, habareapix_map=Form1.landscape_dila01clean_AREAqual))
                            Form1.using = "landscape_dila01clean_AREAqual"
                        else:
                            indiv_habareapix.append(identify_habareapix.identify_habareapix(indiv_xy_position, habareapix_map=Form1.landscape_dila01clean_AREApix))
                            Form1.using = "Form1.landscape_dila01clean_AREApix"
                            
                    elif Form1.species_profile=="Highly generalist":
                        indiv_whichpatchid.append(identify_patchid.identify_patchid(indiv_xy_position, patchid_map=Form1.landscape_dila02clean_pid))
                        if Form1.include_habitatquality=="HabitatQuality_YES":
                            indiv_habareapix.append(identify_habareapix.identify_habareapix(indiv_xy_position, habareapix_map=Form1.landscape_dila02clean_AREAqual))
                            Form1.using = "landscape_dila02clean_AREAqual"
                        else:
                            indiv_habareapix.append(identify_habareapix.identify_habareapix(indiv_xy_position, habareapix_map=Form1.landscape_dila02clean_AREApix))
                            Form1.using = "Form1.landscape_dila02clean_AREApix"
                            
                    elif  Form1.species_profile=="Random walk": 
                        Form1.using = "Not considere AREAPix for random walk"
                    else:
                        pass
                
                error=0
                if Form1.timesteps==0:
                    self.logger.AppendText("\n  ...... ??? Time steps=  %s\n" % Form1.timesteps)
                    d= wx.MessageDialog( self, " Error on Time steps \n"
                                " try again","BioDIM v 1.1 (Landscape genetic embeded)", wx.OK)
                    d.ShowModal() # Shows it
                    d.Destroy() # finally destroy it when finished.
                    error=1
    
                if Form1.homerangesize==0:
                    self.logger.AppendText("\n  ...... ??? Home range size =  %s\n" % Form1.homerangesize)
                    d= wx.MessageDialog( self, " Error on Home range size \n"
                                " try again","BioDIM v 1.1 (Landscape genetic embeded)", wx.OK)
                    d.ShowModal() # Shows it
                    d.Destroy() # finally destroy it when finished.
                    error=1
                    
                if Form1.numberruns==0:
                    self.logger.AppendText("\n  ...... ??? Number of runs =  %s\n" % Form1.numberruns)
                    d= wx.MessageDialog( self, " Error on Number of runs \n"
                                " try again","BioDIM v 1.1 (Landscape genetic embeded)", wx.OK)
                    d.ShowModal() # Shows it
                    d.Destroy() # finally destroy it when finished.
                    error=1
                    
                if Form1.start_popsize==0:
                    self.logger.AppendText("\n  ...... ??? starting population= %s\n" % Form1.start_popsize)
                    d= wx.MessageDialog( self, " Error on Population size \n"
                                " try again","BioDIM v 1.1 (Landscape genetic embeded)", wx.OK)
                    d.ShowModal() # Shows it
                    d.Destroy() # finally destroy it when finished.
                    error=1
    
                if Form1.movement_dist_sigma_pixel==0:
                    self.logger.AppendText("\n  ...... ??? Mov.Dist.Pix= %0.1f\n" % Form1.movement_dist_sigma_pixel)
                    d= wx.MessageDialog( self, " Error Mov.Dist.Pix \n"
                                " try again","BioDIM v 1.1 (Landscape genetic embeded)", wx.OK)
                    d.ShowModal() # Shows it
                    d.Destroy() # finally destroy it when finished.
                    error=1
    
                if Form1.when_dispersing_distance_factor==0:
                    self.logger.AppendText("\n  ...... ??? On dispersing factor = %0.1f\n" % Form1.when_dispersing_distance_factor)
                    d= wx.MessageDialog( self, " Error on dispersing factor \n"
                                " try again","BioDIM v 1.1 (Landscape genetic embeded)", wx.OK)
                    d.ShowModal() # Shows it
                    d.Destroy() # finally destroy it when finished.
                    error=1
                    
                if Form1.indivpixels_whenmoving==0:
                    self.logger.AppendText("\n  ...... ??? Indiv.Size (pix)= %s" % Form1.indivpixels_whenmoving)
                    d= wx.MessageDialog( self, " Error on Indiv.Pix.Size \n"
                                " try again","BioDIM v 1.1 (Landscape genetic embeded)", wx.OK)
                    d.ShowModal() # Shows it
                    d.Destroy() # finally destroy it when finished.
                    error=1
                    
                if error==0:
                    self.logger.AppendText("  [ %s ]\n" % Form1.landscape_grassname_habmat)
                    self.logger.AppendText("USING %s \n" % Form1.using)
                    self.logger.AppendText("\n  ...... Steps:: ")
                    
                    control_isDispersingHistory=[]
                    
                    #actual_step_range=[0,1,2,3,4,5,6,7,8,9,14,19,24,29,39,49,74,99,124,149,174,199,249,299,349,399,449,499,549,599,649,699,749,799,849,899,949,999,1249,1499,1749,1999]
                    actual_step_range=range(0,Form1.timesteps, 5)
                    
                    for actual_step in range(Form1.timesteps):
                        #self.Refresh()
                        
                        if actual_step in actual_step_range:
                            self.logger.AppendText(" %s" % (actual_step+1))
    
                        #------------------ check which dispersal model was choose
                        if Form1.species_profile=='Random walk':
                            indiv_xy, indiv_totaldistance, changed_quadrant=disperse_random_walk(Form1.landscape_matrix,indiv_xy, Form1.movement_dist_sigma_pixel, indiv_totaldistance)
                        elif Form1.species_profile=='Habitat dependent':
                            indiv_xy, indiv_totaldistance, changed_quadrant=disperse_habitat_dependent(indiv_xy, indiv_isdispersing, indiv_totaldistance,indiv_dispdirectionX,indiv_dispdirectionY)
                        elif Form1.species_profile=='Frag. dependent' or Form1.species_profile=='Core dependent':
                            indiv_xy, indiv_totaldistance, changed_quadrant=disperse_habitat_dependent(indiv_xy, indiv_isdispersing, indiv_totaldistance,indiv_dispdirectionX,indiv_dispdirectionY)
                        elif Form1.species_profile=='Moderately generalist':
                            indiv_xy, indiv_totaldistance, changed_quadrant=disperse_habitat_dependent(indiv_xy, indiv_isdispersing, indiv_totaldistance,indiv_dispdirectionX,indiv_dispdirectionY)
                        elif Form1.species_profile=='Highly generalist':
                            indiv_xy, indiv_totaldistance, changed_quadrant=disperse_habitat_dependent(indiv_xy, indiv_isdispersing, indiv_totaldistance,indiv_dispdirectionX,indiv_dispdirectionY)
                        else:
                            self.logger.AppendText("\n  ...... ??? Dispesal model not defined")
                            d= wx.MessageDialog( self, " Species profile Error\n Model under development\n"
                                        " Choose another species","BioDIM v 1.1 (Landscape genetic embeded)", wx.OK)
                            d.ShowModal() # Shows it
                            d.Destroy() # finally destroy it when finished.
                            error=1
                            
                        for num_of_indiv in range(len(indiv_xy)):
                            indiv_age[num_of_indiv]=indiv_age[num_of_indiv]+1
                            indiv_xy_position=indiv_xy[num_of_indiv]
     
                            indiv_xy_quadrant[num_of_indiv][0]+=changed_quadrant[num_of_indiv][0]
                            indiv_xy_quadrant[num_of_indiv][1]+=changed_quadrant[num_of_indiv][1]
                            
                            #####indiv_isdispersing=indiv_isdispersing
                            ##### check above!!!!
                            
                            indiv_distedgePix[num_of_indiv]=estimate_distedgePix.estimate_distedgePix(indiv_xy_position,landscape_habdist=Form1.landscape_habdist)

                            if indiv_islive[num_of_indiv]==1:
                                indiv_islive_timestep_waslive[num_of_indiv]=(actual_step+1)
                                indiv_movementcost[num_of_indiv]=estimate_movement_cost(actualcost=indiv_movementcost[num_of_indiv], distfromedgePix=indiv_distedgePix[num_of_indiv], aux_xy=indiv_xy[num_of_indiv])
                                
                                if Form1.include_probdeath==1:
                                    indiv_islive[num_of_indiv]=kill_individual_new.kill_individual_new(distfromedgePix=indiv_distedgePix[num_of_indiv],tab_mortality=Form1.tab_mortality)
                            if indiv_islive[num_of_indiv]==1:
                                ###\\\ TROCA GENS
                                ###indiv_LOCI = []
                                ###indiv_LOCI_START = []
                                ### check conferir se esta indo ate o ultimo individuo
                                if indiv_isfemale[num_of_indiv]==1:
                                    for other_indiv in range((num_of_indiv+1),len(indiv_xy)):
                                        if indiv_isfemale[other_indiv]==0:
                                            indiv_distance_between_them_inmeters=distance_between_indiv.distance_between_indiv(xy_ind_a=indiv_xy[num_of_indiv],xy_ind_b=indiv_xy[other_indiv],spatialresolution=Form1.spatialresolution)
                                            if indiv_distance_between_them_inmeters < Form1.proximity_between_indiv_meters_threshold:
                                                indiv_number_of_meetings[num_of_indiv]=indiv_number_of_meetings[num_of_indiv]+1
                                                #indiv_number_of_meetings[other_indiv]=indiv_number_of_meetings[other_indiv]+1
                                                #the above line increment MALE meetings
                                                indiv_LOCI[num_of_indiv],indiv_LOCI[other_indiv]=gene_exchance.gene_exchance(indiv_LOCI_indA=indiv_LOCI[num_of_indiv],indiv_LOCI_indB=indiv_LOCI[other_indiv],LOCI_gene_exchange_rate=Form1.LOCI_gene_exchange_rate)
                                        
                                if Form1.species_profile=="Habitat dependent":
                                    indiv_whichpatchid[num_of_indiv]=identify_patchid.identify_patchid(indiv_xy_position, patchid_map=Form1.landscape_habmat_pid)
                                    indiv_habareapix[num_of_indiv]=identify_habareapix.identify_habareapix(indiv_xy_position, habareapix_map=Form1.landscape_habmat_areapix)
                                elif Form1.species_profile=="Frag. dependent" or Form1.species_profile=="Core dependent":
                                    indiv_whichpatchid[num_of_indiv]=identify_patchid.identify_patchid(indiv_xy_position, patchid_map=Form1.landscape_frag_pid)
                                    indiv_habareapix[num_of_indiv]=identify_habareapix.identify_habareapix(indiv_xy_position, habareapix_map=Form1.landscape_frag_AREApix)
                                elif Form1.species_profile=="Moderately generalist":
                                    indiv_whichpatchid[num_of_indiv]=identify_patchid.identify_patchid(indiv_xy_position, patchid_map=Form1.landscape_dila01clean_pid)
                                    indiv_habareapix[num_of_indiv]=identify_habareapix.identify_habareapix(indiv_xy_position, habareapix_map=Form1.landscape_dila01clean_AREApix)
                                elif Form1.species_profile=="Highly generalist":
                                    indiv_whichpatchid[num_of_indiv]=identify_patchid.identify_patchid(indiv_xy_position, patchid_map=Form1.landscape_dila02clean_pid)
                                    indiv_habareapix[num_of_indiv]=identify_habareapix.identify_habareapix(indiv_xy_position, habareapix_map=Form1.landscape_dila02clean_AREApix)
                                elif Form1.species_profile=="Random walk":
                                    pass
                                else:
                                    self.logger.AppendText("\n  ...... ??? Dispesal model not defined")
                                    d= wx.MessageDialog( self, " Species profile Error\n Model under development\n"
                                                " Choose another species","BioDIM v 1.1 (Landscape genetic embeded)", wx.OK)
                                    d.ShowModal() # Shows it
                                    d.Destroy() # finally destroy it when finished.
                                    error=1
                        if Form1.plotmovements==1:
                            plot_walk(Form1.landscape_matrix, indiv_xy, aux_isdispersing=indiv_isdispersing, aux_islive=indiv_islive, nruns=nruns, aux_isdispersingRESET=indiv_isdispersingRESET, timestep=actual_step)
                        
                        indiv_isdispersing=check_overpopulation_onpatch.check_overpopulation_onpatch(indiv_isdispersing, indiv_whichpatchid, indiv_habareapix, indiv_age,spatialresolution=Form1.spatialresolution,homerangesize=Form1.homerangesize)
                        indiv_isdispersing, indiv_isdispersingRESET=reset_isdispersing.reset_isdispersing(indiv_isdispersing, indiv_whichpatchid, indiv_habareapix, indiv_islive, indiv_isdispersingRESET,spatialresolution=Form1.spatialresolution,homerangesize=Form1.homerangesize)
                        
                        if actual_step in actual_step_range:
                            if Form1.plotmovements==1:
                                imageFile=Form1.background_filename[0]
                                im1 = Image.open(imageFile)
                                jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                                wx.StaticBitmap(self, -1, jpg1, (350,30), (jpg1.GetWidth(), jpg1.GetHeight()), style=wx.SIMPLE_BORDER)
                        control_isDispersingHistory.append(sum(indiv_isdispersing))
                        #HERE FINISH ONE TIMESTEP
                        #Below information is stored on each step
                        #print "Num.islive=",str(sum(indiv_islive))
                        if Form1.output_store_ongoingsteps_landscape==1 or Form1.output_store_ongoingsteps_indiv==1:
                            indiv_effectivedistance=estimate_effectivedistance.estimate_effectivedistance(indiv_xy_initpos, indiv_xy,indiv_xy_quadrant,landscape_matrix=Form1.landscape_matrix)
                            organize_output(moment="ongoingstep",grassname_habmat=Form1.landscape_grassname_habmat, isdispersing=indiv_isdispersing,isfemale=indiv_isfemale, islive=indiv_islive, totaldistance=indiv_totaldistance, effectivedistance=indiv_effectivedistance, experiment_info=Form1.experiment_info, actualrun=nruns, actual_step=actual_step, actual_movementcost=indiv_movementcost, timestep_waslive=indiv_islive_timestep_waslive,number_of_meetings=indiv_number_of_meetings,LOCI_start=indiv_LOCI_START,LOCI_end=indiv_LOCI)

                    #END for actual_step in range(0,Form1.timesteps):    
                    ##-----------------------------------
                    ##-----------------------------------
                    ##-----------------------------------
                    #out of for
                    
                    indiv_effectivedistance=estimate_effectivedistance.estimate_effectivedistance(indiv_xy_initpos, indiv_xy,indiv_xy_quadrant,landscape_matrix=Form1.landscape_matrix)
                    
                    organize_output(moment="summary_of_a_run", grassname_habmat=Form1.landscape_grassname_habmat, isdispersing=indiv_isdispersing, isfemale=indiv_isfemale, islive=indiv_islive, totaldistance=indiv_totaldistance, effectivedistance=indiv_effectivedistance, experiment_info=Form1.experiment_info, actualrun=nruns, actual_step=actual_step, actual_movementcost=indiv_movementcost, timestep_waslive=indiv_islive_timestep_waslive,number_of_meetings=indiv_number_of_meetings,LOCI_start=indiv_LOCI_START,LOCI_end=indiv_LOCI)

                    StartingPopsizeTXT='\n\nStarting Pop'+str(Form1.start_popsize)
                    self.logger.AppendText(StartingPopsizeTXT)

                    
                    IsDispersingTXT='\nIs dispersing '+str(sum(indiv_isdispersing))+" of "+str(len(indiv_isdispersing))+" =  "
                    Percentage_dispersing=float(sum(indiv_isdispersing))/ len(indiv_isdispersing) *100.0
    
                    IsDispersingTXT=IsDispersingTXT+str(round(Percentage_dispersing,2))
                    self.logger.AppendText(IsDispersingTXT)
    
                    IsLiveTXT='\nNumber of lives is '+str(sum(indiv_islive))+" of "+str(len(indiv_islive))+" =  "
                    Percentage_IsLive=float(sum(indiv_islive))/ len(indiv_islive) *100.0
    
                    IsLiveTXT=IsLiveTXT+str(round(Percentage_IsLive,2))
                    self.logger.AppendText(IsLiveTXT)
    
                    time_ending = time.clock()
                    time_difference=time_ending-time_starting
                    
                    self.logger.AppendText("\nTime of running = %0.1f minutes\n\n\n" % (time_difference/60.0))
                #end of if error==0:
                
                if nruns==(Form1.numberruns-1):
                    d= wx.MessageDialog( self, " Thanks for simulating \n"
                                    " Finished!","BioDIM v 1.1 (Landscape genetic embeded)", wx.OK)
                    d.ShowModal() # Shows it
                    d.Destroy() # finally destroy it when finished.
                else: #RUN new simulation
                    self.logger.AppendText(" Picking up new landscape ... please wait\n")
                    Form1.landscape_head, Form1.landscape_matrix,Form1.landscape_grassname_habmat,Form1.landscape_habdist,Form1.landscape_habmat_pid,Form1.landscape_habmat_areapix,Form1.landscape_hqmqlq_quality,Form1.landscape_hqmqlq_AREAqual,Form1.landscape_frag_pid,Form1.landscape_frag_AREApix,Form1.landscape_frag_AREAqual,Form1.landscape_dila01clean_pid,Form1.landscape_dila01clean_AREApix,Form1.landscape_dila01clean_AREAqual,Form1.landscape_dila02clean_pid,Form1.landscape_dila02clean_AREApix,Form1.landscape_dila02clean_AREAqual=pickup_one_landscape()
                    
                    if Form1.changehomerangesize==0: #not change
                        pass
                    if Form1.changehomerangesize==1: #uniform distribution
                        Form1.homerangesize=random.uniform(a=Form1.changehomerangesize_P1,b=Form1.changehomerangesize_P2)
                    if Form1.changehomerangesize==2: #normal distribution
                        Form1.homerangesize=random.normalvariate(mu=Form1.changehomerangesize_P1,sigma=Form1.changehomerangesize_P2)
                             
                    Form1.start_popsize=estimate_start_popsize(Form1.landscape_grassname_habmat)
                    
                    imageFile=Form1.background_filename[0]
                
                    im = Image.new('P', (len(Form1.landscape_matrix),len(Form1.landscape_matrix)))  # 'P' for palettized
                    data = sum(Form1.landscape_matrix, [])  # flatten data
                    im.putdata(data)
                    pal = color_pallete()
                    im.putpalette(pal)
                    im.save(Form1.background_filename[0])
                        
                    imageFile=Form1.background_filename[0]
                    im1 = Image.open(imageFile)
                    jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                    wx.StaticBitmap(self, -1, jpg1, (350,30), (jpg1.GetWidth(), jpg1.GetHeight()), style=wx.SIMPLE_BORDER)
                    
                    Form1.background_filename=Form1.background_filename_start

                    self.logger.AppendText(" New landscape: %s\n" % Form1.landscape_grassname_habmat )
                    self.Refresh()

                    
    def EvtText(self, event):
        self.logger.AppendText('EvtText: %s\n' % event.GetString())
        if event.GetId()==20: #20=output_prefix
            Form1.output_prefix=event.GetString()
            
        if event.GetId()==30: #30=popsize
            not_int=0
            try: 
                int(event.GetString())
            except ValueError:
                not_int=1
                
            if not_int==1:
                Form1.start_popsize=0
            else:
                Form1.start_popsize=int(event.GetString())
        if event.GetId()==40: #40=timesteps
            not_int=0
            try: 
                int(event.GetString())
            except ValueError:
                not_int=1
                
            if not_int==1:
                Form1.timesteps=0
            else:
                Form1.timesteps=int(event.GetString())            
        if event.GetId()==50: #50=numberruns
            not_int=0
            try: 
                int(event.GetString())
            except ValueError:
                not_int=1
                
            if not_int==1:
                Form1.numberruns=0
            else:
                Form1.numberruns=int(event.GetString())            
        if event.GetId()==60: #60=homerangesize
            not_int=0
            try: 
                int(event.GetString())
            except ValueError:
                not_int=1
                
            if not_int==1:
                Form1.homerangesize=0
            else:
                Form1.homerangesize=int(event.GetString())
                
            Form1.start_popsize=estimate_start_popsize(Form1.landscape_grassname_habmat)
            Form1.lblstart_popsize = wx.StaticText(self, -1, str(Form1.start_popsize)+"  ",wx.Point(84,123))
            self.logger.AppendText('New start popsize: %d\n' % Form1.start_popsize)
            
        if event.GetId()==70: #70=indivpixels
            not_int=0
            try: 
                int(event.GetString())
            except ValueError:
                not_int=1
                
            if not_int==1:
                Form1.indivpixels_whenmoving=0
            else:
                Form1.indivpixels_whenmoving=int(event.GetString())            
        if event.GetId()==80: #80=movement_dist_sigma_pixel
            not_float=0
            try: 
                float(event.GetString())
            except ValueError:
                not_float=1
                
            if not_float==1:
                Form1.movement_dist_sigma_pixel=0
            else:
                Form1.movement_dist_sigma_pixel=float(event.GetString())
        if event.GetId()==81: #81=when_dispersing_distance_factor
            not_float=0
            try: 
                float(event.GetString())
            except ValueError:
                not_float=1
            
            if not_float==1:
                Form1.when_dispersing_distance_factor=0
            else:
                Form1.when_dispersing_distance_factor=float(event.GetString())
                
                
    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()
    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())
        if event.GetId()==91:
            if event.Checked()==1:
                Form1.include_habitatquality="HabitatQuality_YES"
            else:
                Form1.include_habitatquality="HabitatQuality_NO"
            self.logger.AppendText('   %s\n' % Form1.include_habitatquality)

        if event.GetId()==94: #Form1.plotmovements
            if int(event.Checked())==1:
                Form1.plotmovements=1
            else:
                Form1.plotmovements=0
            self.logger.AppendText('   Plot momevements: %s\n' % str(Form1.plotmovements))
            
        if event.GetId()==95: #Form1.include_probdeath
            if int(event.Checked())==1:
                Form1.include_probdeath=1
            else:
                Form1.include_probdeath=0
            self.logger.AppendText('   Include Prob.of.Death: %s\n' % str(Form1.include_probdeath))

            
    def OnExit(self, event):
        d= wx.MessageDialog( self, " Thanks for simulating \n"
                            " BioDIM v 1.1 (Landscape genetic embeded)","Good bye", wx.OK)
                            # Create a message dialog box
        d.ShowModal() # Shows it
        d.Destroy() # finally destroy it when finished.
        frame.Close(True)  # Close the frame. 

        
#----------------------------------------------------------------------
def head_split_up_line(line):
    line = line.split(' ')
    clean_line={}
    clean_line[line[0]]=line[len(line)-1]
    return clean_line
    
#----------------------------------------------------------------------
def read_landscape_head_ascii_standard(input_land, matrixmode):
    input_file = open(input_land, 'r')
    line = input_file.readline()
    nlines = 0
    head = {}
    while nlines<5:
        line=input_file.readline()
        clean_line = head_split_up_line(line)
        head.update(clean_line)
        nlines += 1
    input_file.close()
    
    input_file = open(input_land, 'r')
    lines = input_file.readlines()
    lines = lines[6:]
    input_file.close()

    matrix = []
    if matrixmode=="int":
        for line in lines:
            matrix.append(map(int, line.strip().split(" ")))
    if matrixmode=="float":
        for line in lines:
            matrix.append(map(float, line.strip().split(" ")))
    if matrixmode=="long":
        for line in lines:
            matrix.append(map(long, line.strip().split(" ")))
    return head, matrix
    
#----------------------------------------------------------------------
def read_landscape_head_ascii_grass(input_land):
    input_file = open(input_land, 'r')
    line = input_file.readline()
    nlines = 0
    head = {}
    while nlines<5:
        line=input_file.readline()
        clean_line = head_split_up_line(line)
        head.update(clean_line)
        nlines += 1
    input_file.close()
    
    input_file = open(input_land, 'r')
    lines = input_file.readlines()
    lines = lines[6:]
    input_file.close()

    matrix = []
    for line in lines:
        matrix.append(map(float, line.strip().split(" ")))
    return head, matrix

#----------------------------------------------------------------------
#......................................................................
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = wx.Frame(None, -1, " BioDIM v1.1 - Biologically scalled DIspersal Model - LANDSCAPE GENETIC EMBEDDED - UofT - LeLab - Feb2010", size=(900,600))
    Form1(frame,-1)
    frame.Show(1)
    
    app.MainLoop()
