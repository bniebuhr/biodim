# Testing random function for BioDIM

# Time

from timeit import timeit

def f():
    l = 200
    b = 100
    h = 30    
    grid = [[[-1 for x in range(l)] for y in range(b)] for z in range(h)]
    return grid
    
timeit(f, number = 100)

#----------------------------------------

# test times to read map names from file or from grass db
# much better to read it from file! ~ 1000 times faster

from timeit import timeit
import os
import grass.script as grass

def fun_read_table():
    
    select_form = 'random'
    previous_landscape = ''
    
    os.chdir(r'/home/leecb/Github/biodim/input')
    file_habmat = open("simulados_HABMAT.txt","r")
    habmat = file_habmat.readlines()
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


lista = grass.list_grouped('rast', pattern = '*HABMAT*') ['MS_HABMAT']

def fun_read_GRASS():
    
    select_form = 'random'
    previous_landscape = ''
    
    habmat = lista
    
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
    
    return landscape_grassname_habmat, landscape_index

timeit(fun_read_table, number = 100)

timeit(fun_read_GRASS, number = 100)

# but not if we put grass.list_grouped to outside, to be read only once

#-----------------------------------------------------

# Test load maps to python memory

import grass.script.array as garray
from read_landscape_head_ascii_standard import read_landscape_head_ascii_standard
import grass.script as grass
import time
import os

ts1 = time.time()

for i in range(10):
    #mapp = 'simulation_000017_p067_h049_HABMAT'
    mapp = 'lndscp_0001_floresta_1985_bin_HABMAT'
    a = garray.array() 
    a.read(mapp)

tf1 = time.time()   

# vs pickup one landscape

os.chdir('/home/leecb/Github/biodim/temp')

ts2 = time.time()

for i in range(10):
    grass.run_command('r.out.ascii', input=map, output='random_landscape_habmat.asc', overwrite = True)
    landscape_head, landscape_matrix=read_landscape_head_ascii_standard('random_landscape_habmat.asc',"int")

tf2 = time.time()

print 'delta t1 = '+str(tf1-ts1)

# o primeiro eh bem mais rapido!!!!