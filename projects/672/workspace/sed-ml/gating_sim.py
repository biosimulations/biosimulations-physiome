# To reproduce the data needed for Figure 11 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run gating_sim.py

import opencor as oc
import get_init
import imp
imp.reload(get_init)

# The prefix of the saved output file name 
prefilename = 'gating'
# Load the simulation file
simfile='gating_experiment.sedml'
simulation = oc.open_simulation(simfile)

# The data object houses all the relevant information
# and pointers to the OpenCOR internal data representations
data = simulation.data()

# Define the interval of interest for this simulation experiment
start, end, pointInterval = 0, 170, 0.1
data.set_starting_point(start)
data.set_ending_point(end)
data.set_point_interval(pointInterval)

filename ='%s.csv' % (prefilename)
# Reset states and parameters
simulation.reset(True)
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



