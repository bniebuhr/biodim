import os
import numpy as np
import math
os.chdir(r'C:\B\A')
tabela_resultado=np.genfromtxt('teste_indiv.txt',names=True, delimiter=';', dtype=None)
teste=open('Rplot.txt','w')


teste.write("#####################################################################################\n")
teste.write("##                                 SYNTHESIS                                       ##\n")
teste.write("#####################################################################################\n")

teste.write("-------------------------------------------------------------------------------------\n")
teste.write("\nexperiment_info :\n")
x=0
experiment_info=list(tabela_resultado["experiment_info"])
lista_apio_experiment_info=[]
for i in experiment_info:
    temp=i
    if len(lista_apio_experiment_info)==0:
        lista_apio_experiment_info.append(i)
        teste.write('  '+i+'\n')
    else:
        temp2=lista_apio_experiment_info[x]
        if temp != temp2 and temp !='experiment_info' :
            lista_apio_experiment_info.append(i)
            #print i
            teste.write('  '+i+'\n')
            x=x+1 


teste.write("\n--------------------------------------------------------------------------------------\n")
teste.write("\nActualrun:\n")
#actualrun    
      
actualrun=list(tabela_resultado["actualrun"])
lista_apio_actualrun=[]
x=0
for i in actualrun:
    temp=i
    if len(lista_apio_actualrun)==0:
        lista_apio_actualrun.append(temp)
        teste.write('     '+i)
    else:
        temp2=lista_apio_actualrun[x]
        if temp!=temp2 and temp!='actualrun':
            lista_apio_actualrun.append(i)
            #print i
            teste.write(' , '+i)
            x=x+1 
    

teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nGrassname Habmat:\n")
lista_apio_grassname_habmat=[]
grassname_habmat=list(tabela_resultado["grassname_habmat"])
x=0
for i in grassname_habmat:
    temp=i
    if len(lista_apio_grassname_habmat)==0:
        lista_apio_grassname_habmat.append(temp)
        teste.write('  '+i+'\n')
    else:
        temp2=lista_apio_grassname_habmat[x]
        if temp!=temp2 and temp!='grassname_habmat':
            lista_apio_grassname_habmat.append(i)
            #print i
            teste.write('  '+i+'\n')
            x=x+1



teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nPLAND:\n")
lista_apio_PLAND=[]
PLAND=list(tabela_resultado["PLAND"])
x=0
for i in PLAND:
    temp=i
    if len(lista_apio_PLAND)==0:
        lista_apio_PLAND.append(temp) 
        teste.write('  '+i)
    else:
        temp2=lista_apio_PLAND[x]
        if temp!=temp2 and temp!='PLAND':
            lista_apio_PLAND.append(i)
            #print i
            teste.write(' , '+i)
            x=x+1        



teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nCONFIG\n")
lista_apio_CONFIG=[]
CONFIG=list(tabela_resultado["CONFIG"])
x=0
for i in CONFIG:
    temp=i
    if len(lista_apio_CONFIG)==0:
        lista_apio_CONFIG.append(temp) 
        teste.write('  '+i)
    else:
        temp2=lista_apio_CONFIG[x]
        if temp!=temp2 and temp!='CONFIG':
            lista_apio_CONFIG.append(i)
            #print i
            teste.write(' , '+i)
            x=x+1    


teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nHABQUAL:\n")
lista_apio_HABQUAL=[]
HABQUAL=list(tabela_resultado["HABQUAL"])
x=0
for i in HABQUAL:
    temp=i
    if len(lista_apio_HABQUAL)==0:
        lista_apio_HABQUAL.append(temp) 
        teste.write('  '+i)
    else:
        temp2=lista_apio_HABQUAL[x]
        if temp!=temp2 and temp!='HABQUAL':
            lista_apio_HABQUAL.append(i)
            #print i
            teste.write(' , '+i)
            x=x+1


teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nSpecies Profile:\n")
lista_apio_species_profile=[]
species_profile=list(tabela_resultado["species_profile"])
x=0
for i in species_profile:
    temp=i
    if len(lista_apio_species_profile)==0:
        lista_apio_species_profile.append(temp) 
        teste.write('  '+i+'\n')
    else:
        temp2=lista_apio_species_profile[x]
        if temp!=temp2 and temp!='species_profile':
            lista_apio_species_profile.append(i)
            #print i
            teste.write('  '+i+'\n')
            x=x+1




teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nInclude Quality:\n")
lista_apio_include_quality=[]
include_quality=list(tabela_resultado["include_quality"])
x=0
for i in include_quality:
    temp=i
    if len(lista_apio_include_quality)==0:
        lista_apio_include_quality.append(temp) 
        teste.write('  '+i+'\n')
    else:
        temp2=lista_apio_include_quality[x]
        if temp!=temp2 and temp!='include_quality':
            lista_apio_include_quality.append(i)
            #print i
            teste.write('  '+i+'\n')
            x=x+1
            
            
            
teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nStart Popsize:\n")
lista_apio_start_popsize=[]
start_popsize=list(tabela_resultado["start_popsize"])
x=0
for i in start_popsize:
    temp=i
    if len(lista_apio_start_popsize)==0:
        lista_apio_start_popsize.append(temp) 
        teste.write('  '+i)
    else:
        temp2=lista_apio_start_popsize[x]
        if temp!=temp2 and temp!='start_popsize':
            lista_apio_start_popsize.append(i)
            #print i
            teste.write(' , '+i)
            x=x+1




teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nTimesteps:\n")
lista_apio_timesteps=[]
timesteps=list(tabela_resultado["timesteps"])
x=0
for i in timesteps:
    temp=i
    if len(lista_apio_timesteps)==0:
        lista_apio_timesteps.append(temp) 
        teste.write('  '+i)
    else:
        temp2=lista_apio_timesteps[x]
        if temp!=temp2 and temp!='timesteps':
            lista_apio_timesteps.append(i)
            #print i
            teste.write(' , '+i)
            x=x+1


teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nTotal of individuals:\n")
lista_apio_indiv=[]
indiv=list(tabela_resultado["indiv"])
i=indiv[-1]
teste.write('  '+i)




teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nHome Range Size:\n")
lista_apio_homerangesize=[]

homerangesize=list(tabela_resultado["homerangesize"])
x=0
for i in homerangesize:
    temp=i
    if len(lista_apio_homerangesize)==0:
        lista_apio_homerangesize.append(temp) 
        teste.write('  '+i)
    else:
        temp2=lista_apio_homerangesize[x]
        if temp!=temp2 and temp!='homerangesize':
            lista_apio_homerangesize.append(i)
            print i
            teste.write(' , '+i)
            x=x+1





teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nmovdistpix:\n")
lista_apio_movdistpix=[]

movdistpix=list(tabela_resultado["movdistpix"])
x=0
for i in movdistpix:
    temp=i
    if len(lista_apio_movdistpix)==0:
        lista_apio_movdistpix.append(temp) 
        teste.write('  '+i)
    else:
        temp2=lista_apio_movdistpix[x]
        if temp!=temp2 and temp!='movdistpix':
            lista_apio_movdistpix.append(i)
            print i
            teste.write(' , '+i)
            x=x+1



teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nDispfactor:\n")
lista_apio_dispfactor=[]
dispfactor=list(tabela_resultado["dispfactor"])
x=0
for i in dispfactor:
    temp=i
    if len(lista_apio_dispfactor)==0:
        lista_apio_dispfactor.append(temp) 
        teste.write('  '+i)
    else:
        temp2=lista_apio_dispfactor[x]
        if temp!=temp2 and temp!='dispfactor':
            lista_apio_dispfactor.append(i)
            print i
            teste.write(' , '+i)
            x=x+1

teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nIsdispersing:\n")
isdispersing=list(tabela_resultado["isdispersing"])
isdispersing_0=0
isdispersing_1=0

for i in isdispersing:
    if i =="0":
        isdispersing_0=isdispersing_0+1
    if i=='1':
        isdispersing_1=isdispersing_1+1
teste.write('   Dispersal Individuos: '+`isdispersing_0`+'\n')       
teste.write('   Not dispesal Individuos: '+`isdispersing_1`)         
    

teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nIsfemale:\n")
isfemale=list(tabela_resultado["isfemale"])
female_0=0
female_1=0

for i in isfemale:
    if i =="0":
        female_0=female_0+1
    if i=='1':
        female_1=female_1+1


teste.write('   Individuals female: '+`female_1`+'\n')       
teste.write('   Individuals male: '+`female_0`)


teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nis Alive:\n")
islive=list(tabela_resultado["islive"])
islive_0=0
islive_1=0

for i in islive:
    if i =="0":
        islive_0=female_0+1
    if i=='1':
        islive_1=female_1+1


teste.write('   Individuals A live: '+`islive_1`+'\n')       
teste.write('   Individuals Dead: '+`islive_0`)


teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nTotal distance:\n")
totaldistance=list(tabela_resultado["totaldistance"])

dist_min=999999999999999999
dist_max=0
dist_mean=0
acumulator_dist=0
cont_dist=0
for i in totaldistance:
    if i!="totaldistance":
        temp=float(i)
        acumulator_dist=acumulator_dist+temp
        cont_dist=cont_dist+1
    if temp > dist_max:
        dist_max=round(temp,3)
    if temp<dist_min:
        dist_min=round(temp,3)
if cont_dist>0: 
    dist_mean=round(acumulator_dist/cont_dist,3)
    teste.write('   Distance Min:  '+`dist_min`+'\n')       
    teste.write('   Distance Max:  '+`dist_max`+'\n')
    teste.write('   Distance Mean: '+`dist_mean`)



teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nEffectivedistance:\n")
effectivedistance=list(tabela_resultado["effectivedistance"])
acumulator_eftcdistance=0.0
cont_maean_distance=0
eftcdistance_min=999999999999999999999999
eftcdistance_max=0

for i in effectivedistance:
    if i !=  "effectivedistance":
        temp=float(i)
        acumulator_eftcdistance=acumulator_eftcdistance+temp
        cont_maean_distance=cont_maean_distance+1
    if temp>eftcdistance_max:
        eftcdistance_max=round(temp,3)
    if temp<eftcdistance_min:
        eftcdistance_min=round(temp,3)
        
        

if cont_maean_distance>0:    
    mean_effectivedistance=round(acumulator_eftcdistance/cont_maean_distance,3)
    teste.write('   Effective distance Min:  '+`eftcdistance_min`+'\n')       
    teste.write('   Effective distance Max:  '+`eftcdistance_max`+'\n')
    teste.write('   Effective distance Mean: '+`mean_effectivedistance`)    





teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nActual Movement Cost:\n")
actual_movementcost=list(tabela_resultado["actual_movementcost"])
acumulator_actual_movementcost=0.0
cont_maean_actual_movementcost=0
actual_movementcost_min=999999999999999999999999
actual_movementcost_max=0
for i in actual_movementcost:
    if i !=  "actual_movementcost":
        temp=float(i)
        acumulator_actual_movementcost=acumulator_actual_movementcost+temp
        cont_maean_actual_movementcost=cont_maean_actual_movementcost+1
    if temp>actual_movementcost_max:
        actual_movementcost_max=round(temp,3)
    if temp<actual_movementcost_min:
        actual_movementcost_min=round(temp,3)
        
        

if cont_maean_distance>0:    
    mean_actual_movementcost=round(acumulator_actual_movementcost/cont_maean_actual_movementcost,3)
    teste.write('   Actual Movement Cost Min:  '+`actual_movementcost_min`+'\n')       
    teste.write('   Actual Movement Cost Max:  '+`actual_movementcost_max`+'\n')
    teste.write('   Actual Movement Cost Mean: '+`mean_actual_movementcost`) 




teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nTimestep waslive:\n")
lista_apio_timestep_waslive=[]

timestep_waslive=list(tabela_resultado["timestep_waslive"])
x=0
for i in timestep_waslive:
    temp=i
    if len(lista_apio_timestep_waslive)==0:
        lista_apio_timestep_waslive.append(temp) 
        teste.write('  '+i)
    else:
        temp2=lista_apio_timestep_waslive[x]
        if temp!=temp2 and temp!='timestep_waslive':
            lista_apio_timestep_waslive.append(i)
            print i
            teste.write(' , '+i)
            x=x+1



teste.write("\n\n--------------------------------------------------------------------------------------\n")
teste.write("\nNumber of Meetings:\n")
number_of_meetings=list(tabela_resultado["number_of_meetings"])
acumulator_number_of_meetings=0.0
cont_maean_number_of_meetings=0

for i in number_of_meetings:
    if i !=  "number_of_meetings":
        temp=float(i)
        acumulator_number_of_meetings=acumulator_number_of_meetings+temp
        cont_maean_number_of_meetings=cont_maean_number_of_meetings+1
        
teste.write('   Total meetings :  '+`cont_maean_number_of_meetings`+'\n')

teste.close()