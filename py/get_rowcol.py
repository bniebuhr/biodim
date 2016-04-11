
def get_rowcol(xy, spatialresolution, x_west, y_north):
    
    rowcol = []
    for indiv in range(len(xy)):
        col = int((xy[indiv][0] - x_west)/spatialresolution) # x = col
        row = int((y_north - xy[indiv][1])/spatialresolution) # y = row
        rowcol.append([row, col])
        
    return rowcol
    
    