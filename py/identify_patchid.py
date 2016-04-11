def identify_patchid(indiv_xy_position, patchid_map):
    """
    ######## o que acontece se o bicho esta dispersando???  pid = 0 o mesmo para a area...
    
    This function identifies the ID of the patch in which the individual is.
    Input:
    - indiv_xy_position: cell that corresponde to [x,y](row,col) positions of an individual
    - patchid_map: matrix/map of Patch ID positions
    Output:
    - patchid: PID of the fragment
    """ 
    
    row=int(indiv_xy_position[0])
    col=int(indiv_xy_position[1])
    patchid=patchid_map[row][col]
    
    return patchid
