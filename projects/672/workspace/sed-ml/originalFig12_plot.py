import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilename = 'simFig12'
# Figure name
prefig = 'Fig12'
figfile = 'original%s.png' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 12, 8
fig = plt.figure(figsize=(fw,fh))
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Set subplots
subpRow, subpCol = 1, 1
ax = fig.add_subplot(111)
lfontsize, labelfontsize = 12, 12 # legend, label fontsize
# For reading original data derived from the paper
fileindex=[90, 15, 7, 6]
# For read data from the simulation output files
V_initial = [-90, -15, -7, -6]
x_name = 'outputs/time'
y_name ='outputs/minus_V'
rol=int(6*100)
for i, iV_initial in enumerate(V_initial):
    filename ='%s_(%d)mV.csv' % (prefilename, iV_initial)      
    data = pd.read_csv(filename)
    x_data = data[x_name][0:rol]   
    y_data = data[y_name][0:rol]
    T_data = data['parameters/T']
    ax.plot(x_data, y_data, color=cycle[i], label = 'CellML @ %d mV' % (iV_initial ) )

    filename = 'fig12_%d.csv' % fileindex[i]
    odata = pd.read_csv(filename)
    ox_data = odata['x']   
    oy_data = odata['Curve1']
    ax.plot(ox_data, oy_data, '.',  color=cycle[i], label = 'HH @ %d mV' % (iV_initial) )

    ax.tick_params(direction='in', axis='both')    
    ax.legend(loc = 'best', fontsize=lfontsize, frameon=False)
    ax.set_xlabel ('time (ms)', fontsize= labelfontsize)
    ax.set_ylabel ('-V (mV)', fontsize= labelfontsize)

ax.set_title('%s in the primary publication' % (prefig))
plt.grid(True,linestyle='-.')
plt.savefig(figfile)        
plt.show()




