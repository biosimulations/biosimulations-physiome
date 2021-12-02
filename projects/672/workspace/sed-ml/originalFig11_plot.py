import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilename = 'simFig11'
# Figure name
prefig = 'Fig11'
figfile = 'original%s.png' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 12, 10
fig = plt.figure(figsize=(fw,fh))
# Set subplots
subpRow, subpCol = 5, 2
ax, lns = {}, {}
lfontsize, labelfontsize = 12, 12 # legend, label fontsize
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Read data from the files
V_clamp = [-5, -10.01, -20, -30, -40, -60, -80, -100, -115, -130]
plotindex = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10]
fileindex =['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
x_name = 'outputs/time'
y_name ='outputs/Ii'

for i, iV_clamp in enumerate(V_clamp):
    filename ='%s_(%d)mV.csv' % (prefilename, iV_clamp)
    data = pd.read_csv(filename)
    x_data = data[x_name]   
    y_data = data[y_name]
    T_data = data['parameters/T']
    ax[i] = fig.add_subplot(subpRow, subpCol, plotindex[i])
    ax[i].plot(x_data, y_data, color=cycle[0], label = 'CellML @ %d mV' % (iV_clamp ))
    ax[i].tick_params(direction='in', axis='both')   

    filename = 'fig11_%s.csv' % fileindex[i]
    odata = pd.read_csv(filename)
    ox_data = odata['x']   
    oy_data = odata['Curve1']
    ax[i].plot(ox_data, oy_data, '.', color=cycle[1], label = 'HH @ %d mV' % (iV_clamp ) )


    ax[i].legend(loc = 'best', fontsize=lfontsize, frameon=False)
    if plotindex[i] in [9,10]: 
        ax[i].set_xlabel ('time(ms)', fontsize= labelfontsize)
    else:
        ax[i].set_xticklabels([])
    
plt.savefig(figfile)        
plt.show()




