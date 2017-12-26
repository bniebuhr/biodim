
# Import modules
import datetime
from dateutil.rrule import rrulestr
from dateutil.parser import parse

# Import functions
from biodim_io import read_write_input_parms

# Class biodim_simulation
class biodim_simulation():
    
    def __init__(self, load_file = '', load_dir = '', save_setup_file = '',
                 time_step = 1, time_unit = 'monthly', n_steps = 200, start_datetime = '19900101T060000'):
        # Setup simulations
        
        self.setup = {}
        
        # If there is no file with simulation settings to be load, load it from the parameters
        if load_file == '' or load_dir == '':
            
            # Time resolution and extension
            self.setup['time_step'] = time_step # Time step - distance between steps
            self.setup['time_unit'] = time_unit # Unit of the the time
            self.setup['n_steps'] = n_steps # Number of steps for a simulation
            
            # Save file with parameters
            # File name
            if save_setup_file == '':
                name_setup_file = 'biodim_setup_'+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+'.txt'
            else:
                name_setup_file = save_setup_file
            # Write
            read_write_input_parms(folder_name = '.', file_name = name_setup_file, rw = 'w', parms = self.setup)                        
            
        # Instead, if a file is given as argument, read parameters from inside it
        else:
            
            self.setup = read_write_input_parms(folder_name = load_dir, file_name = load_file, rw = 'r')        
            
        # Possible time units
        possible_time_units = ['secondly', 'minutely', 'hourly', 'dayly', 'weekly', 'monthly', 'yearly']
            
        # Check if time_unit is one of the possible values
        if time_unit in possible_time_units:
            # If True, the steps are defined as a list of dates, accoriding to the parameters
            self.steps = list(rrulestr('FREQ='+time_unit+';INTERVAL='+str(time_step)+';COUNT='+str(n_steps),
                                       dtstart = parse(start_datetime)))
        else:
            raise ValueError('The time unit is '+time_unit+'; but it must be one of the following options: '+', '.join(possible_time_units)+'. Please retry.')
            

    def load_landscape():
        pass
    
    def step():
        pass
        
    def simulation():
        # for i in n_steps, step
        pass
        


