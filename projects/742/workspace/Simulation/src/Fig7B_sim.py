# To reproduce the data needed for Figure 7B in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig7B_sim.py

import opencor as oc
import numpy as np

# Load the simulation file
simfile='../Vramp_experiment.sedml'
simulation = oc.open_simulation(simfile)
# The data object houses all the relevant information
# and pointers to the OpenCOR internal data representations
data = simulation.data()
# Set the experiments
K_Cahalf =[3, 11, 15]
duration = 160
Nai=2.9836
# Define the interval of interest for this simulation experiment
start, pointInterval = 0, 0.001
data.set_starting_point(start)
data.set_point_interval(pointInterval)
# Data to save
varName = np.array(["time", "rho_vCa", "V"])
vars = np.reshape(varName, (1, len(varName)))
# start to save when the test voltage returns to holding
rows=int((duration)/pointInterval+1)
r = np.zeros((rows,len(varName)))
# The prefix of the saved output file name 
prefilename = 'simFig7B'
inhPump=1
for j, iK_Cahalf in enumerate(K_Cahalf):
   data.set_ending_point(duration)
   # Reset states and parameters
   simulation.reset(True)
   # Set constant parameter values
   data.constants()['control_para/Nai'] = Nai
   data.constants()['control_para/inhPump'] = inhPump
   data.constants()['control_para/K_Cahalf'] = iK_Cahalf
   simulation.run()
   # Access simulation results
   results = simulation.results()
   # Grab a specific algebraic variable results 
   r[:,0] = results.voi().values()[-rows:]
   r[:,1] = results.algebraic()['outputs/rho_vCa'].values()[-rows:]
   r[:,2] = results.states()['outputs/V'].values()[-rows:]
   # clear the results except the last run
   simulation.clear_results() 
   # Save the simulation result of the last run
   filename='../simulatedData/%s_%d.csv' % (prefilename,j)
   np.savetxt(filename, vars, fmt='%s',delimiter=",")
   with open(filename, "ab") as f:
       np.savetxt(f, r, delimiter=",")
   f.close
    

