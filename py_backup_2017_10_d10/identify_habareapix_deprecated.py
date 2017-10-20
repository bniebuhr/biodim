
def identify_habarea(indiv_xy_position, habareapix_map, userbase = False):
    """
    This function identifies the habitat area of a patch in which an individual is.
    If userbase = False (simulation on the DataBase maps), the area is in number of pixels;
    if userbase = True (simulation on the user (real) maps), the area is in number of hectares.
    Input:
    - indiv_xy_position: cell that corresponde to [x,y](row,col) positions of an individual
    - habareapix_map: matrix/map of Area of each patch 
      (if userbase = False, AREAPix in pixels; if userbase = True, AreaHA in hectares)
    Output:
    - patchid: Area of the fragment
      (if userbase = False, in pixels; if userbase = True, in hectares)
    """  
    
    row=int(indiv_xy_position[0])
    col=int(indiv_xy_position[1])
    habareapix=habareapix_map[row][col]
    return habareapix
