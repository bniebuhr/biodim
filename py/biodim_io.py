
# Import modules
import os
import numpy as np
from ast import literal_eval
from collections import OrderedDict

def read_write_input_parms(folder_name, file_name, rw = 'r', parms = None):
    
    if rw == 'r':
        #os.chdir(folder_name)
        #with open('teste.txt', 'r') as f:
            #fil = f.read()
            ##lines = f.readlines()  
        #lines
        
        # Lines of the input file
        lines = np.genfromtxt(folder_name+'/'+file_name, comments="#", delimiter="=", autostrip=True, dtype = (str, None))

        parms = OrderedDict()
        for i in lines:
            try:
                if i[1] == 'None':
                    parms[i[0]] = None
                else:
                    parms[i[0]] = literal_eval(i[1])
            except:
                parms[i[0]] = str(i[1])
                
        
        return parms
        
    elif rw == 'w' and parms is not None:
        with open(folder_name+'/'+file_name, 'w') as f:
            f.write('# BioDIM setup file\n\n')
            for key,value in parms.items():
                f.write('%s=%s\n' % (key,str(value)))
