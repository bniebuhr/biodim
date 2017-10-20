import grass.script as grass
from export_raster_from_grass import set_region

def map_info(landscape, usegrid = False, x_center = '', y_center = '', dims = ''):
    '''
    This function extracts information (extent, resolutin/grain, number of rows and columns) from the landscape,
    directly from the GRASS GIS DataBase
    Input:
    - landscape: name of the landscape (it may the HABMAT landscape - binary)
    
    Output:
    - dim: (nrows, ncols) - number of rows and columns of the landscape
    - x_west: western limit of the map
    - x_east: eastern limit of the map
    - y_south: southern limit of the map
    - y_north: northern limit of the map
    - res_x: resolution/grain (size of the pixel), in the west-east direction
    - res_y: resolution/grain (size of the pixel), in the south-north direction
    '''
    
    #landscape='lndscp_0002_Mapa0002_tif_HABMAT_HABMAT'
    #if usegrid:
        #set_region(x_col=x_center, y_row=y_center, dims=dims)
    #else:
        #grass.run_command('g.region', raster=landscape)
    info = grass.parse_command('r.info', map=landscape, flags='g')
        
    # aqui deveriamos checar se a resolucao eh inteira... como fazer isso?
    res_x = int(info['ewres'])
    res_y = int(info['nsres'])    
    if usegrid:
        dim = [dims[0]/res_y, dims[1]/res_x] # dims (y,x): in y/rows (meters), in x/cols (meters) 
        x_west = x_center-(dims[1]/2)
        x_east = x_center+(dims[1]/2)
        y_south = y_center-(dims[0]/2)
        y_north = y_center+(dims[0]/2)        
    else:
        dim = [int(info['rows']), int(info['cols'])]
        x_west = int(float(info['west']))
        x_east = int(float(info['east']))
        y_south = int(float(info['south']))
        y_north = int(float(info['north']))
    
    #print 'dims = %d, %d; limits W-E: %d - %d, S-N: %d - %d; res = %d, %d' % (dim[0], dim[1], x_west, x_east, y_south, y_north, res_x, res_y)
    
    return dim, x_west, x_east, y_south, y_north, res_x, res_y
    
#landscape_name = 'simulation_000001_p029_h059_HABMAT'
#dim, x_west, x_east, y_south, y_north, res_x, res_y = map_info(landscape=landscape_name)
#print 'dims = %d, %d; limits W-E: %d - %d, S-N: %d - %d; res = %d, %d' % (dim[0], dim[1], x_west, x_east, y_south, y_north, res_x, res_y)