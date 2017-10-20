
def read_table(file_in):
    """
    This function reads a plain text table, excludes headers and transform it into a 2-D list (matrix)
    Input:
    - file_in: file containing a plain text table (e.g., txt/csv), with spaces separating words/values
    Output:
    - matrix: 2-D list with table values
    """
    
    input_file = open(file_in, 'r')
    lines = input_file.readlines()
    lines = lines[1:] # excluding header
    input_file.close()
    
    matrix = []
    for line in lines:
        matrix.append(map(float, line.strip().split(" ")))
    return matrix
