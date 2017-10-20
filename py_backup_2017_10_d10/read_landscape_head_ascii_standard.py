from head_split_up_line import head_split_up_line

def read_landscape_head_ascii_standard(input_land, matrixmode):
    '''
    This function read the header and the matrix of an ascii map, and returns both the
    header, with map limits and number of rows/cols, and a matrix corresponding to the map
    Input:
    - input_land: GRASS GIS raster map
    - matrixmode: type of map - int, float, or long
    Output:
    - head: header of the ascii map, with map limits (north, south, east, west) and number of rows/cols
    - matrix: input map in a form of matrix (2 dimension list)
    '''
    
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