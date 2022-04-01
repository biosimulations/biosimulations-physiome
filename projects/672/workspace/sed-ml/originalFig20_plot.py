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

for i, iend in enumerate(t_stim):
    filename ='%s_%s.csv' % (prefilename, suffixfile[i])      
    data = pd.read_csv(filename)
    x_data = data[x_name]   
    y_data = data[y_name]
    T_data = data['parameters/T']
    ax.plot(x_data, y_data,  color=cycle[i], label = '%s:CellML model @ t=%0.1f ms, %0.1f ℃' % (suffixfile[i],iend, T_data[1] ) )

    filename = 'fig20_%s.csv' % suffixfile[i]
    odata = pd.read_csv(filename)
    ox_data = odata['x']   
    oy_data = odata['Curve1']
    ax.plot(ox_data, oy_data, '.', color=cycle[i], label = '%s:HH model @ t=%0.1f ms, %0.1f ℃' % (suffixfile[i],iend, T_data[1] ) )

    ax.tick_params(direction='in', axis='both')    
    ax.legend(loc = 'best', fontsize=lfontsize, frameon=False)
    ax.set_xlabel ('time (ms)', fontsize= labelfontsize)
    ax.set_ylabel ('-V (mV)', fontsize= labelfontsize)

plt.savefig(figfile)        
plt.show()




