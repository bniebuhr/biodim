
def getForest(landscape_matrix):
    '''
    This function returns the percentage of habitat/forest in the landscape and which cells (row,col)
    of the map correspond to habitat/forest.
    Input:
    - landscape_matrix: table/map of habitat, considering 1 = forest (HQ=high quality),
      2 = forest (MQ = medium quality), and 3 = matrix (LQ = low quality)
    Ouput:
    - pland: percentage of habitat/forest in the landscape
    - forest: sequence of cells (row, column) that correspond to habitat/forest
    '''
    
    forest = []
    cont = 0.0
    for row in range(len(landscape_matrix)):
        for col in range(len(landscape_matrix[0])):
            feature = landscape_matrix[row][col]
            if feature == 1: #HQ
                forest.append([row,col])
                cont += 1.0
            if feature == 2: #MQ
                forest.append([row,col])
                cont += 1.0
                
    pland = int(100*cont/float(len(landscape_matrix)*len(landscape_matrix[0])))
    
    return pland, forest

def getForest_habmat(landscape_matrix):
    '''
    This function returns the percentage of habitat/forest in the landscape and which cells (row,col)
    of the map correspond to habitat/forest. This function is equal to getForest, but designed to 
    user (real) maps that do not have quality on it. It is based on a binary map of habitat (1) 
    matrix (0) only.
    Input:
    - landscape_matrix: table/map of habitat, considering 1 = forest and 0 = matrix.
    Ouput:
    - pland: percentage of habitat/forest in the landscape
    - forest: sequence of cells (row, column) that correspond to habitat/forest
    '''    

    forest = []
    cont = 0.0
    for row in range(len(landscape_matrix)):
        for col in range(len(landscape_matrix[0])):
            feature = landscape_matrix[row][col]
            if feature == 1: 
                forest.append([row,col])
                cont += 1
                
    pland = int(100*cont/float(len(landscape_matrix)*len(landscape_matrix[0])))
    
    return pland, forest
