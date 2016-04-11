import random

def color_pallete(userbase = False):
    """
    This function define the pallete of colors of the map before exporting/plotting results
    or before showing maps in the GUI
    Input:
    - userbase: False = simulated database maps are used - maps with quality (1=HQ, 2=MQ, 3=LQ)
                True = user (real) maps are used - habitat/matrix maps (1=hab, 0=mat)
    Output:
    - pal: pallete of colors (a flatten list of RGB for each class)
    """    
    pal = [(0,0,0) for i in range(256)]  # all black
    
    random.seed(1)
    for i in range(1,255):
        color_R=random.sample(range(1,255),1)
        color_G=random.sample(range(1,255),1)
        color_B=random.sample(range(1,255),1)
        #pal[i]=((255-i),int(i/2),i)
        pal[i]=(color_R[0],color_G[0],color_B[0])
    
    pal=random.sample(pal, 255)

#    if Form1.background_filename[0]=="random_landscape_habmat.png":
#        pal[1] = (68,194,0)     # HABITAT
#        pal[2] = (255,190,190)  # MATRIZ
#    if Form1.background_filename[0]=="random_landscape_hqmqlq.png":
#    if 1==1:
#        pal[1] = (68,194,0)     # HABITAT
#        pal[2] = (255,235,190)  # MQ/MATRIZ
#        pal[3] = (255,190,190)  # MATRIZ
    if userbase:
        pal[1] = (60,170,0)     # HABITAT
        pal[0] = (255,255,190)  # MATRIZ
    else:
        pal[1] = (68,194,0)     # HABITAT
        pal[2] = (255,235,190)  # MQ/MATRIZ
        pal[3] = (255,190,190)  # MATRIZ

    pal = sum(pal, ())  # flatten it
    random.seed()
    return pal