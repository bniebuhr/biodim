
def identify_habarea(indiv_xy_position, habarea_map):
    """
    This function identifies the habitat area of a patch in which an individual is.
    Input:
    - indiv_xy_position: cell that corresponde to (row,col) positions of an individual
    - habarea_map: matrix/map of Area of each patch
    Output:
    - patchid: Area of the fragment (in ha)
    """  
    
    row=int(indiv_xy_position[0])
    col=int(indiv_xy_position[1])
    habarea=habarea_map[row][col]
    
    return habarea
