import grass.script as grass

def map_info(landscape):
    
    info = grass.parse_command('r.info', map=landscape, flags='g')
    
    # aqui deveriamos checar se a resolucao eh inteira... como fazer isso?
    dim = [int(info['rows']), int(info['cols'])]
    x_west = int(info['west'])
    x_east = int(info['east'])
    y_south = int(info['south'])
    y_north = int(info['north'])
    res_x = int(info['ewres'])
    res_y = int(info['nsres'])
    
    print 'dims = %d, %d; limits W-E: %d - %d, S-N: %d - %d; res = %d, %d' % (dim[0], dim[1], x_west, x_east, y_south, y_north, res_x, res_y)
    
    return dim, x_west, x_east, y_south, y_north, res_x, res_y
    
map_info()