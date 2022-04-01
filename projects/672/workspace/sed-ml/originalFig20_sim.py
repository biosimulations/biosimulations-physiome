# To reproduce the data needed for Figure 20 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run originalFig20_sim.py

import opencor as oc
import get_init
import imp
imp.reload(get_init)

# The prefix of the saved output file name 
prefilename = 'simFig20'
# Load the simulation file
simfile='periodic-stimulus.sedml'
simulation = oc.open_simulation(simfile)

# The data object houses all the relevant information
# and pointers to the OpenCOR internal data representations
data = simulation.data()

# Define the interval of interest for this simulation experiment
start, end, pointInterval = 0, 20.01, 0.001
data.set_starting_point(start)
data.set_ending_point(end)
data.set_point_interval(pointInterval)

# Compute initial value based on T and V_b
T, V_b = 6, 0
m, n, h = get_init.init_gate(T, V_b)

iV_initial = -15
V_stim = -90
t_stim = [20, 4.7284, 5.7302, 7.7352]
suffixfile=['A', 'B', 'C', 'D',]

for i, iend in enumerate(t_stim):
   filename ='%s_%s.csv' % (prefilename, suffixfile[i])
   # Reset states and parameters
   simulation.reset(True)
   # Set constant parameter values
   data.states()['outputs/V'] = iV_initial
   data.constants()['parameters/T'] = T
   data.states()['outputs/m'] = m
   data.states()['outputs/n'] = n
   data.states()['outputs/h'] = h
   # Run simulation from 0 to iend
   data.set_starting_point(start)
   data.set_ending_point(iend)
   simulation.run()
   if i>0:       
       # Stimulate at iend and run till end
       data.states()['outputs/V'] = V_stim
       data.set_starting_point(iend)
       data.set_ending_point(end)
       simulation.run()
   # Access simulation results
   results = simulation.results()
   # Access the full datastore representation of the simulation results
   ds = results.data_store()
   voi_and_variables = ds.voi_and_variables()  
   # Save the simulation result
   outfile = open(filename, 'w')
   cols = []
   for key, item in voi_and_variables.items():
       outfile.write(str(key) + ",")
       cols.append(list(item.values()))
   
   outfile.write("\n")
   
   for i in range(0, len(cols[0])):
       for j in range(0, len(cols)):
           outfile.write(str(cols[j][i]) + ",")
       outfile.write("\n")

   outfile.close()
   # clear the results
   simulation.clear_results()




