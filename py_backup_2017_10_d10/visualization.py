#---------------------------------------------------------------------------------------
"""
 BioDIM - Biologically scaled Dispersal Model
 
 Visualization module

 Functions:
 - plot_walk
 
"""
#---------------------------------------------------------------------------------------

import os
import random
from PIL import Image
from color_pallete import color_pallete 

#---------------------------------------
def plot_walk(landscape_matrix, indiv_xy, aux_isdispersing, aux_islive, nlandscape, nruns, aux_isdispersingRESET, timestep, output_prefix, UserBaseMap, indivpixels_isNOTlive, indivpixels_isdispersing, indivpixels_whenmoving):
    '''....'''

    #random.seed(123) #to force every individual have the same color
                     #on each movement
                     
    # Checking if there is a dir moves
    cur_dir = os.getcwd()
    moves_dir = cur_dir+'/moves'
    if not os.path.exists(moves_dir):
        os.makedirs(moves_dir)
    else:
        # precisa limpar as imagens que tem la??
        pass
                     
    landscape_matrix_temp=[]
    for row in range(len(landscape_matrix)):
        landscape_matrix_temp.append(landscape_matrix[row])

    for num_of_indiv in range(len(indiv_xy)):
        if aux_islive[num_of_indiv]==0:
            numbpix=indivpixels_isNOTlive
        elif aux_isdispersing[num_of_indiv]==1:
            numbpix=indivpixels_isdispersing
        else:
            numbpix=indivpixels_whenmoving
            
        for pixelsX in range(-(int(numbpix/2)),(int(numbpix/2)+1)):
            for pixelsY in range(-(int(numbpix/2)),(int(numbpix/2)+1)):
                xp=int(indiv_xy[num_of_indiv][0]+pixelsX)
                yp=int(indiv_xy[num_of_indiv][1]+pixelsY)
                if xp>(len(landscape_matrix)-1):
                    xp=(len(landscape_matrix)-1)
                if xp<0:
                    xp=0
                if yp>(len(landscape_matrix[0])-1):
                    yp=(len(landscape_matrix[0])-1)
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

    pal = color_pallete(userbase = UserBaseMap)

    im.putpalette(pal)

    #im.save(Form1.background_filename[0])
    
    if nlandscape<9:
        myzerosl="000"
    elif nlandscape<99:
        myzerosl="00"
    elif nlandscape<999:        
        myzerosl="0"
    else:
        myzerosl=""
    
    if nruns<9:
        myzeros="000"
    elif nruns<99:
        myzeros="00"
    elif nruns<999:        
        myzeros="0"
    else:
        myzeros=""
        
    saverun=output_prefix+"_map_"+myzerosl+str(nlandscape+1)+"_run_"+myzeros+str(nruns+1)+".png"
    #im.save(saverun)

    if timestep<9:
        myzerosTS="000"
    elif timestep<99:
        myzerosTS="00"
    elif timestep<999:        
        myzerosTS="0"
    else:
        myzerosTS=""
    saverunTS="moves/"+output_prefix+"_map_"+myzerosl+str(nlandscape+1)+"_run_"+myzeros+str(nruns+1)+"_TS_"+myzerosTS+str(timestep+1)+".png"
    im2=im.copy()
    im2.save(saverunTS)
       
    #random.seed()  #to release the random.seed()
