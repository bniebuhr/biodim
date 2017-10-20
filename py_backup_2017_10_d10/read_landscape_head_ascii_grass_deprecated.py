
def read_landscape_head_ascii_grass(input_land):
    input_file = open(input_land, 'r')
    line = input_file.readline()
    nlines = 0
    head = {}
    while nlines<5:
        line=input_file.readline()
        clean_line = head_split_up_line.head_split_up_line(line)
        head.update(clean_line)
        nlines += 1
    input_file.close()
    
    input_file = open(input_land, 'r')
    lines = input_file.readlines()
    lines = lines[6:]
    input_file.close()

    matrix = []
    for line in lines:
        matrix.append(map(float, line.strip().split(" ")))
    return head, matrix
