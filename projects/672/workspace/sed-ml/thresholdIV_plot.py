import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilename = 'simFig12'
V_initial = [-90, -15, -7]
# Figure name
prefig = 'threshold_IV'
figfile = '%s.png' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 6, 6
fig = plt.figure(figsize=(fw,fh))
# Set subplots
subpRow, subpCol = 1, 1
ax, lns = {}, {}
lfontsize, labelfontsize = 10, 10 # legend, label fontsize
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Read data from the files
x_name = 'outputs/minus_V'
y_name ='outputs/Ii'
y_labels =['$I_i(\mu A/cm^2)$']

ax = fig.add_subplot(subpRow, subpCol, 1)

for i, iV_initial in enumerate(V_initial):
    filename ='%s_(%d)mV.csv' % (prefilename, iV_initial)
    data = pd.read_csv(filename)       
    x_data = data[x_name]   
    y_data = data[y_name] 

    ax.plot(x_data, y_data, color=cycle[i],label='V_init=%d mV' % (iV_initial))

prefilename = 'simFig22'
V_initial = 30
filename ='%s_(%d)mV.csv' % (prefilename, V_initial)
data = pd.read_csv(filename)       
x_data = data[x_name]   
y_data = data[y_name] 
ax.plot(x_data, y_data, color=cycle[i+1],label='V_init=%d mV' % (V_initial))

ax.tick_params(direction='in', axis='both')   
ax.set_ylabel (y_labels[0], fontsize= labelfontsize)
ax.grid(linestyle='-.')
ax.set_xlabel ('-V (mV)', fontsize= labelfontsize)   
ax.legend(loc = 'best', fontsize=lfontsize, frameon=False)   
plt.savefig(figfile)        
plt.show()




