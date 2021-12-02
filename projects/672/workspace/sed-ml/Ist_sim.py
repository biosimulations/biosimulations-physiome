# To produce the data needed for Figures in associated Physiome paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Ist_sim.py

import opencor as oc
import get_init
import imp
imp.reload(get_init)

# The prefix of the saved output file name 
prefilename = 'Ist'
# Load the simulation file
simfile='periodic-stimulus.sedml'
simulation = oc.open_simulation(simfile)

# The data object houses all the relevant information
# and pointers to the OpenCOR internal data representations
data = simulation.data()

# Define the interval of interest for this simulation experiment
start, end, pointInterval = 0, 60, 0.001
data.set_starting_point(start)
data.set_ending_point(end)
data.set_point_interval(pointInterval)

# Compute initial value based on T and V_b
T, V_b = 6.3, 0
m, n, h = get_init.init_gate(T, V_b)

V_initial = [0]

Periods=[20, 20, 10, 10]
Ists=[-10, 20, -10, -50]

for i, iPeriod in enumerate(Periods):
   filename ='%s_%dms%dmV.csv' % (prefilename,iPeriod,Ists[i])
   # Reset states and parameters
   simulation.reset(True)
   # Set constant parameter values
   data.states()['outputs/V'] = V_initial[0]
   data.constants()['parameters/T'] = T
   data.states()['outputs/m'] = m
   data.states()['outputs/n'] = n
   data.states()['outputs/h'] = h
   data.constants()['stimulus_protocol_params/stimPeriod'] = iPeriod
   data.constants()['stimulus_protocol_params/stimCurrent'] = Ists[i]
   data.constants()['stimulus_protocol_params/stimDuration'] = 1
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




