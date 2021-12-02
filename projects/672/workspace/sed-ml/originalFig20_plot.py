import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilename = 'simFig20'
# Figure name
prefig = 'Fig20'
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
suffixfile=['A', 'B', 'C', 'D',]
# For read data from the simulation output files
t_stim = [20, 4.7284, 5.7302, 7.7352]
x_name = 'outputs/time'
y_name ='outputs/minus_V'
pointInterval=0.0001
for i, iend in enumerate(t_stim):
    filename ='%s_%s.csv' % (prefilename, suffixfile[i])      
    data = pd.read_csv(filename)
    if i>0:
       x_data = data[x_name][int(t_stim[i]/pointInterval+2):]   
       y_data = data[y_name][int(t_stim[i]/pointInterval+2):]
    else:
       x_data = data[x_name]   
       y_data = data[y_name]

    ax.plot(x_data, y_data,  color=cycle[i], label = '%s: CellML @ t=%0.1f ms' % (suffixfile[i],iend ) )

    filename = 'fig20_%s.csv' % suffixfile[i]
    odata = pd.read_csv(filename)
    ox_data = odata['x']   
    oy_data = odata['Curve1']
    ax.plot(ox_data, oy_data, '.', color=cycle[i], label = '%s: HH @ t=%0.1f ms' % (suffixfile[i],iend ) )

    ax.tick_params(direction='in', axis='both')    
    ax.legend(loc='upper right', bbox_to_anchor=(0.8, 0.8), fontsize=lfontsize, frameon=False)
    ax.set_xlabel ('time (ms)', fontsize= labelfontsize)
    ax.set_ylabel ('-V (mV)', fontsize= labelfontsize)

ax.set_title('%s in the primary publication' % (prefig))
plt.axhline(y=0.0, color="black", linestyle="--")
plt.savefig(figfile)        
plt.show()




