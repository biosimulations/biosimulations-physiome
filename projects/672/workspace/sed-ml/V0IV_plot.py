import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilename = 'V0'
# Figure name
prefig = 'V0_IV'
figfile = '%s.png' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 7, 6
fig = plt.figure(figsize=(fw,fh))
# Set subplots
subpRow, subpCol = 1, 1
ax, lns = {}, {}
lfontsize, labelfontsize = 12, 12 # legend, label fontsize
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Read data from the files
plotindex = [1]
x_name = 'outputs/minus_V'
y_names =['outputs/Ii']
y_labels =['$I_i(\mu A/cm^2)$']

filename ='%s.csv' % (prefilename)
data = pd.read_csv(filename)
for i, y_name in enumerate(y_names):       
    x_data = data[x_name]   
    y_data = data[y_name]
    ax[i] = fig.add_subplot(subpRow, subpCol, plotindex[i])
    ax[i].plot(x_data, y_data, color=cycle[0])
    ax[i].tick_params(direction='in', axis='both')   
    ax[i].set_ylabel (y_labels[i], fontsize= labelfontsize)
    ax[i].grid(linestyle='-.')
    ax[i].set_xlabel ('-V (mV)', fontsize= labelfontsize)   
    
plt.savefig(figfile)        
plt.show()




