#!/c/Python25 python
#---------------------------------------------------------------------------------------
"""
 BioDIM - Biologically scaled Dispersal Model
 Version 1.05b.1 (com pastas)
 
 Milton C. Ribeiro - mcr@rc.unesp.br
 Bernardo B. S. Niebuhr - bernardo_brandaum@yahoo.com.br
 John W. Ribeiro - jw.ribeiro.rc@gmail.com
 
 Laboratorio de Ecologia Espacial e Conservacao
 Universidade Estadual Paulista - UNESP
 Rio Claro - SP - Brasil
 
 BioDim description...
"""
#---------------------------------------------------------------------------------------

import grass.script as grass
from PIL import Image
import wx
import random
import re
import time
import math
import os
#from rpy2 import robjects
from datetime import datetime

ID_ABOUT=101
ID_IBMCFG=102
ID_EXIT=110


#---------------------------------------------------
# Auxiliary modules
#---------------------------------------------------
from read_table import read_table
#---------------------------------------------------
# from head_split_up_line import head_split_up_line
# this function is used in the read_landscape_head_ascii_standard module
#---------------------------------------------------
from distance_between_indiv import  distance_between_indiv_pix_meters # leads with spatial resolution/distance
#---------------------------------------------------
from estimate_distedge import estimate_distedge # leads with spatial resolution/distance
#---------------------------------------------------
from estimate_netdisplacement import estimate_netdisplacement
#---------------------------------------------------

#---------------------------------------------------
# Landscape modules
#---------------------------------------------------
#from select_landscape_grassnames import * 
#---------------------------------------------------
#from export_raster_from_grass import *             ### GRASS FUNCTIONS
#---------------------------------------------------
#from read_landscape_head_ascii_standard import read_landscape_head_ascii_standard
# the three function above are used by pickup_one_landscape
#---------------------------------------------------
from pickup_one_landscape import pickup_one_landscape
#---------------------------------------------------
from get_map_info import map_info
#---------------------------------------------------
from color_pallete import color_pallete
#---------------------------------------------------
from getForest import *                             # leads with spatial resolution - PIXELS - nao precisa mexer
#---------------------------------------------------
from identify_patchid import identify_patchid       # leads with spatial resolution - PIXELS
#---------------------------------------------------
from identify_habarea import identify_habarea       # leads with spatial resolution - PIXELS
#---------------------------------------------------
from check_landscaperange import check_landscaperange # leads with spatial resolution - PIXELS and distance
#---------------------------------------------------

#---------------------------------------------------
# Genetic modules
#---------------------------------------------------
from gene_exchange import gene_exchange             
#---------------------------------------------------
from LOCI_start import LOCI_start
#---------------------------------------------------

#---------------------------------------------------
# Population modules
#---------------------------------------------------
from estimate_start_popsize import estimate_start_popsize # leads with spatial resolution - PIXELS AND AREA
#---------------------------------------------------
from populate import populate_random                       # leads with spatial resolution - PIXELS
#---------------------------------------------------
from check_overpopulation_onpatch import check_overpopulation_onpatch # leads with spatial resolution - PIXELS AND AREA
#---------------------------------------------------
from reset_isdispersing import reset_isdispersing   # leads with spatial resolution - PIXELS AND AREA
#---------------------------------------------------

#---------------------------------------------------
# Mortality modules
#---------------------------------------------------
from mortality import get_safetyness_mortality, kill_individual_new # leads with spatial resolution - PIXELS AND DISTANCE
#---------------------------------------------------
def estimate_movement_cost(tab_safetyness, landscape_matrix, species_profile, aux_xy, include_habitatquality, distfromedge, spatialresolution):
    protecdness = get_safetyness_mortality(tab_in=tab_safetyness, species_profile=species_profile, distMeters=distfromedge, spatialresolution=spatialresolution)
    
    aux=[aux_xy]
    aux, changed_quadrant = check_landscaperange(aux, landscape_matrix)
    YY=aux[0][0]
    XX=aux[0][1]        # leads with spatial resolution - PIXELS
    row=int(YY)
    col=int(XX)
    
    if include_habitatquality == "HabitatQuality_YES":
        habqualyOnPosition=Form1.landscape_hqmqlq_quality[row][col]
    else:
        habqualyOnPosition=1.0

    if protecdness<0.05:
        protecdness=0.05
    if protecdness>1:
        protecdness=1.0
    if habqualyOnPosition<0.05:
        habqualyOnPosition=0.05
    if habqualyOnPosition>1:
        habqualyOnPosition=1.0
    
    cost=1.0/(protecdness*habqualyOnPosition)
    
    return cost

#---------------------------------------------------

#---------------------------------------------------
# Movement modules
#---------------------------------------------------
from rowscols2xy import rowscols2xy
#---------------------------------------------------
#from disperse_random_walk import disperse_random_walk # aqui tem unit testing!!!
#---------------------------------------------------
from choose_dispersaldirection import *
#---------------------------------------------------
from movement import get_listofposition, OnHabitat, disperse_habitat_dependent, disperse_random_walk
#---------------------------------------------------


#---------------------------------------------------
# Output models
#---------------------------------------------------
from create_synthesis import create_synthesis
#---------------------------------------------------
def organize_output(moment, grassname_habmat, isdispersing, isfemale, islive, totaldistance, netdisplacement, step_length, experiment_info, actualrun, actual_step, actual_movementcost, timestep_waslive, number_of_meetings, LOCI_start, LOCI_end, initpos, xy):
    """
    Is there a problem (output name) if nruns > 9999? # Is "myzeros"really used??
    # !!!!!!!!!! a virgula esta correta????
    # da pra verificar se habqual ja existe, acho... se foi definida ali em cima, nao precisa recalcular
    
    This function writes the output - what piece of information is going to be saved,
    how files are going to look like etc.
    Input (Information to be saved):
    - moment:
    - grassname_habmat:
    - isdispersing:
    - isfemale:
    - islive:
    - totaldistance:
    - netdisplacement:
    - experiment_info:
    - actualrun:
    - actual_step:
    - actual_movementcost:
    - timestep_waslive:
    - number_of_meetings:
    - LOCI_start:
    - LOCI_end:
    - initpos: list of pairs (x,y) indicating the position of each animal in the beginning of a simulation
    - xy: list of pairs (x,y) indicating the position of each animal in the current step (as [row, col])
    Output (files):
    - output_prefix_indiv_step.txt: summary of individual information during the simulation
    - output_prefix_landscape_step.txt: summary of landscape information during the simulation
    - output_prefix_indiv.txt: summary of individual information at the end of the simulation
    - output_prefix_landscape.txt: summary of landscape information at the end of the simulation
    """    

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
            x0y0_real = rowscols2xy(initpos, spatialresolution=Form1.spatialresolution, x_west=Form1.x_west, y_north=Form1.y_north)
            xy_real = rowscols2xy(xy, spatialresolution=Form1.spatialresolution, x_west=Form1.x_west, y_north=Form1.y_north)
            if actual_step==0 and actualrun==0 and sum(totaldistance) == 0.0:
                file_output_indiv.write('experiment_info;actualrun;nruns;grassname_habmat;PLAND;CONFIG;HABQUAL;species_profile;include_quality;start_popsize;actual_step;timesteps;indiv;homerangesize;avgsteplength;dispfactor;row0;col0;row;col;x0;y0;x;y;realizedsteplength;isdispersing;isfemale;islive;totaldistance;netdisplacement;actual_movementcost;timestep_waslivem;number_of_meetings;LOCI_start;LOCI_end\n')
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
                HABQUAL=HABQUAL/(len(Form1.landscape_matrix)*len(Form1.landscape_matrix[0]))
                HABQUAL=round(HABQUAL*100,0)
               
                file_output_indiv.write('%s;' % str(HABQUAL))
                file_output_indiv.write('%s;' % Form1.species_profile)
                file_output_indiv.write('%s;' % Form1.include_habitatquality)
                file_output_indiv.write('%s;' % str(Form1.start_popsize))
                file_output_indiv.write('%s;' % str(actual_step+1))
                file_output_indiv.write('%s;' % str(Form1.timesteps))
                file_output_indiv.write('%s;' % str(indiv+1))
                file_output_indiv.write('%s;' % str(Form1.homerangesize))
                file_output_indiv.write('%s;' % str(Form1.avg_movement_dist_meters))
                file_output_indiv.write('%s;' % str(Form1.when_dispersing_distance_factor))
                file_output_indiv.write('%s;' % str(initpos[indiv][0]))
                file_output_indiv.write('%s;' % str(initpos[indiv][1]))
                file_output_indiv.write('%s;' % str(xy[indiv][0]))
                file_output_indiv.write('%s;' % str(xy[indiv][1]))
                file_output_indiv.write('%s;' % str(x0y0_real[indiv][0]))
                file_output_indiv.write('%s;' % str(x0y0_real[indiv][1]))
                file_output_indiv.write('%s;' % str(xy_real[indiv][0]))
                file_output_indiv.write('%s;' % str(xy_real[indiv][1]))
                file_output_indiv.write('%s;' % str(step_length[indiv]))
                file_output_indiv.write('%s;' % str(isdispersing[indiv]))
                file_output_indiv.write('%s;' % str(isfemale[indiv]))
                file_output_indiv.write('%s;' % str(islive[indiv]))                
                file_output_indiv.write('%s;' % str(totaldistance[indiv]))
                file_output_indiv.write('%s;' % str(netdisplacement[indiv]))
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
            if actual_step==0 and actualrun==0 and sum(totaldistance) == 0.0:
                file_output_landscape.write('experiment_info;actualrun;nruns;grassname_habmat;PLAND;CONFIG;HABQUAL;species_profile;include_quality;start_popsize;actual_step;timesteps;homerangesize;avgsteplength;avgrealizedsteplength;dispfactor;isdispersing;isfemale;islive;totaldistance;netdisplacement;actual_movementcost;timestep_waslive;number_of_meetings\n')
            file_output_landscape.write('%s;' % experiment_info)
            file_output_landscape.write('%s;' % str(actualrun+1))
            file_output_landscape.write('%s;' % Form1.numberruns)
            file_output_landscape.write('%s;' % Form1.landscape_grassname_habmat)
            file_output_landscape.write('%s;' % Form1.landscape_grassname_habmat[19:22]) ######### nessas linhas pode dar problema com os novos mapas
            file_output_landscape.write('%s;' % Form1.landscape_grassname_habmat[24:27])
            
            HABQUAL=0
            for row in range(len(Form1.landscape_hqmqlq_quality)):
                for col in range(len(Form1.landscape_hqmqlq_quality[0])):
                    HABQUAL+=Form1.landscape_hqmqlq_quality[row][col]
            HABQUAL=float(HABQUAL)/100.0
            HABQUAL=HABQUAL/(len(Form1.landscape_matrix)*len(Form1.landscape_matrix[0]))
            HABQUAL=round(HABQUAL*100,0)
           
            file_output_landscape.write('%s;' % str(HABQUAL))
            file_output_landscape.write('%s;' % Form1.species_profile)
            file_output_landscape.write('%s;' % Form1.include_habitatquality)
            file_output_landscape.write('%s;' % str(Form1.start_popsize))
            file_output_landscape.write('%s;' % str(actual_step+1))  
            file_output_landscape.write('%s;' % str(Form1.timesteps))
            file_output_landscape.write('%s;' % str(Form1.homerangesize))
            file_output_landscape.write('%s;' % str(Form1.avg_movement_dist_meters))
            #if type(step_length[0]) == 'str':
                #mean_sl = 'NA'
            #else:
                #mean_sl = sum(step_length)/float(len(step_length))
            #file_output_landscape.write('%s;' % str(mean_sl))
            file_output_landscape.write('%s;' % str(Form1.when_dispersing_distance_factor))
            file_output_landscape.write('%s;' % str(sum(isdispersing)))
            file_output_landscape.write('%s;' % str(sum(isfemale)))
            file_output_landscape.write('%s;' % str(sum(islive)))
            file_output_landscape.write('%s;' % str(  round(float(sum(totaldistance)),2)  ))
            file_output_landscape.write('%s;' % str(  round(float(sum(netdisplacement)),2)  ))
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
                    file_output_indiv.write('experiment_info;actualrun;nruns;grassname_habmat;PLAND;CONFIG;HABQUAL;species_profile;include_quality;start_popsize;timesteps;indiv;homerangesize;avgsteplength;dispfactor;isdispersing;isfemale;islive;totaldistance;netdisplacement;actual_movementcost;timestep_waslive;number_of_meetings;LOCI_start;LOCI_end\n')
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
                HABQUAL=HABQUAL/(len(Form1.landscape_matrix)*len(Form1.landscape_matrix[0]))
                HABQUAL=round(HABQUAL*100,0)
            
                file_output_indiv.write('%s;' % str(HABQUAL))                
                file_output_indiv.write('%s;' % Form1.species_profile)
                file_output_indiv.write('%s;' % Form1.include_habitatquality)
                file_output_indiv.write('%s;' % str(Form1.start_popsize))
                file_output_indiv.write('%s;' % str(Form1.timesteps))
                file_output_indiv.write('%s;' % str(indiv+1))
                file_output_indiv.write('%s;' % str(Form1.homerangesize))
                file_output_indiv.write('%s;' % str(Form1.avg_movement_dist_meters))
                file_output_indiv.write('%s;' % str(Form1.when_dispersing_distance_factor))
                file_output_indiv.write('%s;' % str(isdispersing[indiv]))
                file_output_indiv.write('%s;' % str(isfemale[indiv]))
                file_output_indiv.write('%s;' % str(islive[indiv]))
                file_output_indiv.write('%s;' % str(totaldistance[indiv]))
                file_output_indiv.write('%s;' % str(netdisplacement[indiv]))
                file_output_indiv.write('%s;' % str(actual_movementcost[indiv]))
                file_output_indiv.write('%s;' % str(timestep_waslive[indiv]))
                file_output_indiv.write('%s;' % str(number_of_meetings[indiv]))
                file_output_indiv.write('%s;' % str(LOCI_start[indiv]))
                file_output_indiv.write('%s'  % str(LOCI_end[indiv]))
                file_output_indiv.write('\n')
            file_output_indiv.close()
            
            create_synthesis(output_filename_indiv)
    
        if Form1.output_store_summary_landscape==1:
            output_filename_landscape=Form1.output_prefix+"_landscape.txt"
            file_output_landscape=open(output_filename_landscape,"a")
            if actualrun==0:
                file_output_landscape.write('experiment_info;actualrun;nruns;grassname_habmat;PLAND;CONFIG;HABQUAL;species_profile;include_quality;start_popsize;timesteps;homerangesize;avgsteplength;dispfactor;isdispersing;isfemale;islive;totaldistance;netdisplacement;actual_movementcost;timestep_waslive;number_of_meetings\n')
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
            HABQUAL=HABQUAL/(len(Form1.landscape_matrix)*len(Form1.landscape_matrix[0]))
            HABQUAL=round(HABQUAL*100,0)
            
            file_output_landscape.write('%s;' % str(HABQUAL))
            file_output_landscape.write('%s;' % Form1.species_profile)
            file_output_landscape.write('%s;' % Form1.include_habitatquality)
            file_output_landscape.write('%s;' % str(Form1.start_popsize))
            file_output_landscape.write('%s;' % str(Form1.timesteps))
            file_output_landscape.write('%s;' % str(Form1.homerangesize))
            file_output_landscape.write('%s;' % str(Form1.avg_movement_dist_meters))
            file_output_landscape.write('%s;' % str(Form1.when_dispersing_distance_factor))            
            file_output_landscape.write('%s;' % str(sum(isdispersing)))
            file_output_landscape.write('%s;' % str(sum(isfemale)))
            file_output_landscape.write('%s;' % str(sum(islive)))
            file_output_landscape.write('%s;' % str(  round(float(sum(totaldistance)),2)  ))
            file_output_landscape.write('%s;' % str(  round(float(sum(netdisplacement)),2)  ))
            file_output_landscape.write('%s;' % str(max(actual_movementcost)))
            file_output_landscape.write('%s;' % str(sum(timestep_waslive)))
            file_output_landscape.write('%s'  % str(sum(number_of_meetings)))
            file_output_landscape.write('\n')
            file_output_landscape.close()
            
        
#---------------------------------------
from visualization import plot_walk
#---------------------------------------

#---------------------------------------
# Main structure of the program
class Form1(wx.Panel):
    
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        
        Form1.biodim_version = 'BioDIM v. 1.05b.1'
        #------------------------------------------------
        Form1.UserBaseMap=False
        
        Form1.defaultDIR = os.getcwd()
        Form1.tempDir='../temp'
        Form1.inputDir='../input'
        Form1.outputDir='../output'
        Form1.pyDir='../py'
        Form1.auxDir='../auxfiles'
        
        #------------------------------------------------
        # Initializing parameters
        
        Form1.include_habitatquality="HabitatQuality_NO"
        Form1.plotmovements=0
        Form1.include_probdeath=0
        Form1.exportPNG=True
        
        # Mortality parameters - in the future we will not need that anymore...
        os.chdir(Form1.defaultDIR)
        os.chdir(Form1.inputDir)
        
        Form1.tab_safetyness=read_table("_models_safetyness.txt")
        Form1.tab_mortality=read_table("_models_mortality.txt")
        
        # Output parameters
        Form1.output_store_ongoingsteps_indiv=1
        Form1.output_store_ongoingsteps_landscape=1
        Form1.output_store_summary_indiv=1
        Form1.output_store_summary_landscape=1
        
        self.speciesList = ['Random walk','Core dependent','Frag. dependent', 'Habitat dependent', 'Moderately generalist', 'Highly generalist']

        Form1.species_profile=self.speciesList[3]
        
        Form1.start_popsize=5
        Form1.numberruns=100
        Form1.timesteps=200
        #***********************************************
        # list of maps
        if Form1.UserBaseMap:
            if Form1.exportPNG:
                Form1.background_filename=["random_landscape_habmat.png","random_landscape_habdist.png","random_landscape_habmat_pid.png","random_landscape_habmat_areapix.png","random_landscape_frag_pid.png","random_landscape_frag_AREApix.png"]
            else:
                Form1.background_filename=["random_landscape_habmat.png"]
        else:
            if Form1.exportPNG:
                Form1.background_filename=["random_landscape_hqmqlq.png","random_landscape_habmat.png","random_landscape_habdist.png","random_landscape_habmat_pid.png","random_landscape_habmat_areapix.png","random_landscape_hqmqlq_quality.png","random_landscape_hqmqlq_AREAqual.png","random_landscape_frag_pid.png","random_landscape_frag_AREApix.png","random_landscape_frag_AREAqual.png"]
            else:
                Form1.background_filename=["random_landscape_hqmqlq.png","random_landscape_habmat.png"]
                
        Form1.background_filename_start=Form1.background_filename

        #LOCI Informations -----------------------------
        Form1.LOCI_structure=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0],[0,0],[0,0,0,0,0,0]] # here we define the structure of the loci
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
        
        # Plot walk settings
        Form1.indivpixels_whenmoving=1
        Form1.indivpixels_isdispersing=1
        Form1.indivpixels_isNOTlive=1
       
        # Movement settings
        Form1.avg_movement_dist_meters=60.0 # average step length in each time unit, in meters
        Form1.when_dispersing_distance_factor=3.0
        
        Form1.indiv_agemean = 100
        Form1.indiv_agestd  = 20
        Form1.indiv_female_rate = 0.5
        
        #*************************************************
        #Form1.spatialresolution=30 #resolution in meters
        Form1.output_prefix="_explandgen01_mca_t02"
        
        #-------------------------------------------------
        # Initializing GUI
        
        self.quote = wx.StaticText(self, id=-1, label=Form1.biodim_version+" - landscape genetic embedded", pos=wx.Point(20, 30))
        
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.quote.SetForegroundColour("blue")
        self.quote.SetFont(font)

        # ------------------------
        # Selecting a landscape and calculating initial population
        if Form1.UserBaseMap:
            Form1.landscape_head, Form1.landscape_matrix, Form1.landscape_grassname_habmat, Form1.landscape_habdist, Form1.landscape_habmat_pid, Form1.landscape_habmat_areapix, Form1.landscape_frag_pid, Form1.landscape_frag_AREApix, Form1.landscape_dila01clean_pid, Form1.landscape_dila01clean_AREApix, Form1.landscape_dila02clean_pid, Form1.landscape_dila02clean_AREApix=pickup_one_landscape(Form1.defaultDIR, Form1.inputDir, Form1.tempDir, userbasemap=Form1.UserBaseMap, exportPNG=Form1.exportPNG)
        else:
            Form1.landscape_head, Form1.landscape_matrix, Form1.landscape_grassname_habmat, Form1.landscape_habdist,Form1.landscape_habmat_pid,Form1.landscape_habmat_areapix,Form1.landscape_hqmqlq_quality,Form1.landscape_hqmqlq_AREAqual,Form1.landscape_frag_pid,Form1.landscape_frag_AREApix,Form1.landscape_frag_AREAqual,Form1.landscape_dila01clean_pid,Form1.landscape_dila01clean_AREApix,Form1.landscape_dila01clean_AREAqual,Form1.landscape_dila02clean_pid,Form1.landscape_dila02clean_AREApix,Form1.landscape_dila02clean_AREAqual=pickup_one_landscape(Form1.defaultDIR, Form1.inputDir, Form1.tempDir, userbasemap=Form1.UserBaseMap, exportPNG=Form1.exportPNG)
        
        if Form1.UserBaseMap:
            pland, forest=getForest_habmat(landscape_matrix = Form1.landscape_matrix)
        else:
            pland, forest=getForest(landscape_matrix = Form1.landscape_matrix)        
        
        # Map information - in principle res_x and res_y are equal - we can ignore res_y
        Form1.mapdims, Form1.x_west, Form1.x_east, Form1.y_south, Form1.y_north, Form1.spatialresolution, res_y = map_info(landscape=Form1.landscape_grassname_habmat)        
        
        # Initial population size
        Form1.start_popsize=estimate_start_popsize(Form1.landscape_matrix, pland, Form1.homerangesize, Form1.spatialresolution)
        
        # ------------------------
        # Initializing GUI

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
        os.chdir(Form1.defaultDIR)
        os.chdir(Form1.tempDir) #acho que vai aqui isso.. ele vai mudar as imagens que mostra no programa
        im = Image.new('P', (len(Form1.landscape_matrix),len(Form1.landscape_matrix[0])))  # 'P' for palettized
        data = sum(Form1.landscape_matrix, [])  # flatten data
        im.putdata(data)
        pal = color_pallete(userbase = Form1.UserBaseMap)
        im.putpalette(pal)
        im.save(Form1.background_filename[0])
            
        imageFile=Form1.background_filename[0]
        im1 = Image.open(imageFile)
        jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(self, -1, jpg1, (450,30), (jpg1.GetWidth(), jpg1.GetHeight()), style=wx.SIMPLE_BORDER)
        
        ##------------ LElab_logo
        #setinput
        os.chdir(Form1.defaultDIR)
        os.chdir(Form1.auxDir) # os logos estao na pasta input
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
        
        Form1.lblavg_movement_dist_meters = wx.StaticText(self, -1, "Avg.Step.Length(m):",wx.Point(125,120))
        Form1.edtavg_movement_dist_meters = wx.TextCtrl(self, 80, str(Form1.avg_movement_dist_meters), wx.Point(195, 120), wx.Size(30,-1))
        wx.EVT_TEXT(self, 80, self.EvtText)
        wx.EVT_CHAR(Form1.edtavg_movement_dist_meters, self.EvtChar)
        
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
        
        ##################################################
        # Isso nao eh usado em lugar algum!!!
        # Radio Boxes
        #self.dispersiveList = ['1', '2', '3', '4', '5', '6',
                      #'7', '8', '9', '10']
        #rb = wx.RadioBox(self, 92, "Choose dispersive level", wx.Point(20, 210), wx.DefaultSize,
                        #self.dispersiveList, 2, wx.RA_SPECIFY_COLS)
        #wx.EVT_RADIOBOX(self, 92, self.EvtRadioBox)


    def EvtRadioBox(self, event):
        self.logger.AppendText('Dispersive behaviour: %d\n' % (event.GetInt()+1))
        
    def EvtComboBox(self, event):
        if event.GetId()==93:   #93==Species Profile Combo box
            Form1.species_profile=event.GetString()
            self.logger.AppendText('Species Profile: %s\n' % event.GetString())
        else:
            self.logger.AppendText('EvtComboBox: NEED TO BE SPECIFIED' )
        
    def OnClick(self,event):
        self.logger.AppendText(" Click on object with Id %d\n" %event.GetId())
        
        ###### Se formos tirar os pngs, precisamos mudar aqui
        if event.GetId()==9:   #9==CHANGE BACKGROUND
            background_filename_list_aux=[]
            for i in range(len(Form1.background_filename)-1):
                background_filename_list_aux.append(Form1.background_filename[i+1])
            background_filename_list_aux.append(Form1.background_filename[0])
            Form1.background_filename=background_filename_list_aux
            
            self.logger.AppendText(" New background ==> %s\n" % Form1.background_filename[0] )
            
            os.chdir(Form1.defaultDIR)
            os.chdir(Form1.tempDir)
            imageFile=Form1.background_filename[0]
            im1 = Image.open(imageFile)
            jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            wx.StaticBitmap(self, -1, jpg1, (450,30), (jpg1.GetWidth(), jpg1.GetHeight()), style=wx.SIMPLE_BORDER)
            self.Refresh()
            
        ###### Se formos tirar os pngs, precisamos mudar aqui
        if event.GetId()==11:   #11==CHANGE LANDSCAPE
            self.logger.AppendText(" Picking up new landscape ... please wait\n")
            
            #pickupland scape
            if Form1.UserBaseMap:
                Form1.landscape_head, Form1.landscape_matrix, Form1.landscape_grassname_habmat, Form1.landscape_habdist, Form1.landscape_habmat_pid, Form1.landscape_habmat_areapix, Form1.landscape_frag_pid, Form1.landscape_frag_AREApix, Form1.landscape_dila01clean_pid, Form1.landscape_dila01clean_AREApix, Form1.landscape_dila02clean_pid, Form1.landscape_dila02clean_AREApix=pickup_one_landscape(Form1.defaultDIR, Form1.inputDir, Form1.tempDir, userbasemap=Form1.UserBaseMap, exportPNG=Form1.exportPNG)
            else:
                Form1.landscape_head, Form1.landscape_matrix, Form1.landscape_grassname_habmat, Form1.landscape_habdist, Form1.landscape_habmat_pid, Form1.landscape_habmat_areapix,Form1.landscape_hqmqlq_quality,Form1.landscape_hqmqlq_AREAqual,Form1.landscape_frag_pid,Form1.landscape_frag_AREApix,Form1.landscape_frag_AREAqual,Form1.landscape_dila01clean_pid,Form1.landscape_dila01clean_AREApix,Form1.landscape_dila01clean_AREAqual,Form1.landscape_dila02clean_pid,Form1.landscape_dila02clean_AREApix,Form1.landscape_dila02clean_AREAqual=pickup_one_landscape(Form1.defaultDIR, Form1.inputDir, Form1.tempDir, userbasemap=Form1.UserBaseMap, exportPNG=Form1.exportPNG)
                        
            # Map information - in principle res_x and res_y are equal - we can ignore res_y
            Form1.mapdims, Form1.x_west, Form1.x_east, Form1.y_south, Form1.y_north, Form1.spatialresolution, res_y = map_info(landscape=Form1.landscape_grassname_habmat)        
               
            # background
            os.chdir(Form1.defaultDIR)
            os.chdir(Form1.tempDir) 
            imageFile=Form1.background_filename_start[0]
        
            im = Image.new('P', (len(Form1.landscape_matrix),len(Form1.landscape_matrix[0])))  # 'P' for palettized
            data = sum(Form1.landscape_matrix, [])  # flatten data
            im.putdata(data)
            pal = color_pallete(userbase = Form1.UserBaseMap)
            im.putpalette(pal)
            im.save(Form1.background_filename_start[0])
                
            imageFile=Form1.background_filename_start[0]
            #if Form1.plotmovements==1:
            im1 = Image.open(imageFile)
            jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            wx.StaticBitmap(self, -1, jpg1, (450,30), (jpg1.GetWidth(), jpg1.GetHeight()), style=wx.SIMPLE_BORDER)
            
            Form1.background_filename=Form1.background_filename_start
            
            self.logger.AppendText(" New landscape: %s\n" % Form1.landscape_grassname_habmat )
            self.Refresh()

        #-----------------------------------------------------
        # Here is the beginning of a run
        
        if event.GetId()==10:   #10==START
            Form1.experiment_info=datetime.now()
            for nruns in range(Form1.numberruns):
                if nruns>=0:
                    self.logger.AppendText("  ...........\n   Simulation started...\n")
                    self.logger.AppendText("  ...Landscape: %s\n"    % Form1.landscape_grassname_habmat)
                    self.logger.AppendText("  ...PopSize  : %d\n"    % Form1.start_popsize)
                    self.logger.AppendText("  ...NumSteps : %d\n"    % Form1.timesteps)
                    self.logger.AppendText("  ...MovDstPix: %0.1f\n" % Form1.avg_movement_dist_meters)
                    self.logger.AppendText("  ...OnDispFact: %0.1f\n" % Form1.when_dispersing_distance_factor)
                    self.logger.AppendText("  ...HoRa.size: %d\n"    % Form1.homerangesize)
                    self.logger.AppendText("  ...SpProfile: %s\n"    % Form1.species_profile)
                #END if nruns==0:
                
                self.logger.AppendText(".................................................\n")
                self.logger.AppendText("[RUN %s] :::" % str(nruns+1))
                time_starting = time.clock()
    
                #----------------------
                # Initializing variables within a run
                if Form1.UserBaseMap:
                    pland, forest=getForest_habmat(landscape_matrix = Form1.landscape_matrix)
                else:
                    pland, forest=getForest(landscape_matrix = Form1.landscape_matrix)
                
                indiv_xy = populate_random(forest, Form1.start_popsize) # rows and cols in which animals are initally
    
                indiv_xy_initpos=[]
                indiv_xy_quadrant=[]
                indiv_totaldistance=[]
                indiv_age = []
                indiv_isfemale = []
                
                indiv_islive = []
                indiv_islive_timestep_waslive = []
                indiv_isdispersing = []
                indiv_isdispersingRESET = []
                indiv_movdirectionX = []
                indiv_movdirectionY = []
                indiv_distedge = []
                indiv_whichpatchid = []
                indiv_habarea = []
                indiv_movementcost = []
                indiv_steplength = []
                indiv_LOCI = []
                indiv_LOCI_START = []
                indiv_number_of_meetings= []
                
    
                for num_of_indiv in range(len(indiv_xy)):
                    indiv_xy_initpos.append([indiv_xy[num_of_indiv][0],indiv_xy[num_of_indiv][1]])
                    indiv_age.append(abs(int(random.normalvariate(mu=Form1.indiv_agemean, sigma=Form1.indiv_agestd)))+1)
                    if (random.uniform(0,1) < Form1.indiv_female_rate):
                        indiv_isfemale.append(1)
                    else:
                        indiv_isfemale.append(0)
                        
                    indiv_islive.append(1)
                    indiv_islive_timestep_waslive.append(0)
                    indiv_totaldistance.append(0.0)
                    indiv_xy_quadrant.append([0,0])
                    
                    indiv_xy_position=indiv_xy[num_of_indiv]
                    
                    indiv_isdispersing.append(0)
                    indiv_isdispersingRESET.append(0)
                    #indiv_movdirectionX.append('NA')
                    #indiv_movdirectionY.append('NA')
                    indiv_movdirectionX.append(choose_dispersaldirection())
                    indiv_movdirectionY.append(choose_dispersaldirection())
                    
                    indiv_movementcost.append(0.0)
                    indiv_steplength.append('NA')
                    
                    indiv_distedge.append(estimate_distedge(indiv_xy_position, landscape_habdist=Form1.landscape_habdist))
                    
                    aux_LOCI=LOCI_start(aux_loci_struc=Form1.LOCI_structure)
                    indiv_LOCI.append(aux_LOCI)
                    indiv_LOCI_START.append(aux_LOCI)
                    indiv_number_of_meetings.append(0)
                    
                    if Form1.species_profile=="Habitat dependent":
                        indiv_whichpatchid.append(identify_patchid(indiv_xy_position, patchid_map=Form1.landscape_habmat_pid))
                        if Form1.include_habitatquality=="HabitatQuality_YES":
                            indiv_habarea.append(identify_habarea(indiv_xy_position, habarea_map=Form1.landscape_hqmqlq_AREAqual))
                            Form1.using = "landscape_hqmqlq_AREAqual"
                        else:
                            indiv_habarea.append(identify_habarea(indiv_xy_position, habarea_map=Form1.landscape_habmat_areapix))
                            Form1.using = "landscape_habmat_areapix"
                            
                    elif Form1.species_profile=="Frag. dependent" or Form1.species_profile=="Core dependent":
                        ###CHECK = I need to change here, because I still not processed
                        ###    AREAqual for FRAGs
                        ############ NOW ARE OK - BUT IS GOOD TO CHECK IT OUT
                        indiv_whichpatchid.append(identify_patchid(indiv_xy_position, patchid_map=Form1.landscape_frag_pid))
                        if Form1.include_habitatquality=="HabitatQuality_YES":
                            indiv_habarea.append(identify_habarea(indiv_xy_position, habarea_map=Form1.landscape_frag_AREAqual))
                            Form1.using = "landscape_frag_AREAqual"
                        else:
                            indiv_habarea.append(identify_habarea(indiv_xy_position, habarea_map=Form1.landscape_frag_AREApix))
                            Form1.using = "landscape_frag_areapix"
                    
                    elif Form1.species_profile=="Moderately generalist":
                        indiv_whichpatchid.append(identify_patchid(indiv_xy_position, patchid_map=Form1.landscape_dila01clean_pid))
                        if Form1.include_habitatquality=="HabitatQuality_YES":
                            indiv_habarea.append(identify_habarea(indiv_xy_position, habarea_map=Form1.landscape_dila01clean_AREAqual))
                            Form1.using = "landscape_dila01clean_AREAqual"
                        else:
                            indiv_habarea.append(identify_habarea(indiv_xy_position, habarea_map=Form1.landscape_dila01clean_AREApix))
                            Form1.using = "Form1.landscape_dila01clean_AREApix"
                            
                    elif Form1.species_profile=="Highly generalist":
                        indiv_whichpatchid.append(identify_patchid(indiv_xy_position, patchid_map=Form1.landscape_dila02clean_pid))
                        if Form1.include_habitatquality=="HabitatQuality_YES":
                            indiv_habarea.append(identify_habarea(indiv_xy_position, habarea_map=Form1.landscape_dila02clean_AREAqual))
                            Form1.using = "landscape_dila02clean_AREAqual"
                        else:
                            indiv_habarea.append(identify_habarea(indiv_xy_position, habarea_map=Form1.landscape_dila02clean_AREApix))
                            Form1.using = "Form1.landscape_dila02clean_AREApix"
                            
                    elif  Form1.species_profile=="Random walk": 
                        Form1.using = "Not considere AREAPix for random walk"
                    else:
                        pass
                
                error=0
                if Form1.timesteps<=0:
                    self.logger.AppendText("\n  ...... ??? Time steps=  %s\n" % Form1.timesteps)
                    d= wx.MessageDialog( self, " Error on Time steps \n"
                                " try again", Form1.biodim_version+" (Landscape genetic embeded)", wx.OK)
                    d.ShowModal() # Shows it
                    d.Destroy() # finally destroy it when finished.
                    error=1
    
                if Form1.homerangesize<=0:
                    self.logger.AppendText("\n  ...... ??? Home range size =  %s\n" % Form1.homerangesize)
                    d= wx.MessageDialog( self, " Error on Home range size \n"
                                " try again", Form1.biodim_version+" (Landscape genetic embeded)", wx.OK)
                    d.ShowModal() # Shows it
                    d.Destroy() # finally destroy it when finished.
                    error=1
                    
                if Form1.numberruns<=0:
                    self.logger.AppendText("\n  ...... ??? Number of runs =  %s\n" % Form1.numberruns)
                    d= wx.MessageDialog( self, " Error on Number of runs \n"
                                " try again", Form1.biodim_version+" (Landscape genetic embeded)", wx.OK)
                    d.ShowModal() # Shows it
                    d.Destroy() # finally destroy it when finished.
                    error=1
                    
                if Form1.start_popsize<=0:
                    self.logger.AppendText("\n  ...... ??? starting population= %s\n" % Form1.start_popsize)
                    d= wx.MessageDialog( self, " Error on Population size \n"
                                " try again", Form1.biodim_version+" (Landscape genetic embeded)", wx.OK)
                    d.ShowModal() # Shows it
                    d.Destroy() # finally destroy it when finished.
                    error=1
    
                if Form1.avg_movement_dist_meters<=0:
                    self.logger.AppendText("\n  ...... ??? Mov.Dist.Pix= %0.1f\n" % Form1.avg_movement_dist_meters)
                    d= wx.MessageDialog( self, " Error Mov.Dist.Pix \n"
                                " try again", Form1.biodim_version+" (Landscape genetic embeded)", wx.OK)
                    d.ShowModal() # Shows it
                    d.Destroy() # finally destroy it when finished.
                    error=1
    
                if Form1.when_dispersing_distance_factor<=0:
                    self.logger.AppendText("\n  ...... ??? On dispersing factor = %0.1f\n" % Form1.when_dispersing_distance_factor)
                    d= wx.MessageDialog( self, " Error on dispersing factor \n"
                                " try again", Form1.biodim_version+" (Landscape genetic embeded)", wx.OK)
                    d.ShowModal() # Shows it
                    d.Destroy() # finally destroy it when finished.
                    error=1
                    
                if Form1.indivpixels_whenmoving<=0:
                    self.logger.AppendText("\n  ...... ??? Indiv.Size (pix)= %s" % Form1.indivpixels_whenmoving)
                    d= wx.MessageDialog( self, " Error on Indiv.Pix.Size \n"
                                " try again", Form1.biodim_version+" (Landscape genetic embeded)", wx.OK)
                    d.ShowModal() # Shows it
                    d.Destroy() # finally destroy it when finished.
                    error=1
                    
                if error==0:
                    self.logger.AppendText("  [ %s ]\n" % Form1.landscape_grassname_habmat)
                    self.logger.AppendText("USING %s \n" % Form1.using)
                    self.logger.AppendText("\n  ...... Steps:: ")
                    
                    control_isDispersingHistory=[]
                    
                    #Below information is stored on each step
                    #print "Num.islive=",str(sum(indiv_islive))
                    if Form1.output_store_ongoingsteps_landscape==1 or Form1.output_store_ongoingsteps_indiv==1:
                        indiv_netdisplacement = [0.0] * len(indiv_xy)
                        
                        #salvando o txt de output
                        os.chdir(Form1.defaultDIR)
                        os.chdir(Form1.outputDir) #mudando caminho para a pasta de saida
                        organize_output(moment="ongoingstep", grassname_habmat=Form1.landscape_grassname_habmat, isdispersing=indiv_isdispersing, isfemale=indiv_isfemale, islive=indiv_islive, totaldistance=indiv_totaldistance, netdisplacement=indiv_netdisplacement, step_length=indiv_steplength, experiment_info=Form1.experiment_info, actualrun=nruns, actual_step=0, actual_movementcost=indiv_movementcost, timestep_waslive=indiv_islive_timestep_waslive, number_of_meetings=indiv_number_of_meetings, LOCI_start=indiv_LOCI_START, LOCI_end=indiv_LOCI, initpos=indiv_xy_initpos, xy=indiv_xy)
                    
                    
                    #actual_step_range=[0,1,2,3,4,5,6,7,8,9,14,19,24,29,39,49,74,99,124,149,174,199,249,299,349,399,449,499,549,599,649,699,749,799,849,899,949,999,1249,1499,1749,1999]
                    actual_step_range=range(0,Form1.timesteps, 5)
                    
                    for actual_step in range(Form1.timesteps):
                        #self.Refresh()
                        
                        if actual_step in actual_step_range:
                            self.logger.AppendText(" %s" % (actual_step+1))
                            # so para acompanhar, podemos tirar; acho que deixa um pouco mais lento (mas nao muito)
                            grass.run_command("g.message", message='Step: '+str(actual_step+1))
                            
                        #####################################    
                        # colocar no output o inicio, se for pra dar print no step
                        # antes de se mover, ja seria necessario verificar se algum animal vai escolher dispersar, se Npop > K
    
                        #------------------ check which dispersal model was choose
                        if Form1.species_profile=='Random walk':
                            indiv_xy, indiv_totaldistance, indiv_steplength, changed_quadrant=disperse_random_walk(Form1.landscape_matrix, indiv_xy, Form1.avg_movement_dist_meters, Form1.spatialresolution, indiv_totaldistance)
                        elif 'dependent' in Form1.species_profile or 'generalist' in Form1.species_profile:
                            indiv_xy, indiv_totaldistance, indiv_steplength, changed_quadrant=disperse_habitat_dependent(Form1.landscape_habdist, Form1.landscape_frag_pid, indiv_xy, Form1.species_profile, indiv_isdispersing, indiv_totaldistance, Form1.avg_movement_dist_meters, Form1.spatialresolution, Form1.when_dispersing_distance_factor, indiv_movdirectionX, indiv_movdirectionY)
                        #elif Form1.species_profile=='Habitat dependent' or :
                            #indiv_xy, indiv_totaldistance, indiv_steplength, changed_quadrant=disperse_habitat_dependent(Form1.landscape_habdist, Form1.landscape_frag_pid, indiv_xy, Form1.species_profile, indiv_isdispersing, indiv_totaldistance, Form1.avg_movement_dist_meters, Form1.spatialresolution, Form1.when_dispersing_distance_factor, indiv_movdirectionX, indiv_movdirectionY)
                        #elif Form1.species_profile=='Frag. dependent' or Form1.species_profile=='Core dependent':
                            #indiv_xy, indiv_totaldistance, indiv_steplength, changed_quadrant=disperse_habitat_dependent(Form1.landscape_habdist, Form1.landscape_frag_pid, indiv_xy, Form1.species_profile, indiv_isdispersing, indiv_totaldistance, Form1.avg_movement_dist_meters, Form1.spatialresolution, Form1.when_dispersing_distance_factor, indiv_movdirectionX, indiv_movdirectionY)
                        #elif Form1.species_profile=='Moderately generalist':
                            #indiv_xy, indiv_totaldistance, indiv_steplength, changed_quadrant=disperse_habitat_dependent(Form1.landscape_habdist, Form1.landscape_frag_pid, indiv_xy, Form1.species_profile, indiv_isdispersing, indiv_totaldistance, Form1.avg_movement_dist_meters, Form1.spatialresolution, Form1.when_dispersing_distance_factor, indiv_movdirectionX, indiv_movdirectionY)
                        #elif Form1.species_profile=='Highly generalist':
                            #indiv_xy, indiv_totaldistance, indiv_steplength, changed_quadrant=disperse_habitat_dependent(Form1.landscape_habdist, Form1.landscape_frag_pid, indiv_xy, Form1.species_profile, indiv_isdispersing, indiv_totaldistance, Form1.avg_movement_dist_meters, Form1.spatialresolution, Form1.when_dispersing_distance_factor, indiv_movdirectionX, indiv_movdirectionY)
                        else:
                            self.logger.AppendText("\n  ...... ??? Dispesal model not defined")
                            d= wx.MessageDialog( self, " Species profile Error\n Model under development\n"
                                        " Choose another species", Form1.biodim_version+" (Landscape genetic embeded)", wx.OK)
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
                            
                            indiv_distedge[num_of_indiv]=estimate_distedge(indiv_xy_position, landscape_habdist=Form1.landscape_habdist)

                            if indiv_islive[num_of_indiv]==1:
                                indiv_islive_timestep_waslive[num_of_indiv]=(actual_step+1)
                                indiv_movementcost[num_of_indiv]+=estimate_movement_cost(Form1.tab_safetyness, Form1.landscape_matrix, Form1.species_profile, aux_xy=indiv_xy_position, include_habitatquality=Form1.include_habitatquality, distfromedge=indiv_distedge[num_of_indiv], spatialresolution=Form1.spatialresolution)
                                
                                if Form1.include_probdeath==1:
                                    indiv_islive[num_of_indiv]=kill_individual_new(tab_mortality=Form1.tab_mortality, sp_profile=Form1.species_profile, distfromedge=indiv_distedge[num_of_indiv], spatialres=Form1.spatialresolution)
                            
                            if indiv_islive[num_of_indiv]==1:
                                ###\\\ TROCA GENS
                                ###indiv_LOCI = []
                                ###indiv_LOCI_START = []
                                ### check conferir se esta indo ate o ultimo individuo
                                if indiv_isfemale[num_of_indiv]==1:
                                    for other_indiv in range((num_of_indiv+1),len(indiv_xy)):
                                        if indiv_isfemale[other_indiv]==0:
                                            indiv_distance_between_them_inmeters=distance_between_indiv_pix_meters(xy_ind_a=indiv_xy[num_of_indiv], xy_ind_b=indiv_xy[other_indiv], spatialresolution=Form1.spatialresolution)
                                            if indiv_distance_between_them_inmeters < Form1.proximity_between_indiv_meters_threshold:
                                                indiv_number_of_meetings[num_of_indiv]=indiv_number_of_meetings[num_of_indiv]+1
                                                #indiv_number_of_meetings[other_indiv]=indiv_number_of_meetings[other_indiv]+1
                                                #the above line increment MALE meetings
                                                indiv_LOCI[num_of_indiv], indiv_LOCI[other_indiv] = gene_exchange(indiv_LOCI_indA=indiv_LOCI[num_of_indiv], indiv_LOCI_indB=indiv_LOCI[other_indiv], LOCI_gene_exchange_rate=Form1.LOCI_gene_exchange_rate)
                                        
                                if Form1.species_profile=="Habitat dependent":
                                    indiv_whichpatchid[num_of_indiv]=identify_patchid(indiv_xy_position, patchid_map=Form1.landscape_habmat_pid)
                                    indiv_habarea[num_of_indiv]=identify_habarea(indiv_xy_position, habarea_map=Form1.landscape_habmat_areapix)
                                elif Form1.species_profile=="Frag. dependent" or Form1.species_profile=="Core dependent":
                                    indiv_whichpatchid[num_of_indiv]=identify_patchid(indiv_xy_position, patchid_map=Form1.landscape_frag_pid)
                                    indiv_habarea[num_of_indiv]=identify_habarea(indiv_xy_position, habarea_map=Form1.landscape_frag_AREApix)
                                elif Form1.species_profile=="Moderately generalist":
                                    indiv_whichpatchid[num_of_indiv]=identify_patchid(indiv_xy_position, patchid_map=Form1.landscape_dila01clean_pid)
                                    indiv_habarea[num_of_indiv]=identify_habarea(indiv_xy_position, habarea_map=Form1.landscape_dila01clean_AREApix)
                                elif Form1.species_profile=="Highly generalist":
                                    indiv_whichpatchid[num_of_indiv]=identify_patchid(indiv_xy_position, patchid_map=Form1.landscape_dila02clean_pid)
                                    indiv_habarea[num_of_indiv]=identify_habarea(indiv_xy_position, habarea_map=Form1.landscape_dila02clean_AREApix)
                                elif Form1.species_profile=="Random walk":
                                    pass
                                else:
                                    self.logger.AppendText("\n  ...... ??? Dispesal model not defined")
                                    d= wx.MessageDialog( self, " Species profile Error\n Model under development\n"
                                                " Choose another species", Form1.biodim_version+" (Landscape genetic embeded)", wx.OK)
                                    d.ShowModal() # Shows it
                                    d.Destroy() # finally destroy it when finished.
                                    error=1
                        
                        if Form1.plotmovements==1:                            
                            #plot 
                            os.chdir(Form1.defaultDIR)
                            os.chdir(Form1.outputDir)
                            plot_walk(Form1.landscape_matrix, indiv_xy, aux_isdispersing=indiv_isdispersing, aux_islive=indiv_islive, nruns=nruns, 
                                      aux_isdispersingRESET=indiv_isdispersingRESET, timestep=actual_step, output_prefix=Form1.output_prefix, 
                                      UserBaseMap=Form1.UserBaseMap, indivpixels_isNOTlive=Form1.indivpixels_isNOTlive, 
                                      indivpixels_isdispersing=Form1.indivpixels_isdispersing, indivpixels_whenmoving=Form1.indivpixels_whenmoving)
                        
                        indiv_isdispersing=check_overpopulation_onpatch(indiv_isdispersing, indiv_whichpatchid, indiv_habarea, indiv_age, homerangesize=Form1.homerangesize)
                        indiv_isdispersing, indiv_isdispersingRESET=reset_isdispersing(indiv_isdispersing, indiv_whichpatchid, indiv_habarea, indiv_islive, indiv_isdispersingRESET,spatialresolution=Form1.spatialresolution,homerangesize=Form1.homerangesize)
                        
                        if actual_step in actual_step_range:
                            if Form1.plotmovements==1:
                                #
                                os.chdir(Form1.defaultDIR)
                                os.chdir(Form1.tempDir) # acho que essas chamadas terao que ser aqui mesmo
                                imageFile=Form1.background_filename[0]
                                im1 = Image.open(imageFile)
                                jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                                wx.StaticBitmap(self, -1, jpg1, (450,30), (jpg1.GetWidth(), jpg1.GetHeight()), style=wx.SIMPLE_BORDER)
                        
                        control_isDispersingHistory.append(sum(indiv_isdispersing))
                        #HERE FINISH ONE TIMESTEP
                        
                        #Below information is stored on each step
                        #print "Num.islive=",str(sum(indiv_islive))
                        if Form1.output_store_ongoingsteps_landscape==1 or Form1.output_store_ongoingsteps_indiv==1:
                            indiv_netdisplacement = estimate_netdisplacement(indiv_xy_initpos, indiv_xy, indiv_xy_quadrant, landscape_matrix=Form1.landscape_matrix)
                            
                            #salvando o txt de output
                            os.chdir(Form1.defaultDIR)
                            os.chdir(Form1.outputDir) #mudando caminho para a pasta de saida
                            organize_output(moment="ongoingstep", grassname_habmat=Form1.landscape_grassname_habmat, isdispersing=indiv_isdispersing, isfemale=indiv_isfemale, islive=indiv_islive, totaldistance=indiv_totaldistance, netdisplacement=indiv_netdisplacement, step_length=indiv_steplength, experiment_info=Form1.experiment_info, actualrun=nruns, actual_step=actual_step, actual_movementcost=indiv_movementcost, timestep_waslive=indiv_islive_timestep_waslive, number_of_meetings=indiv_number_of_meetings, LOCI_start=indiv_LOCI_START, LOCI_end=indiv_LOCI, initpos=indiv_xy_initpos, xy=indiv_xy)

                    #END for actual_step in range(0,Form1.timesteps):    
                    ##-----------------------------------
                    ##-----------------------------------
                    ##-----------------------------------
                    #out of for
                    #
                    
                    indiv_netdisplacement=estimate_netdisplacement(indiv_xy_initpos, indiv_xy, indiv_xy_quadrant, landscape_matrix=Form1.landscape_matrix)
                    
                    # salvando txt de output
                    os.chdir(Form1.defaultDIR)
                    os.chdir(Form1.outputDir) #mudando caminho para a pasta de saida
                    organize_output(moment="summary_of_a_run", grassname_habmat=Form1.landscape_grassname_habmat, isdispersing=indiv_isdispersing, isfemale=indiv_isfemale, islive=indiv_islive, totaldistance=indiv_totaldistance, netdisplacement=indiv_netdisplacement, step_length=indiv_steplength, experiment_info=Form1.experiment_info, actualrun=nruns, actual_step=actual_step, actual_movementcost=indiv_movementcost, timestep_waslive=indiv_islive_timestep_waslive, number_of_meetings=indiv_number_of_meetings, LOCI_start=indiv_LOCI_START, LOCI_end=indiv_LOCI, initpos=indiv_xy_initpos, xy=indiv_xy)

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
                                    " Finished!", Form1.biodim_version+" (Landscape genetic embeded)", wx.OK)
                    d.ShowModal() # Shows it
                    d.Destroy() # finally destroy it when finished.
                else: #RUN new simulation
                    self.logger.AppendText(" Picking up new landscape ... please wait\n")
                    
                    # pickup_one_landscape
                    os.chdir(Form1.defaultDIR)
                    os.chdir(Form1.tempDir)
                    if Form1.UserBaseMap:
                        Form1.landscape_head, Form1.landscape_matrix, Form1.landscape_grassname_habmat, Form1.landscape_habdist, Form1.landscape_habmat_pid, Form1.landscape_habmat_areapix, Form1.landscape_frag_pid, Form1.landscape_frag_AREApix, Form1.landscape_dila01clean_pid, Form1.landscape_dila01clean_AREApix, Form1.landscape_dila02clean_pid, Form1.landscape_dila02clean_AREApix=pickup_one_landscape(Form1.defaultDIR, Form1.inputDir, Form1.tempDir, userbasemap=Form1.UserBaseMap, exportPNG=Form1.exportPNG)
                    else:
                        Form1.landscape_head, Form1.landscape_matrix, Form1.landscape_grassname_habmat, Form1.landscape_habdist,Form1.landscape_habmat_pid,Form1.landscape_habmat_areapix,Form1.landscape_hqmqlq_quality,Form1.landscape_hqmqlq_AREAqual,Form1.landscape_frag_pid,Form1.landscape_frag_AREApix,Form1.landscape_frag_AREAqual,Form1.landscape_dila01clean_pid,Form1.landscape_dila01clean_AREApix,Form1.landscape_dila01clean_AREAqual,Form1.landscape_dila02clean_pid,Form1.landscape_dila02clean_AREApix,Form1.landscape_dila02clean_AREAqual=pickup_one_landscape(Form1.defaultDIR, Form1.inputDir, Form1.tempDir, userbasemap=Form1.UserBaseMap, exportPNG=Form1.exportPNG)
                                       
                    if Form1.changehomerangesize==0: #not change
                        pass
                    if Form1.changehomerangesize==1: #uniform distribution
                        Form1.homerangesize=random.uniform(a=Form1.changehomerangesize_P1,b=Form1.changehomerangesize_P2)
                    if Form1.changehomerangesize==2: #normal distribution
                        Form1.homerangesize=random.normalvariate(mu=Form1.changehomerangesize_P1,sigma=Form1.changehomerangesize_P2)
                    
                    if Form1.UserBaseMap:
                        pland, forest=getForest_habmat(landscape_matrix = Form1.landscape_matrix)
                    else:
                        pland, forest=getForest(landscape_matrix = Form1.landscape_matrix)
                        
                    # Map information - in principle res_x and res_y are equal - we can ignore res_y
                    Form1.mapdims, Form1.x_west, Form1.x_east, Form1.y_south, Form1.y_north, Form1.spatialresolution, res_y = map_info(landscape=Form1.landscape_grassname_habmat)        
                    
                    #################################
                    # temos la em cima que colocar a opcao de usar sempre a mesma pop inicial ou iniciar sempre com NPop = K
                    Form1.start_popsize=estimate_start_popsize(Form1.landscape_matrix, pland, Form1.homerangesize, Form1.spatialresolution)                    
                    
                    imageFile=Form1.background_filename[0]
                
                    im = Image.new('P', (len(Form1.landscape_matrix),len(Form1.landscape_matrix[0])))  # 'P' for palettized
                    data = sum(Form1.landscape_matrix, [])  # flatten data
                    im.putdata(data)
                    pal = color_pallete(userbase = Form1.UserBaseMap)
                    im.putpalette(pal)
                    im.save(Form1.background_filename[0])
                        
                    imageFile=Form1.background_filename[0]
                    im1 = Image.open(imageFile)
                    jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                    wx.StaticBitmap(self, -1, jpg1, (450,30), (jpg1.GetWidth(), jpg1.GetHeight()), style=wx.SIMPLE_BORDER)
                    
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
            
            if Form1.UserBaseMap:
                pland, forest=getForest_habmat(landscape_matrix = Form1.landscape_matrix)
            else:
                pland, forest=getForest(landscape_matrix = Form1.landscape_matrix)        
                
            Form1.start_popsize=estimate_start_popsize(Form1.landscape_matrix, pland, Form1.homerangesize, Form1.spatialresolution)                

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
        if event.GetId()==80: #80=avg_movement_dist_meters
            not_float=0
            try: 
                float(event.GetString())
            except ValueError:
                not_float=1
                
            if not_float==1:
                Form1.avg_movement_dist_meters=0
            else:
                Form1.avg_movement_dist_meters=float(event.GetString())
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
        d= wx.MessageDialog( self, " Thanks for simulating \n "+
                            Form1.biodim_version+" (Landscape genetic embeded)","Good bye", wx.OK)
                            # Create a message dialog box
        d.ShowModal() # Shows it
        d.Destroy() # finally destroy it when finished.
        frame.Close(True)  # Close the frame. 


#----------------------------------------------------------------------
# Initializing the software
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = wx.Frame(None, -1, "BioDIM v. 1.05b.1 - Biologically scalled DIspersal Model - LANDSCAPE GENETIC EMBEDDED - LeLab/LEEC - Mar2016", size=(1000,600))
    Form1(frame,-1)
    frame.Show(1)
    
    app.MainLoop()
