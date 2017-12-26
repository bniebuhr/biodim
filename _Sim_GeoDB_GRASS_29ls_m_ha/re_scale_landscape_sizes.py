#########################################################
##
## Organizing map units of the BioDIM DataBase
##
#########################################################

import grass.script as grass
import os

############
# Setting landscape extension and resolution - maps with 512x512 pixels, resolution 30m, limits S-N: 0-15360, O-L:0-15360

# list mapsets
mapsets = grass.read_command('g.mapset', flags='l')
mapsets = mapsets.replace('\n', '')

# separating mapsets and transforming it into a list
mapsets2 = mapsets.split(' ')
mapsets2 = [i for i in mapsets2 if len(i) > 0]
mapsets2

print len(mapsets2)

# Parameters
res=30
hectare=10000

for ms in mapsets2:
    
    print ms
    grass.run_command('g.mapset', mapset=ms)
    maps = grass.list_grouped ('rast', pattern='*') [ms]
    
    for mm in maps:
        
        print mm
        grass.run_command('r.region', map=mm, n=512*res, s=0, w=0, e=512*res)
        
############
# Setting area units in hectares

# we want to lead with these mapsets (those in which pixels represent area):
mapsets=["MS_HABMAT_AREA", "MS_HABMAT_DILA01_AREA", "MS_HABMAT_DILA01_AREAqual", "MS_HABMAT_DILA01_AREAqualONE", "MS_HABMAT_DILA02_AREA", "MS_HABMAT_DILA02_AREAqual", "MS_HABMAT_DILA02_AREAqualONE", "MS_HABMAT_FRAG_AREA", "MS_HABMAT_FRAG_AREAqual", "MS_HIQOTH_AREA", "MS_HQMQLQ_AREAqual", "MS_MEQOTH_AREA"]

patt=['AREApix', 'AREApix', 'AREAqual', 'AREAqualONE', 'AREApix', 'AREAqual', 'AREAqualONE', 'AREApix', 'AREAqual', 'AREApix', 'AREAqual', 'AREApix']
newpatt=['AreaHA', 'AreaHA', 'AREAqualHA', 'AREAqualONEHA', 'AreaHA', 'AREAqualHA', 'AREAqualONEHA', 'AreaHA', 'AREAqualHA', 'AreaHA', 'AREAqualHA', 'AreaHA']

files = ["simulados_HABMAT_grassclump_AREApix.txt", "simulados_HABMAT_grassclump_dila01_clean_AREApix.txt", "no", "no", "simulados_HABMAT_grassclump_dila02_clean_AREApix.txt", "no", "no", "simulados_HABMAT_FRAC_AREApix.txt", "no", "no", "simulados_HQMQLQ_AREAqual.txt", "no"]    

len(patt)

folder = r'/home/leecb/Documentos/UNESP/biodim/DB_random_landscapes_10000/landscapes_res1m/unzipped_location2'
os.chdir(folder)

for i in range(len(patt)):
    
    print mapsets[i]
    print patt[i]
    
    grass.run_command('g.mapset', mapset=mapsets[i])
    maps = grass.list_grouped ('rast', pattern='*'+patt[i]) [mapsets[i]]
    
    list_names = []
    for mm in maps:
        
        print mm
        newname = mm.replace(patt[i], newpatt[i])
        list_names.append(newname)
        expression = newname + ' = int( float(' + mm + ') * ' + repr(res) + ' * ' + repr(res) + ' / ' + repr(hectare) + ')'
        print expression
        grass.run_command('g.region', rast=mm)
        grass.mapcalc(expression, overwrite = True, quiet = True)
        
    if files[i] != "no":
        newfile = files[i]#.replace(patt[i], newpatt[i])
        print newfile
        
        txt = open(newfile, 'w')
        for name in list_names:
            txt.write(name+'\n')
            print name
        txt.close()

    #raw_input("Proximo mapset!\n")

############
## Setting distance units in meters

res=30

# we want to lead with these mapsets (those in which):
mapsets="MS_HABMAT_DIST"

files = "simulados_HABMAT_DIST.txt"

grass.run_command('g.mapset', mapset=mapsets)
maps = grass.list_grouped ('rast', pattern='*') [mapsets]

list_names = []
for mm in maps:
    
    # Copy to aux
    print mm
    expression = mm + '.aux = ' + mm
    print expression
    grass.run_command('g.region', rast=mm)
    grass.mapcalc(expression, overwrite = True, quiet = True)    
    
    # remove original
    grass.run_command('g.remove', type='raster', name=mm, flags='f')
    
    # calculate new in meters
    expression2 = mm + ' = ' + mm + '.aux * ' + repr(res)
    print expression2
    grass.mapcalc(expression2, overwrite = True, quiet = True)


############
## Removing old maps (areas in pixels, distance in pixels)

mapsets=["MS_HABMAT_AREA", "MS_HABMAT_DILA01_AREA", "MS_HABMAT_DILA01_AREAqual", "MS_HABMAT_DILA01_AREAqualONE", "MS_HABMAT_DILA02_AREA", "MS_HABMAT_DILA02_AREAqual", "MS_HABMAT_DILA02_AREAqualONE", "MS_HABMAT_FRAG_AREA", "MS_HABMAT_FRAG_AREAqual", "MS_HIQOTH_AREA", "MS_HQMQLQ_AREAqual", "MS_MEQOTH_AREA", "MS_HABMAT_DIST"]

patt=['AREApix', 'AREApix', 'AREAqual', 'AREAqualONE', 'AREApix', 'AREAqual', 'AREAqualONE', 'AREApix', 'AREAqual', 'AREApix', 'AREAqual', 'AREApix', ".aux"]

for i in range(len(patt)):
    
    print mapsets[i]
    print patt[i]
    
    grass.run_command('g.mapset', mapset=mapsets[i])
    maps = grass.list_grouped ('rast', pattern='*'+patt[i]) [mapsets[i]]
    
    for mm in maps:
        
        print mm
        grass.run_command('g.remove', type='raster', name=mm, flags='f')
        
        
        

