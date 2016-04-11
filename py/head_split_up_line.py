
def head_split_up_line(line):
    '''
    Auxiliary function for opening the header of ascii maps and understanding its lines;
    used by function read_landscape_head_ascii_standard se separate elements in the same line.
    Input:
    - line: line read from a document - an ascii map
    Output:
    - clean line: dictionary with the two elements (the first and the last) of the line, 
      which are separated by a space in blanck
    '''
    
    line = line.split(' ')
    clean_line={}
    clean_line[line[0]]=line[len(line)-1]
    
    return clean_line